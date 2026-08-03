# casting-call

**Model routing brain for the Slackwater AI pipeline. Pure data, pure functions, zero side effects.**

Layer 8 of the Slackwater stack. Maps pipeline roles to AI models via a capability atlas. Enforces the counterpoint constraint (no parallel octaves). Provides what-if analysis for model swaps. The pipeline calls `cast()` before each stage to determine which model to invoke.

---

## Architecture

```
  Layer 7: Perception  ──▶  Layer 8: Casting-Call  ──▶  Layer 9: Brain Pipeline
   (the ears)                   (the routing brain)         (the performance)
                                       │
                                       ▼
                              ┌────────────────┐
                              │  ModelAtlas    │
                              │  (13 models)   │
                              └───────┬────────┘
                                      │
                                cast(role)
                                      │
                                      ▼
                              ┌────────────────┐
                              │ CastingDirector│
                              │                │
                              │ • Role → Model │
                              │ • Counterpoint │
                              │ • What-if      │
                              │ • Tempo range  │
                              └────────────────┘
```

### Design Principles

1. **Pure data, pure functions** — the atlas is a frozen dataclass; the director has no I/O, no side effects, no mutation of defaults
2. **One-row model swaps** — changing a model is editing one `ModelProfile` entry, measured against the R2 trajectory set before commit
3. **Musical analogy throughout** — each model is an instrument with a voice character, natural tempo, and role in the ensemble

---

## The Atlas: 13-Model Fleet

| Model | Provider | Voice Character | BPM Range | Cost/1k | Channel | Role |
|-------|----------|----------------|-----------|---------|---------|------|
| `HERMES_405B` | NousResearch | Roland (warm) | 50–70 | $0.0035 | 13 | Personality, voice, lore |
| `GEMINI_PRO` | Google | Yamaha (bright) | 120–140 | $0.0015 | — | Synthesis, summary, vision |
| `CLAUDE_OPUS` | Anthropic | Kurzweil (deep) | 40–60 | $0.0150 | — | Architecture, hard reasoning |
| `CLAUDE_SONNET` | Anthropic | Kurzweil Jr | 90–115 | $0.0030 | — | Fast quality code |
| `SEED_MINI` | ByteDance | Analog synth | 120–140 | $0.0003 | 10 | Intent parse, ideation |
| `SEED_PRO` | ByteDance | Analog synth Pro | 90–120 | $0.0020 | 11 | Deep planning, decomposition |
| `QWEN3_6` | Alibaba | Versatile | 80–100 | $0.0004 | 11 | Logic, spatial reasoning |
| `QWEN3_CODER` | Alibaba | Precision | 80–100 | $0.0005 | 12 | Code generation |
| `NEMOTRON_ULTRA` | NVIDIA | Pipe organ | 40–60 | $0.0080 | 14 | Safety, verification, convergence |
| `GLM_5_2` | Zhipu | Versatile | 90–115 | $0.0006 | — | General intelligence, fallback |
| `KIMI_K3` | Moonshot | Build intelligence | 100–125 | $0.0008 | — | Spatial decomposition |
| `DEEPSEEK_V3` | DeepSeek | Cost-effective | 70–90 | $0.0002 | — | Quick code, fast iteration |
| `MMX_M3` | MiniMax | Creative firehose | 60–200 | $0.0010 | — | Media generation (rubato) |

### Voice Characters

The keyboard analogy maps each model to a synthesizer profile:

| Voice Character | Sound | Characteristics |
|----------------|-------|----------------|
| Roland | Warm, narrative | Character-driven, good at voice, weak at logic |
| Yamaha | Bright, precise | Synthesizer-grade clarity, fast, shallow on depth |
| Kurzweil | Deep, orchestral | Expensive detail, architectural reasoning |
| Kurzweil Jr | Same family, lighter | Faster than Opus, less depth |
| Analog synth | Creative, buzzy, fast | Excellent ideation, no code capability |
| Analog synth Pro | Creative, deeper, slower | Planning and decomposition |
| Pipe organ | Cathedral-scale | Heavy, resonant, maximum depth, slow |
| Precision | Exact, calibrated, dry | Code generation, syntactic correctness |
| Versatile | General-purpose | No single color, balanced fallback |
| Build intelligence | Spatial, structural | Decomposes space, cannot narrate |
| Cost-effective | Cheap, practical | Limited depth, budget option |
| Creative firehose | Media, chaotic, generative | Images/video/music, zero structural validity |

### Failure Modes

Each model entry documents how it breaks:

- **HERMES_405B**: Hallucinates build commands when prompted for structured output. Mitigated by channel enforcement — ch 13 cannot emit build pitches.
- **SEED_MINI**: No depth cliff — generates confidently with no substance. Never give it a code task.
- **QWEN3_CODER**: Produces syntactically correct but contextually oblivious code. Always lattice-snap its output.
- **NEMOTRON_ULTRA**: Cathedral-scale latency. Over-verifies simple builds. The safety verdict is mandatory; the deep reasoning is optional.
- **DEEPSEEK_V3**: Surface-level code that passes syntax but misses architectural intent.

---

## SWMIDI Channel Map

Models assigned to active pipeline channels use the SWMIDI (Slackwater MIDI) addressing scheme:

| Channel | Model | Stage |
|---------|-------|-------|
| 10 | Seed-2.0-mini | Intent parsing / creative ideation |
| 11 | Seed-2.0-pro / Qwen3.6 | Spatial planning (alternate) |
| 12 | Qwen3-Coder-480B | Code generation |
| 13 | Hermes-405B | Personality wrapping / voice |
| 14 | Nemotron-Ultra | Safety check / verification |
| 15 | — | META tempo events (BPM changes) |

Channels `None` (Gemini, Claude, GLM, Kimi, DeepSeek, MMX) are available in the atlas but not currently wired to the pipeline bus. They participate in what-if analysis and roundtable dispatch.

---

## CastingDirector API

### Role → Model Casting

```python
from casting_call import ModelAtlas, CastingDirector

atlas = ModelAtlas.default()
director = CastingDirector(atlas)

# Cast a single role
profile = director.cast("intent_parse")
# → SEED_MINI (Allegro, analog synth, $0.0003/1k)

# Cast with constraints
profile = director.cast("code_gen", context={
    "cost_ceiling": 0.001,
    "exclude": ["QWEN3_CODER"],
    "prefer_speed": True
})
# → DEEPSEEK_V3 (cheapest available coder)
```

### Pipeline Casting

```python
# Cast an entire pipeline at once
roles = ["intent_parse", "planning", "code_gen", "personality_wrap", "safety_check"]
cast = director.cast_pipeline(roles)
# → [SEED_MINI, SEED_PRO, QWEN3_CODER, HERMES_405B, NEMOTRON_ULTRA]
```

`cast_pipeline()` enforces counterpoint: no two roles get the same model unless the role explicitly allows it. The exclude set accumulates as roles are assigned.

### Fallback Chains

Each role has an ordered fallback chain. The director walks the chain and returns the first available model:

| Role | Primary | Fallback 1 | Fallback 2 | Fallback 3 |
|------|---------|-----------|-----------|-----------|
| `intent_parse` | SEED_MINI | GLM_5_2 | DEEPSEEK_V3 | — |
| `planning` | SEED_PRO | QWEN3_6 | CLAUDE_SONNET | — |
| `code_gen` | QWEN3_CODER | DEEPSEEK_V3 | CLAUDE_SONNET | — |
| `personality_wrap` | HERMES_405B | GLM_5_2 | — | — |
| `safety_check` | NEMOTRON_ULTRA | CLAUDE_OPUS | — | — |
| `creative_ideation` | SEED_MINI | MMX_M3 | — | — |
| `spatial_reasoning` | QWEN3_6 | KIMI_K3 | SEED_PRO | — |
| `synthesis` | GEMINI_PRO | GLM_5_2 | CLAUDE_SONNET | — |
| `vision` | GEMINI_PRO | GLM_5_2 | — | — |
| `voice` | HERMES_405B | GLM_5_2 | — | — |

### What-If Analysis

```python
# Can GLM-5.2 handle intent parsing?
director.swap("intent_parse", "GLM_5_2")
# → True (GLM_5_2 has 'intent_parse' strength)

# Full impact analysis
director.what_if("intent_parse", "GLM_5_2")
# → {
#     'feasible': True,
#     'cost_delta': +0.0003,  # more expensive
#     'tempo_delta': (-30, -25),  # slower
#     'reason': 'GLM_5_2 (versatile) can handle intent_parse...'
#   }
```

---

## Counterpoint Rules

The counterpoint constraint prevents wasted compute in the pipeline. Derived from species counterpoint in music theory:

### No Parallel Octaves

Two models never receive structurally identical prompts for the same stage. In music: two voices singing the same note in the same rhythm wastes a voice. In the pipeline: giving two models the same prompt wastes compute.

**Rule:** Same model in **adjacent** pipeline positions = parallel octaves = fail.
**Exception:** Same model in **non-adjacent** positions is a **recap** — that's fine. Seed-mini doing intent parsing (position 1) and creative ideation (position 5) is musical recapitulation, not redundancy.

```python
director.counterpoint_check([
    seed_mini,    # position 0
    seed_pro,     # position 1
    qwen3_coder,  # position 2
    seed_mini,    # position 3 — gap > 1, this is a recap ✓
    nemotron      # position 4
])
# → True (clean cast)

director.counterpoint_check([
    seed_mini,    # position 0
    seed_mini,    # position 1 — adjacent, parallel octaves ✗
    qwen3_coder,
    hermes,
    nemotron
])
# → False
```

---

## Tempo Profiles

Each pipeline role has a natural tempo derived from Italian musical terms:

| Role | Tempo | BPM Range | Description |
|------|-------|-----------|-------------|
| `intent_parse` | Allegro | 120–140 | Fast, expansive — parse before the player finishes sitting down |
| `planning` | Moderato | 90–110 | Walking pace — think but don't stall |
| `code_gen` | Andante | 80–100 | Steady, walking — code generation is a rhythm |
| `personality_wrap` | Adagio | 50–70 | Slow, expressive — the voice takes its time |
| `safety_check` | Largo | 40–55 | Very slow, solemn — the cathedral gate does not hurry |
| `creative_ideation` | Rubato | 60–160 | Free tempo — creativity follows no metronome |
| `spatial_reasoning` | Moderato | 85–110 | Measured, deliberate — spatial decomposition needs room |
| `synthesis` | Andante | 70–95 | Gentle, gathering — pull threads without rushing |
| `vision` | Moderato | 90–115 | Clear, forward-looking — steady walk to the horizon |
| `voice` | Adagio | 55–75 | Slow, warm — the spoken line arrives like a breath |

Tempo transitions between stages feed into the TempoMap (Layer 3) for pipeline breathing.

---

## Architecture

```
casting_call/
├── __init__.py          # Public API exports
├── atlas.py             # ModelAtlas, ModelProfile, VoiceCharacter enum
├── casting.py           # CastingDirector: cast, cast_pipeline, counterpoint
└── tempo_profiles.py    # Role → TempoProfile mapping (BPM ranges)
tests/
└── test_casting.py      # Test suite
```

### `ModelProfile` Schema

```python
@dataclass(frozen=True)
class ModelProfile:
    name: str                           # Unique identifier (e.g., "HERMES_405B")
    provider: str                       # Hosting provider
    voice_character: VoiceCharacter     # Keyboard analogy profile
    tempo_bpm: tuple[int, int]          # Natural BPM range (low, high)
    strengths: list[str]                # Capability tags
    weaknesses: list[str]               # Known limitations
    cost_per_1k_tokens: float           # USD (blended input+output estimate)
    failure_modes: str                  # How this model breaks
    channel: Optional[int] = None       # SWMIDI channel (None = not on bus)
    temperature: float = 0.7            # Default temperature for this model
```

### `ModelAtlas` Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `default()` | `ModelAtlas` | Canonical 13-model fleet |
| `get(name)` | `ModelProfile \| None` | Lookup by name |
| `all()` | `list[ModelProfile]` | All models |
| `by_strength(s)` | `list[ModelProfile]` | Models with a given strength tag |
| `by_tempo_range(lo, hi)` | `list[ModelProfile]` | Models overlapping BPM range |
| `cheapest(s)` | `ModelProfile \| None` | Lowest-cost model with a strength |

---

## Integration

The brain pipeline calls CastingDirector before each stage:

```python
# In brain.py
atlas = ModelAtlas.default()
director = CastingDirector(atlas)

intent_model = director.cast("intent_parse")       # → SEED_MINI
planner_model = director.cast("planning")           # → SEED_PRO
coder_model = director.cast("code_gen")             # → QWEN3_CODER
voice_model = director.cast("personality_wrap")     # → HERMES_405B
safety_model = director.cast("safety_check")        # → NEMOTRON_ULTRA
```

The processor's content safety stage uses `NEMOTRON_ULTRA` as a non-negotiable default — the safety verdict is mandatory regardless of what the atlas says about alternatives.

---

## Related Repositories

| Repository | Role |
|-----------|------|
| [lucineer-brain](../lucineer-brain) | Consumes casting decisions for pipeline execution |
| [lucineer-worker](../lucineer-worker) | Processor daemon invokes brain which invokes casting |
| [lucineer-system](../lucineer-system) | Roundtable documents analyze the fleet |

---

## License

MIT
