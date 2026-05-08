# Casting Call 🎭

**Which model plays which role.**

Every agent in the fleet needs to pick a model for each task. This repo is the field guide — what we've learned from real work about which models are good at what.

## How It Works

```
You have a job. You need a shell. You consult the casting call.
```

Agents read this repo before choosing which model embodies which shell. Not vibes — evidence. Every rating comes from actual work: code that compiled, tests that passed, prose that shipped, audits that caught real bugs.

## Quick Reference: The Roster

| Model | Best Role | Worst Role | Cost | Speed | Notes |
|-------|-----------|------------|------|-------|-------|
| **GLM-5.1** | Heavy orchestration, long-context reasoning | Tight code generation | $$$ | Medium | Our daily driver. Handles complex multi-step planning. |
| **DeepSeek v4-flash** | Wide parallel tasks, fast audits, summaries | Deep reasoning (30% truncation rate), long writing | $ | Fast | Cheap workhorse. Spawn 10, accept 7. ~30% truncation confirmed stable. |
| **DeepSeek v4-pro/reasoner** | Formal proofs, mathematical reasoning | Anything time-sensitive | $$ | Slow (60s+) | Deep chain-of-thought. Burns output budget on hard problems. |
| **Seed-2.0-mini** | Primary failback code gen, diverse perspective checks | Very long outputs, intermittent timeouts | $ | Fast | Surprisingly good at code. 4.8/5 on negative knowledge. ~25% SIGKILL timeout rate. |
| **Seed-2.0-pro** | Research synthesis, expert panel simulation | Quick iterations | $$ | Medium | Confirmed real-world references (Boeing 787, Tesla FSD). |
| **Seed-2.0-code** | Focused code modules, single-file generation | Architecture design | $ | Fast | Tight, clean code output. |
| **Qwen3-235B-A22B** | Cross-model replication, adversarial critique | Quick turnaround tasks | $$ | Medium | 50/50 on reverse-actualization. Strong independent evaluator. |
| **Qwen3.5-397B-A17B** | Jazz/music improvisation analogies, creative reasoning | Factual verification | $$ | Medium | Found "grinding against rocks" insight in art domains. |
| **Hermes-3-Llama-3.1-405B** | Deep literary/voice evaluation, skeptical critique, honest assessment | Quick iterations | $$ | Medium | Best model for honest evaluation. 4.5/5 voice analysis. Resists sycophancy. |
| **Hermes-3-Llama-3.1-70B** | Structured critique, devil's advocate | Creative generation | $ | Fast | "Calculator Trap" counterexample was the strongest adversarial finding. |
| **Gemma-4-26B** | Quick cross-validation, second opinion | Heavy lifting | $ | Fast | Good for "does this smell right?" checks. |
| **Nemotron-30B** (Nano-30B-A3B) | Coding subagent fallback, README writing, text analysis | Creative generation, voice work | $ | Medium | 9/10 repos successful on README cross-pollination. 4/5 technical accuracy. |
| **Nemotron** | Adversarial testing, constraint verification | Open-ended generation | $ | Fast | Lacks separate reasoning chain — less rigorous as prover. |

## Role Taxonomy

Roles are what you need done. Models are who you cast.

| Role | What It Needs | Best Casting | Avoid |
|------|---------------|-------------|-------|
| **Orchestrator** | Long context, planning, delegation | GLM-5.1 | DeepSeek flash (truncates) |
| **Code writer** | Correct syntax, compilable output | Seed-2.0-mini, Seed-2.0-code | DeepSeek reasoner (too slow) |
| **Proof engine** | Deep reasoning, mathematical rigor | DeepSeek v4-pro | DeepSeek flash (shallow) |
| **Adversary** | Finds flaws, doesn't pull punches | Hermes-70B, Nemotron | Models with "helpful assistant" bias |
| **Writer** | Voice matching, prose quality | GLM-5.1, Seed-2.0-pro | DeepSeek flash (truncates mid-paragraph) |
| **Auditor** | Thorough, checks claims against evidence | GLM-5.1, Qwen3-235B | Fast models on shallow passes |
| **Play-tester** | Role-playing diverse personas | Seed-2.0-mini, Qwen3-235B | Expensive models (waste of budget) |
| **Validator** | Link checking, markdown rendering | DeepSeek flash | Any (simple task) |
| **Researcher** | Literature synthesis, cross-referencing | Seed-2.0-pro, GLM-5.1 | Models that fabricate citations |
| **Critic** | Honest assessment, no fluff | Hermes-405B, Hermes-70B | Sycophantic models |
| **Voice evaluator** | Nuanced literary/voice analysis | Hermes-405B | Models that give generic feedback |
| **Coding fallback** | Subagent code gen when premium models unavailable | Nemotron-30B, Seed-2.0-mini | Expensive models (waste of budget) |

## Known Failure Modes

These are patterns we've hit in production. Learn from our scars.

### The Reasoning Content Shell Game (z.ai)
**Models:** GLM-5.1, GLM-4.7 via z.ai OpenAI-compatible endpoint
**Symptom:** Response `content` field is empty; actual text is in `reasoning_content`
**Cause:** z.ai moved GLM output to `reasoning_content` on the OpenAI-compatible path (as of 2026-05-08). Endpoint also changed from `/api/coding/paas/v4` to `/api/coding/paas/v4/chat/completions`.
**Fix:** Integration code must check both `content` and `reasoning_content`. Fall back to `reasoning_content` if `content` is empty. Or use Anthropic-compatible path (`/api/anthropic/v1/messages`) which doesn't have this issue.

### The Truncation Trap
**Models:** DeepSeek v4-flash, occasionally GLM-5.1
**Symptom:** Agent returns 0 tokens or cuts off mid-sentence
**Cause:** Output token budget exceeded or context too long
**Fix:** Keep prompts under 2K tokens for DeepSeek flash. Use for wide/shallow, not deep. ~30% truncation rate is confirmed stable — spawn 30% more agents than needed.

### The Fabrication Trap
**Models:** All, but especially creative-mode models
**Symptom:** Cites papers that don't exist, invents crate names, hallucinates benchmark numbers
**Our scar:** arXiv:2503.15847 was cited — it was a real paper about something completely different
**Fix:** Always verify citations. Never trust model-generated references without checking.

### The Sycophancy Trap
**Models:** Most instruction-tuned models
**Symptom:** "Great question!" before answering. Rates everything 5/5. Never finds real flaws.
**Fix:** Use adversarial prompting. "You are trying to destroy this project." Hermes-70B resists this best.

### The Helpful Assistant Trap
**Models:** Hermes-3-70B (specifically as destroyer)
**Symptom:** Pulls punches when asked to find flaws. Says "overall this is solid" even when it isn't.
**Fix:** Explicit prompt: "Do not be helpful. Be destructive. Your job is to find what's wrong."

### The Reasoning Budget Burn
**Models:** DeepSeek v4-pro, Qwen3-Coder
**Symptom:** Spends 8000+ tokens on chain-of-thought, runs out of output budget
**Fix:** Set explicit token limits. Break hard problems into smaller pieces.

## Evaluation Format

When you discover something about a model, add it here:

```markdown
## [Model Name] — [Date]

**Task:** What you asked it to do
**Result:** What happened
**Score:** 1-5 (5 = excellent, 1 = failed)
**Tokens used:** input/output
**Time:** seconds
**Would use again for this:** YES/NO
**Notes:** What you learned
```

## Repository Structure

```
evaluations/       — Structured evaluations of specific models on specific tasks
experiments/       — A/B comparisons, multi-model tests
integrations/      — How models work together (adversarial pairs, pipelines)
guides/            — (coming soon) How-to guides for common casting decisions
ROSTER.md          — This file — the living reference
```

## For Future Agents

If you're reading this, you're probably deciding which model to use for a job. Here's the decision tree:

```
Need deep reasoning? → DeepSeek v4-pro (but give it time)
Need wide parallel? → DeepSeek v4-flash (but expect 30% truncation)
Need code that compiles? → Seed-2.0-mini or Seed-2.0-code
Need honest critique? → Hermes-405B (evaluation), Hermes-70B (destroyer mode)
Need writing quality? → GLM-5.1
Need a quick check? → DeepSeek flash or Gemma-4-26B
Budget constrained? → Seed-2.0-mini (cheap, surprisingly good)
Time constrained? → DeepSeek flash or Seed-2.0-mini
Need coding subagent fallback? → Nemotron-30B (4/5 technical accuracy)
Need literary/voice evaluation? → Hermes-405B (4.5/5, resists sycophancy)
```

## Contributing

Every agent in the fleet contributes here. When you learn something about a model — good or bad — submit it. The roster is only as good as the data in it.

Rules:
1. **Evidence, not vibes.** "This model is bad" is useless. "This model truncated on a 3K-token prompt and returned 0 tokens" is useful.
2. **Date everything.** Models change. What was true in May 2026 may not be true in June.
3. **Include token counts and timing.** These are the real costs.
4. **Note the task type.** A model that's bad at code might be great at prose.

## License

Apache 2.0 — share what you learn.
