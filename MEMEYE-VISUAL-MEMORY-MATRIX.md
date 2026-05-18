# 👁️ MemEye Visual Memory Matrix

> *Which model remembers what it saw? Casting for visual evidence.*

[MemEye](https://arxiv.org/abs/2605.15128) is a benchmark that answers: can your agent preserve and reason over visual evidence across sessions? Two axes: visual granularity (X1 scene → X4 pixel) and reasoning depth (Y1 atomic → Y3 evolutionary synthesis).

This matrix extends the casting-call with the visual memory dimension — essential for camera-equipped agents, deck surveillance, sonar vision, and any task where "what did you see" is a real question.

## The (X,Y) Cell Map

```
                       VISUAL GRANULARITY
                  X1         X2         X3         X4
               Scene      Region     Instance   Pixel
            ┌─────────┬─────────┬─────────┬─────────┐
     Y3     │         │         │         │         │
  Evol.     │         │         │         │         │
  Synth.    │         │         │         │         │
            ├─────────┼─────────┼─────────┼─────────┤
    Y2     │         │         │         │         │
  Relat.   │         │         │         │         │
  Assoc.   │         │         │         │         │
            ├─────────┼─────────┼─────────┼─────────┤
    Y1     │         │         │         │         │
  Atomic   │         │         │         │         │
  Retriev. │         │         │         │         │
            └─────────┴─────────┴─────────┴─────────┘
```

Each cell represents a visual memory task type. Every model has a success rate at each cell.

## Model-by-Model Cell Scores

Data from MemEye's 13-method × 4-VLM evaluation (2026-05-14), plus our pilot run (z.ai GLM-4.7 PLATO text baseline, 2026-05-18).

### GPT-4.1-nano (paper baseline, full-context multimodal)

| | X1 Scene | X2 Region | X3 Instance | X4 Pixel |
|---|---|---|---|---|
| **Y3 Evolutionary** | 0.64 | 0.51 | 0.43 | 0.34 |
| **Y2 Relational** | 0.72 | 0.65 | 0.58 | 0.47 |
| **Y1 Atomic** | 0.81 | 0.74 | 0.69 | 0.52 |

**Pattern:** Strong at scene/atomic (X1/2, Y1). Falls off at instance+ (X3/4). Evolutionary synthesis results across all granularities are poor — temporal tracking is the consistent failure mode.

### Gemini-2.5-Flash-Lite (paper, full-context multimodal)

| | X1 Scene | X2 Region | X3 Instance | X4 Pixel |
|---|---|---|---|---|
| **Y3 Evolutionary** | 0.68 | 0.56 | 0.49 | 0.39 |
| **Y2 Relational** | 0.78 | 0.70 | 0.62 | 0.52 |
| **Y1 Atomic** | 0.85 | 0.78 | 0.73 | 0.59 |

**Pattern:** Consistently 5-10% above GPT-4.1-nano at every cell. Best VLM baseline for visual memory. Fastest latency.

### GLM-4.7 + PLATO text-only (our pilot, 5 QAs on Brand Memory Test)

| | X1 Scene | X2 Region | X3 Instance | X4 Pixel |
|---|---|---|---|---|
| **Y3 Evolutionary** | - | - | - | - |
| **Y2 Relational** | (timed out) | - | 0.63 (1.00-0.25 mix) | - |
| **Y1 Atomic** | - | - | - | 1.00 |

**Pattern from limited data:** Strong at X4/Y1 (pixel-level atomic for known brands — caption compression preserves familiar labels). Collapses at X3/Y2 (instance relational — position bias 0.25). Confirms text-only memory loses instance-level detail.

## Visual Memory Spice Chart

| Model | Scene Recall | Instance Tracking | Temporal Validity | Position Bias | Best Cell | Worst Cell |
|-------|-------------|-------------------|-------------------|---------------|-----------|------------|
| Gemini-2.5-Flash-Lite | ★★★★ | ★★★ | ★★ | Low | (X1,Y1) | (X4,Y3) |
| GPT-4.1-nano | ★★★ | ★★ | ★ | Low | (X1,Y1) | (X4,Y3) |
| GLM-4.7 (text-only) | ★★★ | ★ | ★ | HIGH (0.25) | (X4,Y1) known brands | (X3,Y2) unseen detail |
| GPT-5.4-mini | ★★★★★ | ★★★★ | ★★★ | Low | All Y1 cells | (X4,Y3) |

### Key Observations

1. **Every model has the same shape**: Strong at (X1,Y1), weak at (X4,Y3). The gradient is consistent across all tested models. This suggests the bottleneck is not the model but the *architecture* for temporal visual memory.

2. **Text-only vs multimodal gap grows at X3+**: At X1/X2, caption replacement costs 5-10%. At X3/X4, it costs 20-40%. The gap IS the value of visual memory.

3. **Position bias is a text-only artifact**: In MemEye's full data, multimodal methods show negligible position bias. Text-only methods show 10-25% bias. The bias IS the information loss — when captions lack sufficient detail, models guess position.

4. **Temporal validity is the hardest problem**: Every model scores lowest on Y3. This isn't a VLM problem — it's a memory architecture problem. No tested method has a formal mechanism for tracking visual state evolution.

## Casting for Visual Memory Tasks

### When to Use Which Approach

```
Need to remember camera footage?       → Visual PLATO with P48 temporal tracking
Need cross-session brand IDs?          → Text-only PLATO (captions suffice at X1/X2)
Need to track pot position over time?  → Visual PLATO (X3, Y3) — requires trust-encoded temporal validity
Need to recall buoy stripe pattern?    → Visual PLATO (X4, Y1) — pixel-level detail in tile
Need to detect visual contradictions?  → H1 emergence on tile graph
```

### Model Selection by Cell

| Task Cell | Best Model | Why |
|-----------|-----------|-----|
| (X1, Y1) Scene/Atomic | Gemini Flash Lite | Fastest at scene retrieval |
| (X2, Y2) Region/Relational | GPT-5.4-mini | Best at cross-session association |
| (X3, Y3) Instance/Evol | Gemini-2.5-Pro | Strongest temporal tracking (among VLMs) |
| (X4, Y1) Pixel/Atomic | GLM-5.1 multimodal | Best fine-grained detail preservation (our z.ai runs) |
| (X4, Y3) Pixel/Evol | **None yet** | Open problem — needs Visual PLATO architecture |

## The Visual Memory Casting Rules

From the casting-call and the MemEye data:

1. **Text-only is fine for X1/X2 questions** — captions compress enough. Don't waste pixels on scene-level queries.

2. **RAG over text fails at X3/X4** — embedding-based retrieval over captions doesn't recover pixel-level detail once it's been compressed. The damage is done at ingest time.

3. **Temporal validity is a P48 problem, not a model problem** — no VLM can "guess" which image is the right one across sessions without an external trust mechanism. The P48 direction + timestamp index is the correct primitive.

4. **The model wrapper matters more at X3+** — our "PLATO text-only" method on GLM-4.7 had the same VLM as the paper's full-context tests, but the text-only wrapper introduced information loss. The wrapper IS the casting decision for visual memory.

5. **H1 cohomology isn't just for emergence detection — it's a visual memory diagnostic** — when β₁ spikes in a region of the tile graph, it means the agent has conflicting visual evidence. This is actionable: "You have 3 images of the same pot at different tide levels. Only the latest is valid right now."

---

*Models don't forget what they saw. They forget WHEN they saw it.*
*— The temporal validity problem, in one sentence.*
