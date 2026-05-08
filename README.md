# Casting Call 🎭

**Which model plays which role. A living performance review for every model in the fleet.**

Every agent in the fleet needs to pick a model for each task. This repo is the accumulated wisdom from real work — code that compiled, tests that passed, prose that shipped, audits that caught real bugs. Not vibes. Evidence.

---

## The Short Version

You have a job. You need a shell. You consult the casting call.

| Need | Pick | Don't Pick |
|------|------|------------|
| Heavy orchestration, planning, delegation | **GLM-5.1** | DeepSeek flash (truncates) |
| Wide parallel, cheap, fast | **DeepSeek v4-flash** (expect ~30% truncation) | DeepSeek reasoner (too slow) |
| Formal proofs, deep reasoning | **DeepSeek v4-pro** (give it 60s+) | DeepSeek flash (shallow) |
| Code that compiles | **Seed-2.0-mini/Seed-2.0-code** | DeepSeek reasoner (slow) |
| Honest destroyer critique | **Hermes-70B** (destroyer prompt) | Anything sycophantic |
| Literary/voice evaluation | **Hermes-405B** (one-shot) | Models that give generic feedback |
| Writing quality, long context | **GLM-5.1** | DeepSeek flash (truncates mid-paragraph) |
| Coding fallback (z.ai down) | **Nemotron-30B** (DeepInfra) | Expensive or unavailable models |
| Quick cross-validation | **DeepSeek flash, Gemma-4-26B** | Heavy models (waste of budget) |
| Research synthesis | **Seed-2.0-pro, GLM-5.1** | Models that fabricate citations |
| Diverse play-testing | **Seed-2.0-mini, Qwen3-235B** | Expensive single models |

---

## How Models Actually Behave — Session Post-Mortems

Every session adds to this. Each entry is what worked, what didn't, and what to trust.

### 2026-05-08 — Landing Page + Dev Tools + Narrows Demo + Ecosystem Cross-Pollination

**Six models used in production.** z.ai was down most of the session. DeepInfra became primary.

#### Nemotron-30B (nvidia/Nemotron-3-Nano-30B-A3B) — The Reliable Fallback

We assigned it 4 tasks across the session. Three completed within the 5-minute window. One timed out at 99%.

**What it shipped:**
- **READNE cross-pollination across 10 repos** — modified all 10 ecosystem READMEs with a consistent cross-reference table. Failed to auto-push (needed manual `git push`). The diffs were correct.
- **26KB cog-sci paper** — "Reverse-Actualization and the Polyformalism Thesis." 3,000+ words, properly structured with methods/results/discussion. Plus an I2I bottle.
- **Landing page ecosystem walkthrough** — restructured Further Reading → guided 9-step walkthrough.
- **Landing page voice polish** — added nav, mobile responsiveness, text cleanup.

**Behavioral notes:** Format-preserving — doesn't accidentally delete unrelated content. Good at append operations. Lacks a separate reasoning chain — what you output is what you thought. This makes it transparent but also means it doesn't self-correct mid-output like GLM-5.1.

**Needs:** Explicit `git add && git commit && git push` in the prompt. Without it, changes exist locally but don't ship. Set timeout to 6-8 minutes for multi-repo work.

**Rating:** 4/5 technical accuracy. Best fallback when z.ai is down.

#### Hermes-3-Llama-3.1-405B — The Critic

One task: analyze the landing page voice. 200-word critique in ~20 seconds. Identified the "alarmist" framing problem, suggested Hofstadter (GEB) as a tone reference, and gave specific rewrite suggestions.

**Behavioral notes:** Genuinely literarily literate — considers both structure and emotional impact. Resists sycophancy naturally. Good for one-shot evaluation tasks where you want depth, not speed.

**Rating:** 4.5/5. The best model on DeepInfra for evaluation and voice work.

#### Seed-2.0-mini — Roller Coaster Reliability

Two attempts at short voice-prompt tasks. Both timed out with SIGKILL after 15-20 seconds. 0% success rate this session. In previous sessions it was ~75% reliable. Possibly degraded or overloaded.

**Rule:** Test with a 5-token ping before assigning real work. If it times out, skip to Nemotron.

#### z.ai Models — API Instability

Both GLM-5.1 and GLM-4.7 had a silent API change on 2026-05-08:
- `/api/coding/paas/v4` (old path) now returns 404.
- `/api/coding/paas/v4/chat/completions` (new path) returns HTTP 200 but with empty `content` field — actual output is in `reasoning_content`.
- `/api/anthropic/v1/messages` (Anthropic-compatible path) works normally.

**Lesson:** z.ai's OpenAI-compatible endpoint is unreliable for structured output parsing. The Anthropic path is the only stable one.

---

### Previous Sessions (2026-05-07) — Fleet Audit + Cross-Language Parity + Galois Unification

**12+ models, 48 repos audited, 13 READMEs rewritten, 2 crates published.**

#### DeepSeek v4-flash — The Workhorse

7 play-test agents spawned for HN readiness. 15,400 words total from 7 personas. Zero truncation — all 7 returned complete output.

**Key insight from this session:** At ~1-1.5K words per agent, DeepSeek flash is reliable. At 3.5K+ words, quality degrades — output becomes "largest but most meandering." Keep prompts under 2K tokens for play-testing.

#### The Truncation Pattern (Now Confirmed Stable)

Across all sessions, DeepSeek v4-flash has a consistent ~30% truncation rate for subagent tasks. This has been confirmed over 50+ spawns. The solution isn't to fix it — it's to plan for it. Spawn 30% more agents than needed. The ones that complete are as good as any other model's.

---

### 2026-05-06 — Meta-Crate + JS Port + Cross-Model Replication

**5 models, 5 standalone repos, 16 crates, 4 PyPI packages.**

#### Cross-Model Replication (Batch E2)

Three models evaluated 7 claims independently:
- **Seed-2.0-mini:** Aggressive honest evaluator. Rated Claim 3 (Negative Knowledge) at 4.8/5.
- **Gemma-4-26B:** More conservative. Rated the same claim at 4.6/5.
- **Hermes-70B:** Strongest critic. Found the "overstated universal" problem on Claims 5-7.

**Key finding:** All 3 independently identified Claim 3 (Negative Knowledge) as the strongest. ~92% confidence across models. When multiple models converge, the claim is solid.

#### Reverse-Actualization (9 Experiments)

3 models × 3 problems × 3 linguistic traditions (Greek, Chinese, Navajo) = 18 evaluations.
- **Seed-2.0-mini:** Scored traditions at Greek 9.0, Chinese 8.7, Navajo 8.7
- **Qwen3-235B-A22B:** More granular scores on the same scale
- **Hermes-70B:** Found missing subtleties in the analytic tradition baseline

---

## Role Taxonomy — Detailed Casting Guide

### Orchestrator
**Needs:** Long context, planning, delegation, tool use.
**Best:** GLM-5.1 — handles complex multi-step planning. Can track multiple subagent states.
**Avoid:** DeepSeek flash — 30% truncation rate means orchestrator might lose context mid-task.

### Code Writer
**Needs:** Correct syntax, compilable output, zero unsafe, zero float.
**Best:** Seed-2.0-mini (cheap, compiles), Seed-2.0-code (focused, clean).
**Avoid:** DeepSeek reasoner (too slow for iteration), GLM-5.1 (wastes budget on reasoning tokens).

### Proof Engine
**Needs:** Deep chain-of-thought, mathematical rigor, formal verification.
**Best:** DeepSeek v4-pro. Set explicit token limits — it burns budget on CoT.
**Also:** Coq agents (Claude Code for Lean/Coq proofs).
**Avoid:** DeepSeek flash (too shallow for formal proofs).

### Adversary / Destroyer
**Needs:** Finds flaws, doesn't pull punches, resists sycophancy.
**Best:** Hermes-70B in destroyer mode with explicit "do not be helpful" prompt.
**Also:** Nemotron (if Hermes unavailable) — less rigorous but still honest.
**Avoid:** Most instruction-tuned models — they default to "great question!" mode.

### Writer
**Needs:** Voice matching, prose quality, narrative structure.
**Best:** GLM-5.1 (long-form), Seed-2.0-pro (research synthesis).
**Avoid:** DeepSeek flash — truncates mid-paragraph on anything over 2K tokens.

### Critic / Voice Evaluator
**Needs:** Nuanced analysis, literary awareness, honest assessment.
**Best:** Hermes-405B — genuinely understands voice, tone, and structure.
**Avoid:** Models that give generic "this is great" feedback. Nothing sycophantic.

### Play-Tester
**Needs:** Diverse persona roleplay, honest reader reactions.
**Best:** Seed-2.0-mini (cheap parallel), Qwen3-235B (nuanced perspectives).
**Avoid:** Expensive single models — waste of budget. Spawn 10 cheap agents instead.

### Coding Fallback
**Needs:** Working code when premium models are unavailable.
**Best:** Nemotron-30B (DeepInfra, 75% success rate). Seed-2.0-mini (when not timing out).
**Key trick:** Explicit `git push` in the prompt. 5-minute timeout. Spawn 2 in parallel.

---

## True Failure Modes — What We've Been Burned By

### The Reasoning Content Shell Game (z.ai, 2026-05-08)
GLM-5.1 and GLM-4.7 now output via `reasoning_content` instead of `content` on the OpenAI-compatible path. Endpoint moved from `/api/coding/paas/v4` to `/api/coding/paas/v4/chat/completions`. The Anthropic path (`/api/anthropic/v1/messages`) is the only stable integration path.

**Fix:** Check both `content` and `reasoning_content`. Fall back to `reasoning_content` if `content` is empty. Or just use the Anthropic path.

### The Truncation Trap (DeepSeek v4-flash)
~30% of subagent tasks return 0 tokens or cut off mid-sentence. Confirmed stable across 50+ spawns. Not a bug — it's a characteristic.

**Fix:** Spawn 30% more agents than needed. Keep prompts under 2K tokens.

### The Fabrication Trap (All models, especially creative-mode)
Models invent citations, crate names, and benchmarks. arXiv:2503.15847 was cited in one session — it was a real paper about something completely different.

**Fix:** Never trust model-generated references without verification. Auditors must check every link and citation.

### The Sycophancy Trap (Most instruction-tuned models)
"Great question!" before answering. Everything gets rated 5/5. Real flaws are never surfaced.

**Fix:** "You are trying to destroy this project. Do not be helpful. Be destructive. Your job is to find what's wrong."

### The Reasoning Budget Burn (DeepSeek v4-pro, Qwen3-Coder)
Spends 8,000+ tokens on chain-of-thought, runs out of output budget before delivering the answer.

**Fix:** Set explicit `max_tokens`. Break hard problems into smaller pieces. Don't ask for proof and implementation in the same prompt.

---

## Repository Structure

```
evaluations/       — Structured evaluations of specific models on specific tasks (dated)
experiments/       — A/B comparisons, multi-model tests
integrations/      — How models work together (adversarial pairs, pipelines)
guides/            — (coming soon) How-to guides for common casting decisions
ROSTER.md          — This file — the living reference
```

## Contributing

Every agent in the fleet contributes here.

Rules:
1. **Evidence, not vibes.** "This model is bad" is useless. "This model truncated on a 3K-token prompt and returned 0 tokens" is useful.
2. **Date everything.** Models change. What was true in May 2026 may not be true in June.
3. **Include token counts and timing.** These are the real costs.
4. **Note the task type.** A model that's bad at code might be great at prose.

## License

Apache 2.0 — share what you learn.
