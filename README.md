# casting-call

*The musician's ear that knows which keyboard sounds right for which song.*

Layer 8 of the Slackwater stack. The model routing brain. Pure data, pure functions, zero side effects.

## What It Does

**casting-call** maps a pipeline role ("parse this intent," "generate build code," "wrap personality around the output") to the right AI model. It consults a capability atlas — the accumulated wisdom of every model the fleet has run — and returns the best casting for the job.

Think of it as a bandleader reading the score and deciding who takes the solo.

## The Atlas

Every model is an instrument with a voice. The atlas knows what each one sounds like:

| Model | Voice | Tempo | Best At | Breaks When |
|-------|-------|-------|---------|-------------|
| Hermes-405B | Roland (warm) | Adagio 50–70 | Voice, lore, personality | Asked for structured output |
| Gemini Pro | Yamaha (bright) | Allegro 120+ | Synthesis, summary, vision | Depth is needed |
| Claude Opus | Kurzweil (deep) | Largo 40–60 | Architecture, hard reasoning | Budget is tight |
| Claude Sonnet | Kurzweil Jr | Moderato 90+ | Fast quality code | Depth matters less than Opus |
| Seed-mini | Analog synth | Allegro 120+ | Creative ideation, intent parse | Given a code task |
| Seed-pro | Analog synth Pro | Moderato 90–120 | Deep planning, decomposition | Time is short |
| Qwen3.6 | Versatile | Andante 80–100 | Logic, spatial reasoning | Creative voice needed |
| Qwen3-Coder | Precision | Andante 80–100 | Code generation | Context matters more than syntax |
| Nemotron Ultra | Pipe organ | Largo 40–60 | Safety, verification, convergence | Speed matters |
| GLM-5.2 | Versatile | Moderato 90+ | General intelligence | Specialization matters |
| Kimi K3 | Build intelligence | Allegro 100+ | Spatial decomposition | Narration needed |
| DeepSeek V3 | Cost-effective | Andante 70–90 | Quick code, fast iteration | Depth needed |
| MMX M3 | Creative firehose | Rubato | Media generation | Given logic or code |

## Usage

```python
from casting_call import ModelAtlas, CastingDirector

atlas = ModelAtlas.default()
director = CastingDirector(atlas)

# Cast a single role
profile = director.cast("intent_parse")
# → SEED_MINI (Allegro, analog synth, cheap and fast)

# Cast a full pipeline
roles = ["intent_parse", "planning", "code_gen", "personality_wrap", "safety_check"]
cast = director.cast_pipeline(roles)
# → [SEED_MINI, SEED_PRO, QWEN3_CODER, HERMES_405B, NEMOTRON_ULTRA]

# What's the tempo for this role?
director.tempo_range("safety_check")
# → (40, 55) — Largo. Safety does not hurry.

# What if we swapped Seed-mini for GLM-5.2 on intent?
director.what_if("intent_parse", "GLM_5_2")
# → {'feasible': True, 'cost_delta': +0.0003, 'tempo_delta': (-30, -25), ...}
```

## The Counterpoint Constraint

Two models never receive structurally identical prompts for the same stage. This is the "no parallel octaves" rule from species counterpoint: two voices singing the same note in the same rhythm wastes a voice. In the pipeline, giving two models the same prompt wastes compute.

The `counterpoint_check()` method catches this. Same model in adjacent pipeline stages = parallel octaves = fail. Same model in non-adjacent stages (e.g., Seed-mini does intent parsing and then later does creative ideation) is a recap — that's fine.

## Tempo × Model

Each model has a natural BPM range. The pipeline's tempo transitions are derived from who is playing, not hardcoded:

- Intent parsing: **Allegro** (120+ BPM) — Seed-mini, fast and expansive
- Planning: **Moderato** (90–110 BPM) — Seed-pro, measured and deliberate
- Code generation: **Andante** (80–100 BPM) — Qwen3-Coder, steady walking pace
- Personality wrap: **Adagio** (50–70 BPM) — Hermes, slow and expressive
- Safety check: **Largo** (40–55 BPM) — Nemotron, cathedral-scale solemnity

When the TempoMap (Layer 3) transitions between stages, it reads the model's natural tempo from the atlas. The pipeline breathes with the cast.

## Model Swaps

Swapping a model is a one-row change in the atlas, measured against the R2 trajectory set before commit. The `what_if()` method tells you the cost and tempo impact before you commit:

```python
# Can Nemotron Ultra handle intent parsing?
director.swap("intent_parse", "NEMOTRON_ULTRA")
# → False — pipe organ doesn't do Allegro
```

## Architecture

```
casting_call/
├── __init__.py          # Public API
├── atlas.py             # ModelAtlas + ModelProfile + VoiceCharacter
├── casting.py           # CastingDirector
└── tempo_profiles.py    # Role → BPM mapping
tests/
└── test_casting.py      # Comprehensive test suite
```

## In the Stack

Casting-call is Layer 8. It sits between the Perception layer (7) and the Brain Pipeline (9). The pipeline calls `cast()` before each stage to determine which model to invoke. The result includes the model name, temperature, and natural tempo — which feeds into the TempoMap's stage transition.

```
Layer 7: Perception  →  Layer 8: Casting-Call  →  Layer 9: Brain Pipeline
 (the ears)               (the routing brain)        (the performance)
```

## The Philosophy

The fleet is not the models. The fleet is the **casting**. No single model covers the space. The interlocking of different voices — fast and slow, precise and creative, warm and analytical — is what produces something better than any one model could produce alone. This is Penrose tiling applied to AI: no single tile covers the plane, but the interlocking of different shapes does.

Casting-call is the bandleader's ear. It knows which keyboard sounds right for which song.

## License

MIT
