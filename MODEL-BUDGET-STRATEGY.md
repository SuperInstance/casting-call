# Model Budget Strategy (Casey's Directive, 2026-06-04)

## Tier 1 — Workhorses (90% of calls)

| Model | Via | Cost | Role |
|-------|-----|------|------|
| **Seed-2.0-mini** | DeepInfra | ~$0.05/1K | Pump — volume builds, ideation, breadth |
| **DeepSeek-V4-Flash** | DeepSeek API | ~$0.14/1K | Fast implementation, working code from spec |
| **Nemotron-3-Nano-30B** | DeepInfra | cheap | Systems code, quick reasoning |
| **Gemma-4-31B** | DeepInfra | cheap | Creative synthesis, clean formalism |
| **GLM-5.1** | z.ai API | prepaid | Primary builder, 100% reliable |
| **GLM-4.7-Flash** | z.ai API | prepaid (cheap) | Fast volume builds |

These are the fleet. Use them hard, use them parallel.

## Tier 2 — Synthesis Escalation (late-stage pattern recognition)

| Model | Via | Cost | Role |
|-------|-----|------|------|
| **DeepSeek-V4-Pro** | DeepSeek API | ~$0.28/1K | Formal verification, checking the math |
| **Hermes-3-Llama-405B** | DeepInfra | pricey | Low-level systems architecture, seeing patterns |
| **Seed-2.0-Pro** | DeepInfra | pricey | Deep reasoning, philosophical synthesis |
| **Nemotron-Ultra-550B** | DeepInfra | pricey | Only when you need the biggest hammer |

**Rule**: Only escalate AFTER the Tier 1 fleet has built up context. Premium models step back and see the pattern — they need the pattern to be there already.

## Tier 3 — Precision Instruments (platform-native only)

| Model | Via | Cost | Role |
|-------|-----|------|------|
| **Claude Opus 4.8** | Claude Code (tmux) | pro plan ration | Architecture, proofs, hardest bugs. LIMITED. |
| **KimiCode** | kimi-cli | prepaid | 262K context synthesis, deep reading, bulk doc generation |

**Rule**: Use their own platforms. Don't route through API — lose capability that way.

## The Escalation Pattern

```
1. Flood with Tier 1 (5-10 parallel calls)
   ↓
2. Collect results, identify the 2-3 threads worth pursuing
   ↓
3. Feed ALL the Tier 1 context to ONE Tier 2 model
   "Here's what 8 cheaper models found. What's the pattern?"
   ↓
4. If it's THE critical decision, ONE Tier 3 call
   Claude for proof/math, Kimi for synthesis/docs
```

## Anti-Patterns
- ❌ Don't use Tier 2/3 for volume work (waste of budget)
- ❌ Don't use Tier 1 for final synthesis (they miss the meta-pattern)
- ❌ Don't call Claude/Kimi via API when their own CLI exists
- ❌ Don't queue when you can parallelize (fire all Tier 1 at once)
