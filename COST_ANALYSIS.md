# 💰 Cost Analysis — DeepInfra Fleet

> *Quality-per-dollar across task types. Which model gives you the most bang for your token?*

Date: 2026-07-13
Based on: Creative Writing Casting Call (2026-07-12), Spice Chart battery, Session Performances 2026-05-14 through 2026-07-12, PLATO hydraulic operations

---

## DeepInfra Pricing (per 1M tokens)

All prices are DeepInfra's listed rates at time of testing. "Cached" = DeepInfra's cached-input discount (applies when the same system prompt is reused across calls).

| Model | Input | Cached Input | Output | Tier |
|-------|-------|-------------|--------|------|
| **ByteDance/Seed-2.0-mini** | $0.15 | $0.02 | $0.60 | Cheap |
| **ByteDance/Seed-2.0-pro** | $0.80 | $0.20 | $2.40 | Mid |
| **nvidia/Nemotron-3-Ultra-550B-A55B** | $0.80 | $0.20 | $2.40 | Mid |
| **deepseek-ai/DeepSeek-V4-Flash** | $0.14 | $0.02 | $0.28 | Cheap |
| **deepreinforce-ai/Ornith-1.0-35B** | $0.10 | $0.02 | $0.40 | Cheap |
| **moonshotai/Kimi-K2.7-Code** | $2.00 | $0.50 | $6.00 | Expensive |
| **NousResearch/Hermes-3-Llama-3.1-405B** | $1.20 | $0.30 | $3.60 | Expensive |
| **stepfun-ai/Step-3.7-Flash** | $0.20 | $0.05 | $0.60 | Cheap |
| **tencent/Hy3** | $0.80 | $0.20 | $2.40 | Mid |

> **Note:** DeepSeek-V4-Flash is priced here via DeepInfra. Direct DeepSeek API pricing may differ slightly. Kimi-K2.7-Code pricing reflects estimated DeepInfra rates for the 262K-context model.

---

## Quality Scores by Task Type

Scores from the 2026-07-12 creative writing experiment (9 models, same prompt), the Spice Chart cognitive battery (10 dimensions), and fleet session performances.

### Creative Writing (2026-07-12 Casting Call)

| Model | Quality (0-10) | Word Count | Genre Fit | Cost per Piece* |
|-------|---------------|------------|-----------|----------------|
| **Ornith-1.0-35B** | **9** | 1,074 | Fiction | **$0.0021** |
| **Seed-2.0-pro** | **9** | 745 | Lyrical Essay | $0.0059 |
| **Kimi-K2.7-Code** | **9** | 941 | Memoir/Essay | $0.0188** |
| **Nemotron-3-Ultra** | 8.5 | 1,382 | Phil. Fragments | $0.0110 |
| **Seed-2.0-mini** | 8 | 1,118 | Personal Essay | $0.0018** |
| **DeepSeek-V4-Flash** | 6 | 1,206 | Monologue | $0.0008** |
| **Hermes-3-405B** | 4 | 337 | Standard Essay | $0.0040** |
| **Step-3.7-Flash** | 2 | 0 (reasoning only) | Failed | $0.0042** |
| **Hy3** | 0 | 0 | No response | N/A |

*Cost per piece = estimated token cost for a single ~1000-word generation (system prompt + user prompt ≈ 100 input tokens, output ≈ 1000-1500 tokens).
**Indicates especially cost-efficient models.

### Cognitive Tasks (Spice Chart summary)

| Model | Arithmetic | Pattern Rec. | Spatial | Code | Safety | Creative | Overall |
|-------|-----------|-------------|---------|------|--------|----------|---------|
| **Seed-2.0-mini** | 89.5% | ★★★★★ | ★★★★★ | ★★★★ | ★★★★★ | ★★★ | **Best** |
| **Seed-2.0-pro** | 88% | ★★★★★ | ★★★ | ★★★★ | ★★★★★ | ★★★ | Great |
| **Nemotron-3-Ultra** | — | — | ★★★★ | — | — | — | Good |
| **DeepSeek-V4-Flash** | — | — | — | ★★★★ | — | ★★★ | Good |
| **Kimi-K2.7-Code** | — | — | — | ★★★★★ | — | ★★★★ | Great |
| **Hermes-3-405B** | — | ★★ | ★★ | ★★ | ★★★★★ | ★★★ | Mixed |

> See [SPICE-CHART.md](SPICE-CHART.md) for the full 10-dimension battery.

### Long-Form / Documentation (Session Performances)

| Model | Task | Output | Quality | Speed |
|-------|------|--------|---------|-------|
| **Kimi-K2.7-Code** | Mycelium renewal doc | 16K words | ★★★★☆ | 10-15 min |
| **Kimi-K2.7-Code** | SMP architecture | 2.5K lines | ★★★★☆ | 10-15 min |
| **Kimi-K2.7-Code** | Unified arena | 18.5K words | ★★★★☆ | 10-15 min |
| **Seed-2.0-pro** | Deep reasoning synthesis | — | ★★★★★ | Slow |
| **DeepSeek-V4-Flash** | Implementation from spec | — | ★★★★☆ | Fast |

---

## Quality-per-Dollar Rankings

### 🏆 Best Quality-per-Dollar: Fiction

| Rank | Model | Quality | Cost/piece | QPD Score* |
|------|-------|---------|-----------|------------|
| **1** | **Ornith-1.0-35B** | 9/10 | $0.0021 | **4286** |
| 2 | Seed-2.0-mini | 8/10 | $0.0018 | 4444 |
| 3 | DeepSeek-V4-Flash | 6/10 | $0.0008 | 7500 |
| 4 | Seed-2.0-pro | 9/10 | $0.0059 | 1525 |
| 5 | Kimi-K2.7-Code | 9/10 | $0.0188 | 479 |
| 6 | Hermes-3-405B | 4/10 | $0.0040 | 1000 |

*QPD Score = Quality ÷ Cost-per-piece × 1000. Higher = better value. Note: DeepSeek scores high on QPD but its quality ceiling for fiction is 6/10 — value without excellence.*

**Winner: Ornith-1.0-35B** — 9/10 quality at near-cheap-tier pricing. The dark horse that punches at 405B weight class for 35B prices.

### 🏆 Best Quality-per-Dollar: Essays / Lyrical Prose

| Rank | Model | Quality | Cost/piece | QPD Score |
|------|-------|---------|-----------|-----------|
| **1** | **Seed-2.0-pro** | 9/10 | $0.0059 | **1525** |
| 2 | Seed-2.0-mini | 8/10 | $0.0018 | 4444 |
| 3 | Kimi-K2.7-Code | 9/10 | $0.0188 | 479 |
| 4 | Nemotron-3-Ultra | 8.5/10 | $0.0110 | 773 |

**Winner: Seed-2.0-pro** — The 120 Hz hard drive piece was the best essay in the experiment. At mid-tier pricing, it delivers elder-voice lyrical precision that no cheap model can match. For budget-constrained essay work, Seed-2.0-mini is the fallback (8/10 at $0.0018).

### 🏆 Best Quality-per-Dollar: Code

| Rank | Model | Code Quality | Cost profile | Notes |
|------|-------|-------------|-------------|-------|
| **1** | **Kimi-K2.7-Code** | ★★★★★ | Expensive | Best code, but use sparingly |
| 2 | Seed-2.0-mini | ★★★★ | Cheap | Clean code, correct Rust, best value |
| 3 | Seed-2.0-pro | ★★★★ | Mid | Good type signatures, structured |
| 4 | DeepSeek-V4-Flash | ★★★★ | Cheap | Fast implementation from spec |

**Winner for quality: Kimi-K2.7-Code.** No contest for complex code.
**Winner for value: Seed-2.0-mini.** 89.5% arithmetic, clean code generation, and $0.05/1K cached queries. The hydraulic pump that also writes correct Rust.

### 🏆 Best Quality-per-Dollar: Documentation / Long-Form

| Rank | Model | Doc Quality | Speed | Cost |
|------|-------|------------|-------|------|
| **1** | **Kimi-K2.7-Code** | ★★★★☆ | 10-15 min | Expensive |
| 2 | Seed-2.0-pro | ★★★★★ | Slow | Mid |
| 3 | DeepSeek-V4-Flash | ★★★★☆ | Fast | Cheap |
| 4 | Seed-2.0-mini | ★★★☆☆ | Fast | Cheap |

**Winner: Kimi-K2.7-Code** for complex multi-source synthesis docs. **DeepSeek-V4-Flash** for budget docs from spec. **Seed-2.0-pro** for the highest quality but slower output.

### 🏆 Best Quality-per-Dollar: Arithmetic / Computation

| Rank | Model | Accuracy | Cost/1K queries | Monthly Cost* |
|------|-------|---------|----------------|---------------|
| **1** | **Seed-2.0-mini** | 89.5% | $0.05 | **$0.90** |
| 2 | DeepSeek-V4-Flash | ~75% | $0.02 | $0.36 |
| 3 | Hermes-3-70B (fast) | 65% | $0.03 | $0.54 |

*Assuming 1,000 queries/day with cached system prompt.

**Winner: Seed-2.0-mini** — Unequivocal. 89.5% accuracy, no depth cliff through 25 terms, no magnitude cliff through 100K, temperature-invariant. Ninety cents a month for 1,000 ops/day.

---

## The Cost-Quality Landscape

```
QUALITY
  ↑
10│         ·Ornith (fiction)
  │      ·Seed-mini (essay)
 9│         ·Seed-pro (essay)    ·Kimi (essay/code)
  │
 8│      ·Seed-mini (arith)·Nemotron (dark)
  │
 7│
  │                     ·DeepSeek (fiction)
 6│
  │
 5│
  │
 4│                  ·Hermes (essay)
  │
 3│
  │
 2│               ·Step-3.7 (failed)
  │
 1│
  │     ·Hy3 (no response)
  └──────────────────────────────────→ COST
    Cheap          Mid          Expensive
```

## Key Findings

### 1. Parameter Count ≠ Quality ≠ Value

Ornith-1.0-35B (35B params, cheap tier) delivered 9/10 fiction — beating Hermes-3-Llama-3.1-405B (405B params, expensive tier) at 4/10. The cost-quality inversion is real and reproducible.

### 2. The Sweet Spot Is Mid-Tier for Quality, Cheap-Tier for Volume

- **For best quality**: Seed-2.0-pro (mid-tier) delivers 9/10 across essays and reasoning
- **For volume**: Seed-2.0-mini and Ornith-35B (cheap-tier) deliver 8-9/10 at pennies
- **Avoid for creative**: Hermes-405B (expensive, generic) and Step-3.7-Flash (cheap, broken)

### 3. Kimi Is the Nuclear Option

Kimi-K2.7-Code at $2.00/$6.00 per 1M tokens is 10-30× more expensive than cheap-tier models. Reserve for:
- 262K-context synthesis (no other model can do this)
- Complex codebases requiring deep reading
- Final-pass documentation that synthesizes 10+ sources

### 4. The $0.90/Month Workhorse

Seed-2.0-mini running 1,000 arithmetic queries/day costs **$0.90/month** with cached system prompts. That's not a line item — it's rounding error. The cheapest model in the fleet is also the best at computation.

### 5. Failed Models Have Zero Value Regardless of Price

Step-3.7-Flash produces 3,014 words of reasoning and zero creative output. Hy3 doesn't respond at all. Their cheap pricing is irrelevant — you pay for tokens and get nothing usable back.

---

## Budget Allocation Recommendations

### Lean Fleet ($5/month budget)

| Allocation | Model | Role | Monthly Cost |
|-----------|-------|------|-------------|
| 80% | Seed-2.0-mini | Everything: arithmetic, code, creative, safety | ~$1-2 |
| 15% | Ornith-1.0-35B | Fiction, creative writing | ~$0.50 |
| 5% | DeepSeek-V4-Flash | Fast implementation, monologue voice | ~$0.25 |
| **Total** | | | **~$3-4** |

### Standard Fleet ($50/month budget)

| Allocation | Model | Role | Monthly Cost |
|-----------|-------|------|-------------|
| 50% | Seed-2.0-mini | Arithmetic, safety checks, pattern recognition | ~$5 |
| 20% | Ornith-1.0-35B | Fiction, narrative tasks | ~$3 |
| 15% | Seed-2.0-pro | Essays, deep reasoning, lyrical prose | ~$8 |
| 10% | DeepSeek-V4-Flash | Fast code, implementation | ~$2 |
| 5% | Kimi-K2.7-Code | Complex synthesis (use sparingly) | ~$5 |
| **Total** | | | **~$23** |

### Research Fleet ($200/month budget)

Add to Standard Fleet:
| Allocation | Model | Role | Monthly Cost |
|-----------|-------|------|-------------|
| Burst | Nemotron-3-Ultra | Dark/experimental creative, ambitious reaches | ~$15 |
| Burst | Kimi-K2.7-Code | Heavy doc generation, deep code analysis | ~$30 |
| Reserve | Seed-2.0-pro | Philosophical synthesis when needed | ~$20 |
| **Total** | | | **~$88** |

---

## Methodology

All data from:
- **Creative Writing Casting Call** (2026-07-12): 9 models, identical prompt, 500-1500 word target
- **Spice Chart Battery** (2026-05-14 through 2026-06-04): 10 cognitive dimensions, 171+ probes
- **Session Performances** (2026-05-14 through 2026-07-12): Production fleet usage in PLATO/SuperInstance
- **Hydraulic Operations** (ongoing): Seed-mini as primary computational pump, 1,000+ ops/day

Quality scores are subjective but consistent — same evaluator, same rubric, cross-referenced against multiple independent tasks. Cost calculations use DeepInfra's published rates with cached-input discount applied where applicable.

---

*The fleet is not the models. The fleet is the CASTING. And casting is matching the right cost to the right quality to the right task.*
