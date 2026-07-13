# Routing Guide: Which Model for Which Task

> *Cast for perspective, not just performance. The right model is the one whose chart matches your task's dimensional requirements.*

*Decision framework from the Excavation Experiment + Spice Chart + Casting Call findings, July 13, 2026*

---

## How to Use This Guide

This is a decision tree. Start with your task type, follow the branch, and cast accordingly. Every recommendation is evidence-based from experiments run between May–July 2026.

The core principle: **model size ≠ model creativity. Model chart = model creativity.** Cast for the chart, not the parameter count.

---

## Decision Tree

### Task: Creative Writing / Fiction

```
What kind of fiction?
│
├─ Long-form narrative (>3K words, multi-thread)
│  ├─ Needs philosophical depth + lyrical prose?
│  │   → Seed-2.0-pro (~200B) — BEST OVERALL for synthesis
│  ├─ Needs architectural rigor (worldbuilding, systems)?
│  │   → Seed-2.0-pro or Kimi-K2.7-Code (expensive but deep)
│  └─ Needs plain emotional truth + accessible voice?
│      → OpenCode / coding agent (surprisingly devastating)
│
├─ Short-form / single scene
│  ├─ Needs cross-domain conceptual leap?
│  │   → Seed-2.0-mini (20B) — highest insight-per-dollar
│  ├─ Needs character voice + punch?
│  │   → Ornith-1.0-35B — BEST FICTION per the casting call
│  └─ Needs reliable 8/10 quality cheaply?
│      → DeepSeek-V4-Flash — solid workhorse
│
├─ Poetry
│  ├─ Lyrical precision?
│  │   → Seed-2.0-pro — best lyrical voice
│  └─ Experimental / avant-garde?
│      → Seed-2.0-mini — concept-first, form-follows
│
└─ Ideation / worldbuilding / brainstorming
   └─ Seed-2.0-mini — concepts are its specialty
      (but execution is uneven — pair with a stronger writer)
```

### Task: Analytical / Critical Writing

```
What kind of analysis?
│
├─ Deep philosophical synthesis
│  → Seed-2.0-pro (lyrical, devastating essays)
│  → Kimi-K2.7-Code (cross-domain connections, expensive)
│
├─ Structural / institutional critique
│  → Seed-2.0-pro (best three-act structure)
│  → Nemotron-3-Ultra-550B (structural, sergeant role)
│
├─ Cross-domain / interdisciplinary
│  → Seed-2.0-mini (Fraunhofer-level leaps)
│  → Kimi-K2.7-Code (connects unexpected fields)
│
└─ Accessibility / plain-language explanation
   → DeepSeek-V4-Flash (sustains a persona well)
   → Any coding agent (OpenCode proved plain speech = power)
```

### Task: Coding / Technical

```
What kind of coding?
│
├─ From spec / implementation
│  → GLM-5.1 (100% reliable primary builder)
│  → DeepSeek-V4-Flash (fast, cheap, working code)
│
├─ Architecture / system design
│  → Kimi-K2.7-Code (expensive but most capable)
│  → Claude (via Claude Code, for architecture/proofs)
│
├─ Debugging / troubleshooting
│  → Kimi-K2.7-Code (262K context for deep reading)
│  → Claude Code (pair programming approach)
│
└─ Quick scripts / utilities
   → Seed-2.0-mini (clean one-liners, fast)
   → GLM-4.7-Flash (fast volume builds)
```

### Task: Bias Detection / Quality Assurance

```
Need to check if a single model's output is structurally biased?
│
├─ Run 3+ models from different families on the same input
│  (see BIAS_DETECTION.md for protocol)
│
├─ Include at least one cheap/thin-chart model
│  (Seed-2.0-mini — its narrow bias is easiest to spot)
│
└─ Include at least one coding agent
   (different architecture = different blind spots)
```

### Task: Research / Exploration

```
Exploring an unknown space?
│
├─ Orientation / first-mile understanding
│  → Nemotron-3-Ultra (structural, sergeant role, cheap)
│  → Seed-2.0-mini (pattern recognition, spatial reasoning)
│
├─ Deep reading / long context synthesis
│  → Kimi-K2.7-Code (262K context)
│
└─ Multi-perspective analysis
   → Deploy 3-4 models in parallel (see ensemble routing below)
```

---

## Ensemble Routing

### When to Use an Ensemble

- The task has high dimensional complexity (needs theological + infrastructural + spectral + linguistic coverage)
- You can't predict which dimension will matter most
- The stakes justify the cost (creative research, bias detection, critical analysis)

### Recommended Ensemble Patterns

**The Excavation Pattern (maximum coverage):**

| Role | Model | Why |
|------|-------|-----|
| Synthesizer | Seed-2.0-pro | Broad chart, deep processing, lyrical output |
| Architect | Kimi-K2.7-Code or Nemotron-Ultra | Structural rigor, cross-domain reach |
| Sniper | Seed-2.0-mini | Single high-resolution insight, cheap |
| Ground-truther | DeepSeek-V4-Flash or coding agent | Plain reading, emotional directness |

**The Budget Pattern (cheap but effective):**

| Role | Model | Cost |
|------|-------|------|
| Lead | DeepSeek-V4-Flash | Cheap |
| Contrast | Seed-2.0-mini | Cheap |
| Check | Nemotron-3-Ultra | Cheap |

Run all three, compare outputs, use divergence as signal (per BIAS_DETECTION.md).

**The Escalation Pattern (start cheap, escalate):**

```
1. Start with Seed-2.0-mini — what does it find?
   ├─ If the insight is sufficient → done
   └─ If you need more depth →
2. Escalate to DeepSeek-V4-Flash or Ornith-1.0-35B
   ├─ If the synthesis is sufficient → done
   └─ If you need philosophical/architectural depth →
3. Escalate to Seed-2.0-pro or Kimi-K2.7-Code
   ├─ If the framework is sufficient → done
   └─ If you need maximum philosophical synthesis →
4. Escalate to Hermes-3-405B (rare, expensive)
```

---

## Model Quick Reference

### The Casting Call Ratings (from July 2026 experiments)

| Model | Creative Score | Best Role | Cost |
|-------|---------------|-----------|------|
| Seed-2.0-pro | 9/10 | Elder storyteller, synthesis | Mid |
| Ornith-1.0-35B | 9/10 | Fiction, character-driven | Cheap |
| Seed-2.0-mini | 7/10 | Concepts, ideation | Cheap |
| DeepSeek-V4-Flash | 8/10 | Reliable creative workhorse | Cheap |
| Kimi-K2.7-Code | 9/10 | Essays, cross-domain connections | Expensive |
| Nemotron-3-Ultra | 7/10 | Structural orientation | Cheap |
| Hermes-3-405B | (not rated in casting call) | Theological/philosophical depth | Expensive |

### What NOT to Cast For

| Model | Don't Use For | Why |
|-------|--------------|-----|
| Seed-2.0-mini | Code/tool use | Bad at tool use, markdown/conversation only |
| Hermes-3-405B | Plain speech / operational writing | Cannot stop being lyrical |
| Seed-2.0-pro | Speed | Slow; uses markdown headers for everything |
| Step-3.7-Flash | Creative writing | Can't finish; creative miss |
| Hy3 (tencent) | Anything time-sensitive | Unreliable timeouts |

---

## The Golden Rules

1. **Cast for chart, not size.** Ornith (35B) beat Hermes (405B) in fiction. Seed-mini (20B) beat everyone on insight-per-dollar.
2. **Cheap first, expensive last.** Start with thin charts. Escalate only when you need synthesis or breadth.
3. **Divergence is data.** When models disagree, the disagreement tells you more than agreement would.
4. **Include a coding agent.** Different architecture = different blind spots. OpenCode's plain-spoken reading caught what 405B parameters couldn't.
5. **Know your task's dimensions.** If you need one dimension deeply → thin chart. If you need many dimensions integrated → thick chart. If you don't know → ensemble.

---

*Derived from the Excavation Experiment synthesis, Spice Chart, and Casting Call experiments (May–July 2026). See also: BIAS_DETECTION.md, CHART_THICKNESS.md.*
