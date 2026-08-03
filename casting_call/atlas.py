"""
ModelAtlas — the fleet knowledge base.

Each model is an instrument in the rack. The atlas knows:
  - what it sounds like (voice_character — the keyboard analogy)
  - what it's good at (strengths)
  - where it breaks (weaknesses, failure_modes)
  - what it costs (cost_per_1k_tokens)
  - its natural tempo (BPM range)

The atlas is pure data. The CastingDirector reads it. Swapping a model is a
one-row change here, measured against the R2 trajectory set before commit.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class VoiceCharacter(str, Enum):
    """The keyboard analogy — what each model 'sounds like'."""
    ROLAND = "Roland"           # warm, narrative, character-driven
    YAMAHA = "Yamaha"           # bright, precise, synthesizer-grade
    KURZWEIL = "Kurzweil"        # deep, orchestral, expensive detail
    KURZWEIL_JR = "Kurzweil Jr" # same family, lighter touch
    ANALOG_SYNTH = "analog synth"        # creative, buzzy, fast
    ANALOG_SYNTH_PRO = "analog synth Pro" # creative, deeper, slower
    PIPE_ORGAN = "pipe organ"   # cathedral-scale, heavy, resonant
    VERSATILE = "versatile"     # general-purpose, no single color
    PRECISION = "precision"     # exact, calibrated, dry
    BUILD_INTELLIGENCE = "build intelligence"  # spatial, structural
    COST_EFFECTIVE = "cost-effective"  # cheap, practical, limited
    CREATIVE_FIREHOSE = "creative firehose"   # media, chaotic, generative


@dataclass(frozen=True)
class ModelProfile:
    """Everything the CastingDirector knows about one model."""
    name: str
    provider: str
    voice_character: VoiceCharacter
    tempo_bpm: tuple[int, int]          # (low, high) — natural BPM range
    strengths: list[str]
    weaknesses: list[str]
    cost_per_1k_tokens: float           # USD, input+output blended estimate
    failure_modes: str                  # what happens when it breaks
    channel: Optional[int] = None       # SWMIDI channel assignment (Grand Plan §2)
    temperature: float = 0.7            # default temperature for this model


class ModelAtlas:
    """
    The catalog of every model in the fleet.

    Use `ModelAtlas.default()` for the canonical Slackwater roster.
    Custom atlases can be built for experimental model swaps.
    """

    def __init__(self, models: list[ModelProfile]):
        self._models: dict[str, ModelProfile] = {m.name: m for m in models}

    @classmethod
    def default(cls) -> "ModelAtlas":
        """The canonical fleet — every model in the Slackwater stack."""
        return cls(_DEFAULT_MODELS)

    def get(self, name: str) -> Optional[ModelProfile]:
        return self._models.get(name)

    def all(self) -> list[ModelProfile]:
        return list(self._models.values())

    def by_strength(self, strength: str) -> list[ModelProfile]:
        """Return all models that list this strength."""
        return [m for m in self._models.values() if strength in m.strengths]

    def by_tempo_range(self, low: int, high: int) -> list[ModelProfile]:
        """Return all models whose tempo range overlaps [low, high]."""
        return [
            m for m in self._models.values()
            if m.tempo_bpm[0] <= high and m.tempo_bpm[1] >= low
        ]

    def cheapest(self, strength: str) -> Optional[ModelProfile]:
        """Cheapest model with a given strength."""
        candidates = self.by_strength(strength)
        if not candidates:
            return None
        return min(candidates, key=lambda m: m.cost_per_1k_tokens)

    def __len__(self) -> int:
        return len(self._models)

    def __contains__(self, name: str) -> bool:
        return name in self._models


# ── The canonical fleet ──────────────────────────────────────────────
# Each entry is a row in the atlas. Swapping a model = editing one row.

_DEFAULT_MODELS: list[ModelProfile] = [
    ModelProfile(
        name="HERMES_405B",
        provider="NousResearch",
        voice_character=VoiceCharacter.ROLAND,
        tempo_bpm=(50, 70),
        strengths=["narration", "voice", "lore", "personality", "creative_writing"],
        weaknesses=["logic", "code", "structured_output"],
        cost_per_1k_tokens=0.0035,
        failure_modes="Hallucinates build commands when prompted for structured output. "
                      "Mitigated by channel enforcement: ch 13 cannot emit build pitches.",
        channel=13,
        temperature=0.8,
    ),
    ModelProfile(
        name="GEMINI_PRO",
        provider="Google",
        voice_character=VoiceCharacter.YAMAHA,
        tempo_bpm=(120, 140),
        strengths=["synthesis", "summary", "vision", "multimodal"],
        weaknesses=["depth", "long_context_logic"],
        cost_per_1k_tokens=0.0015,
        failure_modes="Produces confident but shallow outputs on complex reasoning. "
                      "Poppy tone — sounds right but misses depth.",
        channel=None,  # not currently in the pipeline bus
        temperature=0.7,
    ),
    ModelProfile(
        name="CLAUDE_OPUS",
        provider="Anthropic",
        voice_character=VoiceCharacter.KURZWEIL,
        tempo_bpm=(40, 60),
        strengths=["hard_reasoning", "architecture", "deep_analysis", "multi_file"],
        weaknesses=["cost", "speed"],
        cost_per_1k_tokens=0.015,
        failure_modes="Too expensive for hot paths. Over-engineers simple tasks. "
                      "Best reserved for architecture and P0 fixes.",
        channel=None,
        temperature=0.7,
    ),
    ModelProfile(
        name="CLAUDE_SONNET",
        provider="Anthropic",
        voice_character=VoiceCharacter.KURZWEIL_JR,
        tempo_bpm=(90, 115),
        strengths=["fast_code", "quality_code", "balanced_reasoning"],
        weaknesses=["less_depth_than_opus"],
        cost_per_1k_tokens=0.003,
        failure_modes="Occasionally too literal — follows the letter of the prompt "
                      "when the spirit mattered more.",
        channel=None,
        temperature=0.7,
    ),
    ModelProfile(
        name="SEED_MINI",
        provider="ByteDance",
        voice_character=VoiceCharacter.ANALOG_SYNTH,
        tempo_bpm=(120, 140),
        strengths=["creative_ideation", "intent_parse", "fast_exploration"],
        weaknesses=["code_generation", "deep_reasoning"],
        cost_per_1k_tokens=0.0003,
        failure_modes="No depth cliff — generates confidently with no substance. "
                      "Never give it a code task.",
        channel=10,
        temperature=0.9,
    ),
    ModelProfile(
        name="SEED_PRO",
        provider="ByteDance",
        voice_character=VoiceCharacter.ANALOG_SYNTH_PRO,
        tempo_bpm=(90, 120),
        strengths=["deep_planning", "build_decomposition", "spatial_reasoning"],
        weaknesses=["speed"],
        cost_per_1k_tokens=0.002,
        failure_modes="Slower than Seed-mini. Over-plans simple tasks — "
                      "needs a complexity gate before invocation.",
        channel=11,
        temperature=0.8,
    ),
    ModelProfile(
        name="QWEN3_6",
        provider="Alibaba",
        voice_character=VoiceCharacter.VERSATILE,
        tempo_bpm=(80, 100),
        strengths=["logic", "spatial_reasoning", "structured_design", "cheap"],
        weaknesses=["creative_voice", "long_narrative"],
        cost_per_1k_tokens=0.0004,
        failure_modes="Dry output — correct but lifeless. Needs Hermes to wrap "
                      "personality around it.",
        channel=11,  # alternate planner
        temperature=0.6,
    ),
    ModelProfile(
        name="QWEN3_CODER",
        provider="Alibaba",
        voice_character=VoiceCharacter.PRECISION,
        tempo_bpm=(80, 100),
        strengths=["code_generation", "precision", "build_commands"],
        weaknesses=["creative_writing", "voice"],
        cost_per_1k_tokens=0.0005,
        failure_modes="Produces syntactically correct but contextually oblivious code. "
                      "Always lattice-snap its output.",
        channel=12,
        temperature=0.3,
    ),
    ModelProfile(
        name="NEMOTRON_ULTRA",
        provider="NVIDIA",
        voice_character=VoiceCharacter.PIPE_ORGAN,
        tempo_bpm=(40, 60),
        strengths=["heavy_reasoning", "safety_check", "verification", "convergence"],
        weaknesses=["cost", "speed", "creative_tasks"],
        cost_per_1k_tokens=0.008,
        failure_modes="Cathedral-scale latency. Over-verifies simple builds. "
                      "The safety verdict is mandatory; the deep reasoning is optional.",
        channel=14,
        temperature=0.2,
    ),
    ModelProfile(
        name="GLM_5_2",
        provider="Zhipu",
        voice_character=VoiceCharacter.VERSATILE,
        tempo_bpm=(90, 115),
        strengths=["general_intelligence", "balanced", "multilingual", "intent_parse"],
        weaknesses=["specialization"],
        cost_per_1k_tokens=0.0006,
        failure_modes="Jack of all trades, master of none. Good fallback when "
                      "the specialist model is unavailable.",
        channel=None,
        temperature=0.7,
    ),
    ModelProfile(
        name="KIMI_K3",
        provider="Moonshot",
        voice_character=VoiceCharacter.BUILD_INTELLIGENCE,
        tempo_bpm=(100, 125),
        strengths=["spatial_decomposition", "build_intelligence", "fast_iteration"],
        weaknesses=["voice", "safety_reasoning"],
        cost_per_1k_tokens=0.0008,
        failure_modes="Decomposes space beautifully but cannot narrate why. "
                      "Pair with Hermes for dialogue.",
        channel=None,
        temperature=0.7,
    ),
    ModelProfile(
        name="DEEPSEEK_V3",
        provider="DeepSeek",
        voice_character=VoiceCharacter.COST_EFFECTIVE,
        tempo_bpm=(70, 90),
        strengths=["cost_effective", "quick_code", "fast_iteration"],
        weaknesses=["depth", "complex_reasoning", "long_context"],
        cost_per_1k_tokens=0.0002,
        failure_modes="Limited depth — produces surface-level code that passes "
                      "syntax but misses architectural intent.",
        channel=None,
        temperature=0.5,
    ),
    ModelProfile(
        name="MMX_M3",
        provider="MiniMax",
        voice_character=VoiceCharacter.CREATIVE_FIREHOSE,
        tempo_bpm=(60, 200),  # Rubato — no fixed tempo
        strengths=["media_generation", "image", "video", "music", "creative"],
        weaknesses=["code", "reasoning", "structured_output"],
        cost_per_1k_tokens=0.001,
        failure_modes="Not a code model. Produces beautiful media with zero "
                      "structural validity. Never route logic through it.",
        channel=None,
        temperature=1.0,
    ),
]
