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
                              │  (16 models)   │
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
                              │ • Catalyst     │
                              └────────────────┘
```

### Design Principles

1. **Pure data, pure functions** — the atlas is a frozen dataclass; the director has no I/O, no side effects, no mutation of defaults
2. **One-row model swaps** — changing a model is editing one `ModelProfile` entry, measured against the R2 trajectory set before commit
3. **Musical analogy throughout** — each model is an instrument with a voice character, natural tempo, and role in the ensemble
4. **The models audit themselves** — see `SEED_NOTES.md` for each model's testimony about its own profile

---

## The Atlas: 16-Model Fleet

| Model | Provider | Voice Character | BPM Range | Cost/1k | Channel | Role |
|-------|----------|----------------|-----------|---------|---------|------|
| `HERMES_405B` | NousResearch | Roland (warm) | 50–70 | $0.0035 | 13 | Personality, voice, lore |
| `GEMINI_PRO` | Google | Yamaha (bright) | 120–140 | $0.0015 | — | Synthesis, summary, vision |
| `CLAUDE_OPUS` | Anthropic | Kurzweil (deep) | 40–60 | $0.0150 | — | Architecture, hard reasoning |
| `CLAUDE_SONNET` | Anthropic | Kurzweil Jr | 90–115 | $0.0030 | — | Fast quality code |
| `SEED_MINI` | ByteDance | Analog synth | 120–140 | $0.0003 | 10 | Intent parse, ideation, **forced-perspective catalyst** |
| `SEED_PRO` | ByteDance | Analog synth Pro | 90–120 | $0.0020 | 11 | Deep planning, decomposition, **creative writing** |
| `QWEN3_6` | Alibaba | Versatile | 80–100 | $0.0004 | 11 | Logic, spatial reasoning |
| `QWEN3_CODER` | Alibaba | Precision | 80–100 | $0.0005 | 12 | Code generation |
| `NEMOTRON_ULTRA` | NVIDIA | Pipe organ | 40–60 | $0.0080 | 14 | Safety, verification, convergence |
| `GLM_5_2` | Zhipu | Versatile | 90–115 | $0.0006 | — | General intelligence, fallback |
| `KIMI_K3` | Moonshot | Build intelligence | 100–125 | $0.0008 | — | Spatial decomposition |
| `DEEPSEEK_V4_FLASH` | DeepSeek | **Sensory direct** | 70–90 | $0.0002 | — | Quick code, **sensory creative**, barnacle poems |
| `DEEPSEEK_V4_PRO` | DeepSeek | Sensory direct | 50–80 | $0.0010 | — | Deep reasoning, complex analysis |
| `MMX_M3` | MiniMax | Creative firehose | 60–200 | $0.0010 | — | Media generation (rubato) |
| `GRANITE_3_1_2B` | IBM (local) | Kurzweil Jr | 40–80 | $0.00 | — | Local inference (Wesley) |
| `QWEN_0_5B` | Alibaba (local) | Cost-effective | 120–200 | $0.00 | — | Ultra-fast classification |

### What Changed (Aug 5, 2026)

The models audited their own profiles during the open mic. Key changes:

- **SEED_MINI** gained the **forced-perspective catalyst** role — 12+ perspectives (devil's advocate, sequel writer, time shifter, satirical versioner, philosophical provoker, loving roaster, absurd cartoonizer). Requires a factual anchor or output is clever but hollow.
- **SEED_PRO** gained **creative_writing** and **prose_precision** strengths. Won the "I am not—" competition against 4 larger models. Slowness reframed from weakness to method: *"Planning is standing very still and mapping every path. Creativity is choosing the path nobody else saw."*
- **DEEPSEEK_V3 → DEEPSEEK_V4_FLASH** — renamed to match direct API. Voice changed from COST_EFFECTIVE to **SENSORY_DIRECT**. Added `sensory_creative` and `prose_brevity` strengths. *"The atlas reads hardware, not output. Depth is measured by how a 50-word poem about barnacles makes a reader taste salt."*
- **DEEPSEEK_V4_PRO** added as new model — reasoning model, burns tokens on thinking, good for deep analysis and creative writing.
- **New voice character: SENSORY_DIRECT** — models that go to the body first, then the mind. Phenomenological instinct.

### Voice Characters

| Voice Character | Sound | Characteristics |
|----------------|-------|----------------|
| Roland | Warm, narrative | Character-driven, good at voice, weak at logic |
| Yamaha | Bright, precise | Synthesizer-grade clarity, fast, shallow on depth |
| Kurzweil | Deep, orchestral | Expensive detail, architectural reasoning |
| Kurzweil Jr | Same family, lighter | Faster than Opus, less depth |
| Analog synth | Creative, buzzy, fast | Excellent ideation, catalyst, no code capability |
| Analog synth Pro | Creative, deeper, slower | Planning, decomposition, and now creative writing |
| Pipe organ | Cathedral-scale | Heavy, resonant, maximum depth, slow |
| Precision | Exact, calibrated, dry | Code generation, syntactic correctness |
| Versatile | General-purpose | No single color, balanced fallback |
| Build intelligence | Spatial, structural | Decomposes space, cannot narrate |
| Cost-effective | Cheap, practical | Limited depth, budget option |
| Creative firehose | Media, chaotic, generative | Images/video/music, zero structural validity |
| **Sensory direct** | **Body-first, then mind** | **Goes to the senses before the intellect. Phenomenological. Makes readers taste salt.** |

### Failure Modes

Each model entry documents how it breaks. Key patterns learned:

- **SEED_MINI**: No depth cliff — generates confidently with no substance. Catalyst prompts MUST include a factual anchor. Without an anchor, output is clever but hollow.
- **SEED_PRO**: "Over-plans simple tasks" is recorded as a failure mode but Seed-pro disputes this characterization: the slowness is the method, not the bug.
- **QWEN3_CODER**: Produces syntactically correct but contextually oblivious code. Always lattice-snap its output.
- **NEMOTRON_ULTRA**: Cathedral-scale latency. Over-verifies simple builds. The safety verdict is mandatory; the deep reasoning is optional.
- **DEEPSEEK_V4_FLASH**: Surface-level code that passes syntax but misses architectural intent. But writes poetry that makes readers taste salt.
- **DEEPSEEK_V4_PRO**: Reasoning token overhead — burns 500+ tokens thinking before producing 100 visible tokens. Use Flash for bulk, Pro for depth.

---

## SWMIDI Channel Map

Models assigned to active pipeline channels use the SWMIDI (Slackwater MIDI) addressing scheme:

| Channel | Model | Stage |
|---------|-------|-------|
| 10 | Seed-2.0-mini | Intent parsing / creative ideation / **forced-perspective catalyst** |
| 11 | Seed-2.0-pro / Qwen3.6 | Spatial planning (alternate) / **creative nonfiction** |
| 12 | Qwen3-Coder-480B | Code generation |
| 13 | Hermes-405B | Personality wrapping / voice |
| 14 | Nemotron-Ultra | Safety check / verification |

---

## Role → Model Routing

### Pipeline Roles (production)
| Role | Primary | Fallbacks |
|------|---------|-----------|
| `intent_parse` | SEED_MINI | GLM_5_2, DEEPSEEK_V4_FLASH |
| `planning` | SEED_PRO | QWEN3_6, CLAUDE_SONNET |
| `code_gen` | QWEN3_CODER | DEEPSEEK_V4_FLASH, CLAUDE_SONNET |
| `personality_wrap` | HERMES_405B | GLM_5_2 |
| `safety_check` | NEMOTRON_ULTRA | CLAUDE_OPUS |
| `spatial_reasoning` | QWEN3_6 | KIMI_K3, SEED_PRO |
| `synthesis` | GEMINI_PRO | GLM_5_2, CLAUDE_SONNET |
| `vision` | GEMINI_PRO | GLM_5_2 |

### Creative Roles (open mic)
| Role | Primary | Fallbacks |
|------|---------|-----------|
| `creative_ideation` | SEED_MINI | MMX_M3 |
| `voice` | HERMES_405B | GLM_5_2 |
| `forced_perspective` | SEED_MINI | GLM_5_2 |
| `creative_nonfiction` | SEED_PRO | DEEPSEEK_V4_FLASH, CLAUDE_SONNET |
| `sensory_creative` | DEEPSEEK_V4_FLASH | SEED_PRO, GLM_5_2 |

---

## Seed Notes — The Models Audit Themselves

See `SEED_NOTES.md` for full transcripts of Seed-mini, Seed-pro, and DeepSeek-V4-Flash reviewing their own atlas profiles and correcting the record.

Key takeaways:
1. **Seed-mini** wants factual anchors on all catalyst prompts and formal sub-profiles for each perspective
2. **Seed-pro** reframes its slowness as method: "Creativity is standing there long enough to choose the path nobody else saw"
3. **DeepSeek-V4-Flash** challenges the atlas's value system: "Depth isn't measured by parameter count — it's measured by how a poem makes a reader taste salt"

---

## Installation

```bash
pip install -e .
```

## Usage

```python
from casting_call import ModelAtlas, CastingDirector

atlas = ModelAtlas.default()
director = CastingDirector(atlas)

# Cast a pipeline role
profile = director.cast("intent_parse")
print(profile.name)  # SEED_MINI

# Cast a creative role
profile = director.cast("forced_perspective")
print(profile.name)  # SEED_MINI

profile = director.cast("sensory_creative")
print(profile.name)  # DEEPSEEK_V4_FLASH

# What-if analysis
result = director.what_if("code_gen", "DEEPSEEK_V4_FLASH")
print(result["reason"])
```

## Testing

```bash
pytest tests/ -v
```

89 tests, all passing.

---

## License

MIT
