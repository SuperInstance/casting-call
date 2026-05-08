# README Cross-Pollination & Coding Fallback — 2026-05-08

> Testing mid-tier models as coding subagent fallbacks when premium models (z.ai, kimi) are unavailable

## Experiment Design

- **Goal:** Identify reliable mid-tier coding subagents for fleet work when premium models hit rate limits
- **Method:** Spawn subagents using Nemotron-30B and Hermes-405B via DeepInfra for real fleet tasks
- **Tasks:** README updates across 10 repos, voice critique, landing page rewrites

## Results

### Nemotron-30B (nvidia/Nemotron-3-Nano-30B-A3B)

| Task | Result | Quality | Time |
|------|--------|---------|------|
| README updates (10 repos) | 9/10 success | Good (3.5/5) | 5-10 min/repo |
| Voice critique | Success | Nuanced (3.5/5 creative, 4/5 technical) | ~5 min |
| Landing page rewrite | Success | Competent | ~7 min |

**Strengths:**
- Consistent technical accuracy (4/5)
- Good at structured tasks (README, documentation)
- Reasonable token budget (~5-7 min for medium tasks)
- Via DeepInfra = cheap

**Weaknesses:**
- Creative voice work is competent but not exceptional
- One formatting error in 10 repos (minor)
- Not a replacement for premium models on complex tasks

### Hermes-405B (NousResearch/Hermes-3-Llama-3.1-405B)

| Task | Result | Quality | Time |
|------|--------|---------|------|
| Skeptical voice evaluation | Success | Excellent (4.5/5) | ~15-20s |
| Literary/voice analysis | Success | Excellent (4.5/5) | ~15-20s |

**Strengths:**
- Best model found for honest, nuanced evaluation
- Resists sycophancy — gives specific, actionable critique
- 4.5/5 for evaluation and writing advice
- Doesn't pull punches even when being constructive

**Weaknesses:**
- Larger model = slightly higher cost than 70B variant
- Better for evaluation than generation

## Conclusion

**Nemotron-30B** fills the mid-tier coding subagent niche well. Not as good as Seed-2.0-mini for pure code, but more reliable (no SIGKILL timeouts). Use when z.ai/kimi are down and Seed-2.0-mini is flaking.

**Hermes-405B** is the fleet's go-to for honest evaluation. Upgrade from Hermes-70B for tasks requiring deeper nuance. Worth the extra cost for voice/literary analysis.

## Casting Recommendation

```
Premium coding unavailable? → Nemotron-30B (fallback) or Seed-2.0-mini (fast failback)
Need honest evaluation? → Hermes-405B (best) or Hermes-70B (cheaper)
```
