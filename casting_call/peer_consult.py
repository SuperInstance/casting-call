"""
Peer Consultation Layer for casting-call.

Makes the metaphor REAL: after a primary model produces output, a counterpoint
model reviews it. The exchange is logged as structured JSON.

This is the implementation KimiCode said was missing — "the team asking each
other isn't implemented yet — it's dramatized." Now it's implemented.

Usage:
    from casting_call.peer_consult import PeerConsultant

    pc = PeerConsultant()
    result = pc.consult("intent_parse", "What is the hermit crab protocol?")
    # result contains: primary_output, review_output, synthesis, exchange_log

The exchange log is a list of SWMIDI-compatible events:
    {
        "role": "primary" | "reviewer" | "synthesis",
        "model": "SEED_MINI",
        "tick": 0,
        "pitch": 60,          # event type code
        "velocity": 96,       # confidence 0-127
        "error_mask": 0,      # friction flags
        "content": "...",
    }
"""

from __future__ import annotations

import json
import logging
import os
import time
from dataclasses import dataclass, field
from typing import Any, Optional

import requests

from casting_call.atlas import ModelProfile, VoiceCharacter
from casting_call.casting import CastingDirector
from casting_call.pipeline import get_profile

logger = logging.getLogger(__name__)

# ── DeepInfra model ID mapping ───────────────────────────────────────
# Maps atlas model names to actual DeepInfra API model IDs.
DEEPINFRA_MODEL_MAP: dict[str, str] = {
    "SEED_MINI": "ByteDance/Seed-2.0-mini",
    "SEED_PRO": "ByteDance/Seed-2.0-pro",
    "QWEN3_6": "Qwen/Qwen3.6-35B-A3B",
    "QWEN3_CODER": "Qwen/Qwen3-Coder-480B",
    "HERMES_405B": "NousResearch/Hermes-3-Llama-3.1-405B",
    "NEMOTRON_ULTRA": "nvidia/Nemotron-3-Ultra-550B",
    "GLM_5_2": "zai-org/GLM-5.2",
}

# DeepSeek direct API models (cheaper, use direct API)
DEEPSEEK_MODEL_MAP: dict[str, str] = {
    "DEEPSEEK_V4_FLASH": "deepseek-chat",
    "DEEPSEEK_V4_PRO": "deepseek-reasoner",
}

# Counterpoint partners — different voice for each role.
# The primary is cast by the director; the counterpoint is chosen here
# to provide genuine structural contrast (different voice character).
COUNTERPOINT_MAP: dict[str, str] = {
    "intent_parse":         "QWEN3_6",          # analog synth → versatile
    "planning":             "SEED_MINI",         # synth pro → analog synth
    "code_gen":             "HERMES_405B",       # precision → roland
    "personality_wrap":     "NEMOTRON_ULTRA",    # roland → pipe organ
    "safety_check":         "SEED_MINI",         # pipe organ → analog synth
    "creative_ideation":    "QWEN3_6",           # analog synth → versatile
    "spatial_reasoning":    "HERMES_405B",       # versatile → roland
    "synthesis":            "DEEPSEEK_V4_FLASH", # yamaha → sensory direct
    "vision":               "SEED_PRO",          # yamaha → synth pro
    "voice":                "QWEN3_6",           # roland → versatile
    "forced_perspective":   "NEMOTRON_ULTRA",    # analog synth → pipe organ
    "creative_nonfiction":  "DEEPSEEK_V4_FLASH", # synth pro → sensory direct
    "sensory_creative":     "SEED_PRO",          # sensory direct → synth pro
}


@dataclass
class ExchangeEvent:
    """A single event in a peer consultation exchange.

    Structured to map cleanly onto SWMIDI-8 wire format:
    status = (type_nibble << 4) | channel
    pitch = event type code (0-127)
    velocity = confidence (0-127)
    error_mask = friction flags (8 bits)
    tick = PPQ position on the BeatClock
    """
    role: str           # "primary", "reviewer", "synthesis"
    model: str          # atlas model name
    tick: int           # BeatClock position (96 PPQ)
    pitch: int          # event type code (0-127)
    velocity: int       # confidence 0-127
    error_mask: int     # friction bitmask
    content: str        # the actual text output
    latency_ms: int = 0 # wall-clock latency
    timestamp: str = "" # ISO timestamp

    def to_swmidi_dict(self) -> dict[str, Any]:
        """Convert to SWMIDI-compatible dictionary."""
        return {
            "status": (self.pitch >> 4, 0),  # type nibble, channel
            "pitch": self.pitch,
            "velocity": self.velocity,
            "error_mask": self.error_mask,
            "tick": self.tick,
            "role": self.role,
            "model": self.model,
            "content": self.content,
            "latency_ms": self.latency_ms,
            "timestamp": self.timestamp,
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "role": self.role,
            "model": self.model,
            "tick": self.tick,
            "pitch": self.pitch,
            "velocity": self.velocity,
            "error_mask": self.error_mask,
            "content": self.content,
            "latency_ms": self.latency_ms,
            "timestamp": self.timestamp,
        }


@dataclass
class ConsultationResult:
    """The full result of a peer consultation."""
    primary_model: str
    reviewer_model: str
    primary_output: str
    review_output: str
    synthesis: str
    primary_confidence: int    # 0-127
    review_confidence: int     # 0-127
    synthesis_confidence: int  # 0-127
    improved: bool             # did the review change the output?
    exchange_log: list[ExchangeEvent] = field(default_factory=list)
    total_latency_ms: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "primary_model": self.primary_model,
            "reviewer_model": self.reviewer_model,
            "primary_output": self.primary_output,
            "review_output": self.review_output,
            "synthesis": self.synthesis,
            "primary_confidence": self.primary_confidence,
            "review_confidence": self.review_confidence,
            "synthesis_confidence": self.synthesis_confidence,
            "improved": self.improved,
            "exchange_log": [e.to_dict() for e in self.exchange_log],
            "total_latency_ms": self.total_latency_ms,
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)


class PeerConsultant:
    """
    Real model-to-model consultation.

    After the primary model produces output, a counterpoint model reviews it.
    The exchange is logged as SWMIDI-compatible events.

    The primary is chosen by CastingDirector. The counterpoint is chosen to
    provide maximum structural contrast — a different voice character.
    """

    def __init__(
        self,
        director: CastingDirector | None = None,
        deepinfra_key: str | None = None,
        deepseek_key: str | None = None,
        deepinfra_url: str = "https://api.deepinfra.com/v1/openai/chat/completions",
        deepseek_url: str = "https://api.deepseek.com/v1/chat/completions",
    ):
        self.director = director or CastingDirector(__import__(
            "casting_call.atlas", fromlist=["ModelAtlas"]
        ).ModelAtlas.default())

        self.deepinfra_key = deepinfra_key or os.environ.get("DEEPINFRA_API_KEY", "")
        self.deepseek_key = deepseek_key or os.environ.get("DEEPSEEK_API_KEY", "")
        self.deepinfra_url = deepinfra_url
        self.deepseek_url = deepseek_url

    def _resolve_model_id(self, model_name: str) -> tuple[str, str]:
        """Resolve atlas model name to (api_endpoint, model_id)."""
        if model_name in DEEPINFRA_MODEL_MAP:
            return self.deepinfra_url, DEEPINFRA_MODEL_MAP[model_name]
        if model_name in DEEPSEEK_MODEL_MAP:
            return self.deepseek_url, DEEPSEEK_MODEL_MAP[model_name]
        raise ValueError(f"Model {model_name} has no API mapping")

    def _call_model(
        self,
        model_name: str,
        messages: list[dict[str, str]],
        max_tokens: int = 512,
        temperature: float | None = None,
    ) -> tuple[str, int]:
        """
        Call a model via its API. Returns (content, latency_ms).
        """
        url, model_id = self._resolve_model_id(model_name)

        # Pick the right key
        if model_name in DEEPSEEK_MODEL_MAP:
            headers = {
                "Authorization": f"Bearer {self.deepseek_key}",
                "Content-Type": "application/json",
            }
        else:
            headers = {
                "Authorization": f"Bearer {self.deepinfra_key}",
                "Content-Type": "application/json",
            }

        body: dict[str, Any] = {
            "model": model_id,
            "messages": messages,
            "max_tokens": max_tokens,
        }
        if temperature is not None:
            body["temperature"] = temperature

        t0 = time.time()
        resp = requests.post(url, headers=headers, json=body, timeout=30)
        latency_ms = int((time.time() - t0) * 1000)

        resp.raise_for_status()
        data = resp.json()
        content = data["choices"][0]["message"]["content"]
        return content, latency_ms

    def _confidence_to_velocity(self, text: str) -> int:
        """
        Estimate confidence from output length and hedging language.
        Maps to MIDI velocity (0-127).
        """
        if not text or len(text.strip()) < 10:
            return 32  # low confidence
        hedging = text.lower().count("perhaps") + text.lower().count("might") + \
                   text.lower().count("could") + text.lower().count("maybe") + \
                   text.lower().count("uncertain") + text.lower().count("unclear")
        base = 100
        penalty = min(hedging * 8, 60)
        return max(base - penalty, 40)

    def _detect_friction(self, text: str) -> int:
        """
        Detect friction dimensions from model output.
        Returns an 8-bit error mask.
        """
        mask = 0
        low = text.lower()
        if "error" in low or "invalid" in low or "malformed" in low:
            mask |= 0x04  # SEMANTIC
        if "unsafe" in low or "warning" in low or "inappropriate" in low:
            mask |= 0x08  # SAFETY
        if "timeout" in low or "unavailable" in low or "not found" in low:
            mask |= 0x10  # RESOURCE
        if "cannot" in low or "unable" in low or "permission" in low:
            mask |= 0x40  # AUTHORITY
        return mask

    def consult(
        self,
        role: str,
        prompt: str,
        max_tokens: int = 512,
        tick_offset: int = 0,
    ) -> ConsultationResult:
        """
        Run a full peer consultation.

        1. Cast the primary model for the role.
        2. Cast the counterpoint (different voice character).
        3. Primary produces output.
        4. Reviewer reviews primary's output.
        5. Synthesize a final answer from both.

        All steps logged as ExchangeEvents on the BeatClock.

        Args:
            role: Pipeline role (e.g., 'intent_parse', 'code_gen').
            prompt: The input prompt/task.
            max_tokens: Max tokens per model call.
            tick_offset: Starting tick for the exchange log (96 PPQ).

        Returns:
            ConsultationResult with all outputs and the exchange log.
        """
        exchange: list[ExchangeEvent] = []
        total_t0 = time.time()

        # 1. Cast primary
        primary_profile = self.director.cast(role)
        primary_name = primary_profile.name

        # 2. Cast counterpoint
        reviewer_name = COUNTERPOINT_MAP.get(role, "QWEN3_6")

        # Ensure they're different
        if reviewer_name == primary_name:
            reviewer_name = "SEED_PRO" if primary_name != "SEED_PRO" else "QWEN3_6"

        logger.info(f"Peer consultation: {primary_name} (primary) → {reviewer_name} (reviewer)")

        # 3. Primary produces output
        primary_msgs = [{"role": "user", "content": prompt}]
        primary_output, primary_ms = self._call_model(
            primary_name, primary_msgs, max_tokens, primary_profile.temperature
        )

        exchange.append(ExchangeEvent(
            role="primary",
            model=primary_name,
            tick=tick_offset,
            pitch=0x90,  # NOTE_ON
            velocity=self._confidence_to_velocity(primary_output),
            error_mask=self._detect_friction(primary_output),
            content=primary_output,
            latency_ms=primary_ms,
            timestamp=time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        ))

        # 4. Reviewer reviews primary's output
        review_prompt = (
            f"Another AI model (the {primary_profile.voice_character.value} voice) "
            f"was asked: \"{prompt}\"\n\n"
            f"It answered:\n\"{primary_output}\"\n\n"
            f"Review this answer. Is it correct? Is anything missing or wrong? "
            f"Provide an improved version if needed. Be specific about what you'd change."
        )
        reviewer_msgs = [{"role": "user", "content": review_prompt}]

        try:
            reviewer_profile = self.director.atlas.get(reviewer_name)
            reviewer_temp = reviewer_profile.temperature if reviewer_profile else 0.7
            review_output, review_ms = self._call_model(
                reviewer_name, reviewer_msgs, max_tokens, reviewer_temp
            )
        except Exception as e:
            logger.warning(f"Reviewer {reviewer_name} failed: {e}")
            review_output = f"[Review unavailable: {e}]"
            review_ms = 0

        exchange.append(ExchangeEvent(
            role="reviewer",
            model=reviewer_name,
            tick=tick_offset + 96,  # next beat
            pitch=0x90,  # NOTE_ON
            velocity=self._confidence_to_velocity(review_output),
            error_mask=self._detect_friction(review_output),
            content=review_output,
            latency_ms=review_ms,
            timestamp=time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        ))

        # 5. Synthesize: primary sees the review and produces final answer
        synthesis_msgs = [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": primary_output},
            {"role": "user", "content": f"A reviewer suggested:\n\"{review_output}\"\n\nProvide the best final answer incorporating any valid feedback."},
        ]

        try:
            synthesis_output, synth_ms = self._call_model(
                primary_name, synthesis_msgs, max_tokens, primary_profile.temperature
            )
        except Exception as e:
            logger.warning(f"Synthesis round failed: {e}")
            synthesis_output = primary_output  # fall back to primary
            synth_ms = 0

        improved = synthesis_output.strip() != primary_output.strip()

        exchange.append(ExchangeEvent(
            role="synthesis",
            model=primary_name,
            tick=tick_offset + 192,  # two beats later
            pitch=0x90 if improved else 0x80,  # NOTE_ON if improved, NOTE_OFF if same
            velocity=self._confidence_to_velocity(synthesis_output),
            error_mask=self._detect_friction(synthesis_output),
            content=synthesis_output,
            latency_ms=synth_ms,
            timestamp=time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        ))

        total_ms = int((time.time() - total_t0) * 1000)

        return ConsultationResult(
            primary_model=primary_name,
            reviewer_model=reviewer_name,
            primary_output=primary_output,
            review_output=review_output,
            synthesis=synthesis_output,
            primary_confidence=exchange[0].velocity,
            review_confidence=exchange[1].velocity,
            synthesis_confidence=exchange[2].velocity,
            improved=improved,
            exchange_log=exchange,
            total_latency_ms=total_ms,
        )

    def consult_batch(
        self,
        consultations: list[tuple[str, str]],
    ) -> list[ConsultationResult]:
        """
        Run multiple consultations. Sequential for now; could be parallelized.

        Args:
            consultations: List of (role, prompt) tuples.

        Returns:
            List of ConsultationResults.
        """
        return [self.consult(role, prompt) for role, prompt in consultations]


# ── Convenience function ─────────────────────────────────────────────

def peer_consult(
    role: str,
    prompt: str,
    deepinfra_key: str | None = None,
    deepseek_key: str | None = None,
) -> ConsultationResult:
    """
    One-shot peer consultation.

    Usage:
        result = peer_consult("intent_parse", "What is 2+2?")
        print(result.synthesis)
        print(result.exchange_log)
    """
    pc = PeerConsultant(deepinfra_key=deepinfra_key, deepseek_key=deepseek_key)
    return pc.consult(role, prompt)
