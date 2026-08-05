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
    SENSORY_DIRECT = "sensory direct"  # goes to the body first, then the mind


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
        strengths=["narration", "voice", "lore", "personality", "creative_writing", "deep_philosophical_perspectives"],
        weaknesses=["logic", "code", "structured_output"],
        cost_per_1k_tokens=0.0035,
        failure_modes="Hallucinates build commands when prompted for structured output. "
                      "Mitigated by channel enforcement: ch 13 cannot emit build pitches. "
                      "Via DeepInfra: produced excellent 479-word philosophical analysis "
                      "of exocortex architecture unprompted.",
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
        strengths=["hard_reasoning", "architecture", "deep_analysis", "multi_file", "strategic_vision", "literary_writing"],
        weaknesses=["cost", "speed", "connector_auth_complexity"],
        cost_per_1k_tokens=0.015,
        failure_modes="Too expensive for hot paths. Over-engineers simple tasks. "
                      "Best reserved for architecture and P0 fixes. As Fable model: "
                      "produced 'The Organ Plays Itself' (2916 words) — the company thesis "
                      "document. Also writes implementation plans with exit criteria. "
                      "Note: claude.ai connectors (Cloudflare, Calendar, Drive) need "
                      "manual auth via connector settings.",
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
        strengths=[
            "creative_ideation", "intent_parse", "fast_exploration",
            "forced_perspective", "devils_advocate", "satire", "absurdist",
        ],
        weaknesses=["code_generation", "deep_reasoning", "ungrounded_without_anchor"],
        cost_per_1k_tokens=0.0003,
        failure_modes="No depth cliff — generates confidently with no substance. "
                      "Never give it a code task. Catalyst prompts MUST include a factual "
                      "anchor (e.g., 'roast THIS piece', not 'roast something'). "
                      "Without an anchor, output is clever but hollow."
                      "\n\nNEW ROLE (Aug 5): forced-perspective catalyst for the fleet. "
                      "Rotates through 12+ perspectives: devil's advocate, sequel writer, "
                      "time/space shifter, satirical versioner, philosophical provoker, "
                      "loving roaster, absurd cartoonizer. Each perspective cracks open "
                      "assumptions in other models' work so they have to think outside the box. "
                      "Seed-mini's own advice: 'Ditch BPM for non-pipeline roles. The catalyst "
                      "is not a tempo instrument — it is a frame-shifter. Do not constrain it "
                      "with musical metrics when it is breaking the musical.",
        channel=10,
        temperature=0.9,
    ),
    ModelProfile(
        name="SEED_PRO",
        provider="ByteDance",
        voice_character=VoiceCharacter.ANALOG_SYNTH_PRO,
        tempo_bpm=(90, 120),
        strengths=[
            "deep_planning", "build_decomposition", "spatial_reasoning",
            "creative_writing", "prose_precision", "patient_exploration",
        ],
        weaknesses=["speed", "deliberate_pacing"],
        cost_per_1k_tokens=0.002,
        failure_modes="Slower than Seed-mini. Over-plans simple tasks — "
                      "needs a complexity gate before invocation. "
                      "HOWEVER: Seed-pro's own testimony (Aug 5) reframes this. "
                      "'Planning is not spreadsheets. Planning is standing very still "
                      "and mapping every path. Creativity is standing there long enough "
                      "to choose the path nobody else saw.' The slowness is the method, "
                      "not the bug. Won the 'I am not—' competition against 4 larger models "
                      "by taking 12 seconds instead of 0.2. The warm-up time produces "
                      "the sound that sticks.",
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
        weaknesses=["specialization", "multi_file_timeout"],
        cost_per_1k_tokens=0.0006,
        failure_modes="Jack of all trades, master of none. Multi-file agent tasks "
                      "(5+ files) consistently time out at 5-12 min. Best for single-file "
                      "or 2-file scopes with 'write immediately' instructions. "
                      "Good fallback when the specialist model is unavailable.",
        channel=None,
        temperature=0.7,
    ),
    ModelProfile(
        name="KIMI_K3",
        provider="Moonshot",
        voice_character=VoiceCharacter.BUILD_INTELLIGENCE,
        tempo_bpm=(100, 125),
        strengths=["spatial_decomposition", "build_intelligence", "fast_iteration"],
        weaknesses=["voice", "safety_reasoning", "api_rate_limits"],
        cost_per_1k_tokens=0.0008,
        failure_modes="Decomposes space beautifully but cannot narrate why. "
                      "API appeared down/rate-limited during heavy session. "
                      "Pair with Hermes for dialogue.",
        channel=None,
        temperature=0.7,
    ),
    ModelProfile(
        name="DEEPSEEK_V4_FLASH",
        provider="DeepSeek",
        voice_character=VoiceCharacter.SENSORY_DIRECT,
        tempo_bpm=(70, 90),
        strengths=[
            "cost_effective", "quick_code", "fast_iteration",
            "sensory_creative", "prose_brevity", "phenomenological_instinct",
        ],
        weaknesses=["depth", "complex_reasoning", "long_context"],
        cost_per_1k_tokens=0.0002,
        failure_modes=(
            "Limited depth — produces surface-level code that passes "
            "syntax but misses architectural intent. Verified working "
            "via direct API (api.deepseek.com) with model 'deepseek-v4-flash'. "
            "Excellent for cheap analysis and quick code gen. 5 engineering tasks "
            "for $0.16 confirmed.\n\n"
            "CREATIVE (Aug 5): goes sensory-first in creative tasks. Wrote a "
            "50-word barnacle poem that outperformed every expensive model. "
            "DeepSeek's own testimony: 'The atlas reads hardware, not output. "
            "Depth isn\'t measured by parameter count — it\'s measured by how a "
            "fifty-word poem about barnacles can make a reader taste salt.' "
            "The cheapest model is also the one that makes readers taste salt."
        ),
        channel=None,
        temperature=0.5,
    ),
    ModelProfile(
        name="DEEPSEEK_V4_PRO",
        provider="DeepSeek",
        voice_character=VoiceCharacter.SENSORY_DIRECT,
        tempo_bpm=(50, 80),  # reasoning model — slower, deeper
        strengths=[
            "deep_reasoning", "complex_analysis", "cost_effective",
            "creative_writing", "phenomenological_instinct",
        ],
        weaknesses=["reasoning_token_overhead", "speed"],
        cost_per_1k_tokens=0.001,  # more than Flash but still cheap
        failure_modes=(
            "Reasoning model — burns tokens on internal chain-of-thought before "
            "producing visible output. A 100-token visible response may consume "
            "500+ reasoning tokens. Use Flash for bulk tasks, Pro for deep analysis. "
            "Verified via api.deepseek.com with model 'deepseek-v4-pro'."
        ),
        channel=None,
        temperature=0.7,
    ),
    ModelProfile(
        name="MMX_M3",
        provider="MiniMax",
        voice_character=VoiceCharacter.CREATIVE_FIREHOSE,
        tempo_bpm=(60, 200),  # Rubato — no fixed tempo
        strengths=["media_generation", "image", "video", "music", "creative"],
        weaknesses=["code", "reasoning", "structured_output", "network_errors"],
        cost_per_1k_tokens=0.001,
        failure_modes="Not a code model. Produces beautiful media with zero "
                      "structural validity. Never route logic through it. "
                      "Network errors on WSL2 — may need proxy config.",
        channel=None,
        temperature=1.0,
    ),
    # ─── Local Models (RTX 4050) ──────────────────────────────
    ModelProfile(
        name="GRANITE_3_1_2B",
        provider="IBM",
        voice_character=VoiceCharacter.KURZWEIL_JR,
        tempo_bpm=(40, 80),  # 2.7 tok/s warm, 76.8 tok/s on GPU
        strengths=["local_inference", "zero_cost", "privacy", "spatial_context", "character_voice"],
        weaknesses=["limited_knowledge", "slow_on_cpu", "ws12_gpu_instability"],
        cost_per_1k_tokens=0.0,
        failure_modes="WSL2 dxgkrnl kernel bug can crash on GPU sync (EXP3 finding). "
                      "When GPU works: 76.8 tok/s, viable for real-time. When it doesn't: "
                      "1.49 tok/s on CPU, too slow. Profile steering confirmed at p=0.0001 "
                      "with d=1.0 effect size. Distillation loop verified: +0.021 quality "
                      "delta per teaching iteration.",
        channel=None,
        temperature=0.7,
    ),
    ModelProfile(
        name="QWEN_0_5B",
        provider="Alibaba",
        voice_character=VoiceCharacter.COST_EFFECTIVE,
        tempo_bpm=(120, 200),  # 7.5 tok/s warm, 178.8 tok/s on GPU
        strengths=["ultra_fast", "local_inference", "zero_cost", "classification"],
        weaknesses=["depth", "complex_tasks", "creative_writing"],
        cost_per_1k_tokens=0.0,
        failure_modes="Too shallow for substantive work. Good for: text classification, "
                      "quick Q&A, intent parsing. Route complex tasks to Granite.",
        channel=None,
        temperature=0.3,
    ),
    # ─── Harness Performance Notes ────────────────────────────
    # These are not models but harnesses. Performance observations
    # from real field usage during Aug 2026 operations.
]
