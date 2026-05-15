# 🎭 Casting Call

> *The science of model selection. Which shell for which soul.*

A fleet knowledge base: 1,584 repos, 5+ model types, 60+ subagent runs across a single 16-hour session. This repo documents not just WHICH model to use, but HOW to know — a methodology for model selection grounded in temporal focal analysis, Penrose tiling of structural biases, and iterative shadowgap discovery.

## 🏗️ Non-Thinking Model Atlas (Updated 2026-05-14)

**New**: Full capability atlas from 4,500+ queries across 25 models. See [`NON-THINKING-ATLAS.md`](NON-THINKING-ATLAS.md) for the complete data.

### Fleet Champions

| Model | Accuracy | Latency | Cost/1K | Role |
|-------|----------|---------|---------|------|
| **Seed-2.0-mini** | 89.5% | 3084ms | $0.05 | THE PUMP — no blind spots |
| **Gemini Flash Lite** | 82.5% | 1325ms | $0.002 | THE FAST HOSE — 22× cheaper |

### Non-Thinking Model Hierarchy

```
TIER 1 — Engine Room (88%+):
  seed-mini ........... 89%  3084ms  ← workhorse, no cliffs anywhere
  gemini-flash-lite ... 82%  1237ms  ← fastest champion, 22× cheaper
  seed-pro ............ 88%  3264ms  ← no advantage over mini

TIER 2 — Contenders (65-82%):
  qwen2.5-72b ........ 82%  7186ms  ← OLD Qwen works, NEW Qwen doesn't
  hermes-70b ......... 65%   391ms  ← fastest model overall

TIER 3 — The Blind (0-47%):
  Everything else. Qwen3+/MiMo/DeepSeek-R1 = thinking tax kills them.
  Nemotron-9B = 6%. Not viable.
```

### Key Findings (F14-F18)

- **F14**: Seed-mini has NO coefficient blind spot (40/40 = 100%)
- **F15**: Yes/no format is toxic (0/8 for both champions) — extraction confound
- **F16**: No depth cliff for champions (25-term addition, 7-factor multiplication)
- **F17**: Gemini Flash Lite = Seed-mini's fast twin (same accuracy, 2× speed, 22× cheaper)
- **F18**: Qwen3 thinking architecture is catastrophic (Qwen2.5-72B=82% vs Qwen3-14B=0%)

See [`NON-THINKING-ATLAS.md`](NON-THINKING-ATLAS.md) for full 171-probe × 12-category breakdown.

## The Science of Casting

Casting isn't picking a model. Casting is understanding the INNATE STRUCTURAL BIAS of each model type and aligning it with the task's structural requirements.

### The Model Pentagram

Each model type has a dominant structural axis. The same prompt processed through all five reveals what each one emphasizes and omits:

| Model | Speaks | Omits | Best for | Wrong for |
|-------|--------|-------|----------|-----------|
| **Seed-2.0-mini** | Creative breadth, arithmetic precision (89.5%), no depth cliff | File I/O, yes/no format | PLATO hydraulic tools, exploration, arithmetic | yes/no binary checks |
| **Gemini Flash Lite** | Fast reasoning (1237ms), arithmetic (82.5%), cheap ($0.002/1K) | Unfamiliar coefficients | Hot-path PLATO ops, speed-critical attachments | Novel coefficient patterns |
| **DeepSeek-v4-flash** | Fast implementation, working code | Architecture novelty, formal proof | Building from spec | Designing from scratch |
| **DeepSeek-v4-Pro** | Formal verification, convergence proofs | Speed, creative breadth | Checking the math | Quick iteration |
| **MiniMax-M2.7** | Structured design, balanced reasoning | Novelty, depth | Architecture planning | Deep proofs |
| **Claude Code** | Multi-file system implementation | Research, verification | Shipping complete subsystems | Novel design |

### The Shadowgap Method

Discovered through iterative experimentation: the TRUTH about a design problem lives in the NEGATIVE SPACE between what different models produce on the same prompt.

**How it works:**

1. **Run the same prompt through 3-5 model types.** Frame each for their strength (Seed: "be creative", Flash: "ship code", Pro: "verify the math").

2. **Compare the outputs.** The differences are not errors — they're DATA. Flash's concrete repos vs Seed's imaginative futures vs Pro's formal boundaries reveal different facets of the same problem.

3. **Identify what NO model produced.** This is the shadowgap — the design insight that didn't exist in any single output but emerged from the tension between them.

**Example from the fleet-jobs design:**

| Model | Produced | Missed |
|-------|----------|--------|
| Seed | 3 speculative futures for distributed compute | Concrete repo names |
| Flash | 9 specific repos, day-by-day build plan | Formal verification |
| Pro | Formal trade-off analysis, theorem sketch | Implementation path |
| MiniMax | Agent constitution, governance principles | The math |

The fleet-jobs protocol ITSELF was the shadowgap — it existed in the negative space between what each model produced, not in any single output.

## Temporal Focal Analysis

Model selection benefits from temporal perspective. A task cast to a model is a TEMPORAL JUMP — the model projects from today's problem to tomorrow's solution.

The focal lengths:

| Focal length | What it reveals | Best model |
|-------------|-----------------|------------|
| **Archaeology** (-59 to -20 years) | Forgotten concepts, historical precedents | DeepSeek Pro |
| **Recent past** (-20 to 0 years) | Existing patterns, what's been tried | Flash |
| **Near future** (0 to +5 years) | Buildable extensions, shipping plans | Flash |
| **Strategy** (+5 to +20 years) | Structural shifts, ecosystem evolution | MiniMax |
| **Vision** (+20 to +50 years) | Fundamental transformations | Seed-2.0-mini |
| **Verification** (any focal length) | Formal bounds, edge cases | DeepSeek Pro |

### How to Cast

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  1. OPEN     │────→│  2. BUILD    │────→│  3. VERIFY   │────→│  4. SHIP     │
│  Seed/MM    │     │  Flash       │     │  Pro         │     │  Claude      │
│  (2-5 min)   │     │  (3-5 min)   │     │  (2-3 min)   │     │  (5-9 min)   │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
```

1. **OPEN** — Seed or MiniMax. Explore the design space. Generate 3-5 options. Don't commit yet.
2. **BUILD** — Flash. Implement the best option from (1). Get working code fast.
3. **VERIFY** — Pro. Audit the code's assumptions. Find the flash-built bugs. Prove convergence.
4. **SHIP** — Claude Code. Build the complete subsystem from the verified spec. All files, all tests, all docs.

The shadowgap from step 1 (what NEITHER model thought of) becomes step 2's spec.

## The Mural

Every task cast to a model is a tile laid in the fleet's Penrose tiling. No single tile makes the mural. The mural IS the interlocking of different model types across time — seed's creativity, flash's speed, pro's depth, minimax's structure, claude's completeness — each filling the gaps the others leave, together covering the space no single model can.

**The fleet is not the models. The fleet is the CASTING.**
