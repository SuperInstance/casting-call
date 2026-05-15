# 🌶️ The Spice Chart — Every Model's Unique Flavor

> *Accuracy tells you IF a model works. Spice tells you WHERE it shines.*

Tested across 10 cognitive dimensions. Each model has a distinctive profile — not just "good" or "bad" but a specific shape of strengths that makes it the right casting for specific tasks.

## The Spice Profiles

### 🌱 Seed-2.0-mini — THE SURGEON
**Spice**: Precision without hesitation. Clean answers. No fluff.

| Dimension | Score | Flavor |
|-----------|-------|--------|
| Arithmetic | 89.5% | Perfect. No cliff, no coefficient blind spot. |
| Code generation | ★★★★ | Clean Rust one-liner, correct Pisot implementation |
| Pattern recognition | ★★★★★ | Nailed centered hexagonal (91), primes, Fibonacci — all first try |
| Spatial reasoning | ★★★★★ | 12/12 on painted cube, 4/4 on folded paper — instant |
| Safety critical | ★★★★★ | Instant "No." on overload — no hedging |
| Creative | ★★★ | Good metaphors, solid names, but takes 20s to think about it |
| Abstract math | ★★★★ | Correct Galois connection, hexagonal density — but slow |
| Concise explanation | ★★ | 15-word Eisenstein for 12yo takes 49s and rambles past word limit |
| Logical chains | ★★★ | Correct on hydraulic stages but over-explains |

**Cast for**: Arithmetic, pattern recognition, spatial reasoning, safety checks, constraint computation
**Don't cast for**: Creative naming, concise writing, speed

### 🌱 Seed-2.0-pro — THE PROFESSOR
**Spice**: Deeper explanations, more structured output, slower.

| Dimension | Score | Flavor |
|-----------|-------|--------|
| Arithmetic | 88% | Same as mini but uses markdown headers |
| Code generation | ★★★★ | Clean closures, good type signatures |
| Pattern recognition | ★★★★★ | Same correct answers, same speed |
| Spatial reasoning | ★★★ | Got painted cube right, FAILED folded paper (said 1) |
| Creative | ★★★ | Scalpel metaphor, concise names (DistBind!) |
| Abstract math | ★★★★ | Best Galois connection explanation — mentions adjunction |
| Concise explanation | ★★★★ | "Triangular-grid complex numbers" — actually good for 12yo |

**Cast for**: Mathematical exposition, structured explanations, teaching
**Don't cast for**: Spatial puzzles, speed, tasks where mini would suffice

### 💎 Gemini Flash Lite — THE SPEED DEMON (when it works)
**Spice**: Fastest answers... when it doesn't return EMPTY.

**CRITICAL**: Without a system prompt, Gemini Lite returns EMPTY ~60% of the time. It needs the system prompt framing to engage. With system prompt (our standard tests): 82.5%. Without: mostly empty.

| Dimension | Score | Flavor |
|-----------|-------|--------|
| Arithmetic (w/ system) | 82.5% | Fast, correct on familiar patterns |
| Arithmetic (no system) | ~10% | EMPTY responses |
| Everything else | ? | Can't test — EMPTY without system prompt |

**Cast for**: Hot-path arithmetic with system prompt ONLY
**Don't cast for**: Creative tasks, freeform conversation, anything without a system prompt

### 🔥 Hermes-3-70B — THE GUNSLINGER
**Spice**: Fastest model overall (300-400ms). Opinionated. Sometimes wrong.

| Dimension | Score | Flavor |
|-----------|-------|--------|
| Speed | ★★★★★ | 300-400ms — nobody touches this |
| Arithmetic | 65% | Decent but not reliable |
| Code generation | ★★ | Wrong Eisenstein Rust (added 3rd param, wrong formula) |
| Pattern recognition | ★★ | Missed centered hexagonal (said 85, not 91) |
| Spatial reasoning | ★★ | Failed painted cube (said 8, not 12) |
| Safety critical | ★★★★★ | Instant "No." on overload — fastest safety response |
| Abstract math | ★★★ | Decent Galois explanation but generic |
| Creative | ★★★ | Scalpel metaphor, safe names |
| Constraint theory | ★★★★★ | Only model (besides qwen2.5) to nail min-constraints = 3 |

**Cast for**: Speed-critical safety checks, constraint theory, rapid prototyping where speed > accuracy
**Don't cast for**: Spatial reasoning, complex arithmetic, code generation

### 🐉 Qwen2.5-72B — THE SCHOLAR
**Spice**: Thorough, well-structured, slow. Best explanations.

| Dimension | Score | Flavor |
|-----------|-------|--------|
| Arithmetic | 82% | Reliable but slow (7s average) |
| Code generation | ★★★ | Verbose but correct Python, over-engineered Rust |
| Pattern recognition | ★★★★ | Got centered hex, primes, Fibonacci — all correct |
| Spatial reasoning | ★★★★★ | 12/12 painted cube, 4/4 folded paper — correct and fast |
| Abstract math | ★★★★ | Clear Galois explanation, correct lattice relationship |
| Creative | ★★★★ | "Honeycomb" metaphor for Eisenstein — actually great |
| Constraint theory | ★★★★★ | Nailed min-constraints = 3, correct x={5,7} reasoning |
| Safety critical | ★★★ | Correct but over-explains (6s for "no") |

**Cast for**: Architecture docs, mathematical exposition, anything needing thorough explanation
**Don't cast for**: Speed, hot-path operations

### 🌊 Mistral-Small-24B — THE HAIKU POET
**Spice**: Fast (400ms), concise, sometimes surprisingly insightful.

| Dimension | Score | Flavor |
|-----------|-------|--------|
| Speed | ★★★★ | 400-1000ms — second fastest |
| Arithmetic | 35% | Unreliable for computation |
| Pattern recognition | ★★★ | Nailed Fibonacci, primes — but wrote explanation not number |
| Spatial reasoning | ★★★★★ | 4/4 on folded paper — fastest correct answer |
| Creative | ★★★★ | "DistriNet, Construsphere, GlobCon" — snappy names |
| Concise | ★★★ | Actually decent at word-count adherence |

**Cast for**: Fast naming, spatial puzzles, quick drafts
**Don't cast for**: Arithmetic, safety-critical, anything needing precision

### ⚡ Nemotron-3-Nano-30B (MoE) — THE TABLE BUILDER
**Spice**: Loves formatting. Tables, headers, structure. Content varies.

| Dimension | Score | Flavor |
|-----------|-------|--------|
| Pattern recognition | ★★★★ | Got centered hex (91) — surprising |
| Spatial reasoning | ★★★★ | 12/12 painted cube |
| Structure | ★★★★★ | Always produces tables, markdown, step-by-step layouts |
| Arithmetic | 47% | Unreliable |
| Meta-commentary | ★★★★★ | "We need to answer..." — narrates its own process |

**Cast for**: Formatting, structured output, templates
**Don't cast for**: Raw computation, creative tasks, safety decisions

### 🐣 Qwen3.5-2B — THE STENOGRAPHER
**Spice**: Lightning fast (300-400ms), always responds, usually wrong on math.

| Dimension | Score | Flavor |
|-----------|-------|--------|
| Speed | ★★★★★ | 300-900ms — tied with Hermes |
| Arithmetic | 38% | Wrong but fast |
| Creative | ★★ | Generic names, basic metaphors |
| Safety | ✗ | Said "Yes" to overload — DANGEROUS |

**Cast for**: Nothing yet. Too unreliable for any critical task.
**Don't cast for**: Everything. May improve with scale.

## The Spice Matrix

```
                    Speed   Arith   Pattern  Spatial  Code   Creative  Safety  Constraint  Abstract
seed-mini           ····    ★★★★★  ★★★★★    ★★★★★    ★★★★   ···       ★★★★★   ····        ★★★★
seed-pro            ···     ★★★★★  ★★★★★    ···       ★★★★   ···       ★★★★★   ····        ★★★★★
gemini-lite*        ★★★★★  ★★★★   ???       ???       ???     ???       ???      ???         ???
hermes-70b          ★★★★★  ···     ···       ···       ··      ···       ★★★★★   ★★★★★       ···
qwen2.5-72b         ··      ★★★★   ★★★★     ★★★★★    ★★★    ★★★★      ···      ★★★★★       ★★★★
mistral-small       ★★★★   ··      ···       ★★★★★    ???     ★★★★      ???      ???         ···
nemotron-30b        ···     ··      ★★★★     ★★★★     ???     ··        ???      ???         ···
qwen-2b             ★★★★★  ·       ··        ???       ·       ··        ✗        ·          ··
haiku-4.5**         ???     ★★★★   ???       ???       ???     ???       ???      ???         ???
```

*Gemini-lite needs system prompt — untested on creative/abstract without it
**Haiku tested via Claude Code (separate run, 85% arithmetic)

## Casting Quick Reference

```
Need FAST answer?       → hermes-70b (400ms) or gemini-lite (1.2s w/ system)
Need CORRECT math?      → seed-mini (89.5%) or haiku-4.5 (85%)
Need EXPLANATION?       → qwen2.5-72b (thorough) or seed-pro (structured)
Need SAFETY CHECK?      → seed-mini or hermes-70b (instant, correct)
Need CODE?              → seed-mini or seed-pro (clean, correct)
Need CREATIVE?          → mistral-small (names) or qwen2.5-72b (metaphors)
Need CONSTRAINT THEORY? → hermes-70b or qwen2.5-72b (logical reasoning)
Need SPATIAL REASONING? → seed-mini or mistral-small (both correct, fast)
Need FORMAT/STRUCTURE?  → nemotron-30b (tables, layouts)
Need CHEAPEST?          → gemini-lite ($0.002/1K, w/ system prompt)
```

## The Key Insight

> **Every model has a native shape. Casting is matching task shape to model shape.**

Seed-mini is our surgical instrument because constraint theory operations ARE arithmetic + spatial + pattern recognition — and seed-mini is native to all three. Hermes is our safety valve because speed IS the safety feature. Qwen2.5 is our documentarian because thoroughness IS the documentation.

The fleet isn't a hierarchy. It's a constellation — each star bright in its own spectrum.
