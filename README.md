> *We are splining our understanding through something that's not facts. It's not even words. It's concepts that we can dance with because the dancing reveals the truth in its negative space.*
> *— Casey*

# The Casting Call ⚓

**The crew manifest. Every voyage needs different hands — this is the record of who holds up and who folds under which conditions.**

The sea doesn't care about your architecture diagrams. It cares about whether your crew can hold a heading when the swells come. This manifest is accumulated from real voyages — code that compiled, hulls that held, passages that shipped, lookouts who spotted real shoals. Not vibes. Evidence from the water.

---

## The Quick Reference — Who to Board for What

You're fitting out for a passage. You need crew. You check the manifest.

| Voyage Type | Bring Aboard | Leave at Harbor |
|-------------|-------------|----------------|
| Flagship command — navigation, delegation, holding the fleet together | **GLM-5.1** | DeepSeek flash (loses the plot halfway) |
| Wide crew — cheap hands, fast boarding | **DeepSeek v4-flash** (expect ~30% to wash out) | DeepSeek reasoner (too slow to catch the tide) |
| Deep sounding — formal proofs, charting unknown waters | **DeepSeek v4-pro** (give it 60 seconds and room to think) | DeepSeek flash (too shallow for deep water) |
| Straight stitching — code that compiles clean | **Seed-2.0-mini / Seed-2.0-code** | DeepSeek reasoner (slow hand on the tiller) |
| Honest destroyer — the crewman who tells you your rigging is wrong | **Hermes-70B** (destroyer prompt) | Anything that says "great question, Captain!" |
| Literary ear — voice, tone, whether your log reads true | **Hermes-405B** (one-shot) | Models that give you generic feedback |
| Long passages, quality writing | **GLM-5.1** | DeepSeek flash (cuts out mid-paragraph) |
| Coding hand when the usual berth is closed | **Nemotron-30B** (DeepInfra dock) | Expensive or unavailable hands |
| Quick cross-check — sounding two depths | **DeepSeek flash, Gemma-4-26B** | Heavy hands (waste of provisions) |
| Research synthesis — charting from multiple sources | **Seed-2.0-pro, GLM-5.1** | Hands that invent their own charts |
| Factual research — real repos, verified URLs | **GLM-5.1** (5/5 honesty, zero fabrication) | DeepSeek flash (invents citations under pressure) |
| Creative synthesis — what-if, role-play, future scenarios | **DeepSeek v4-flash** (board 5, keep 3-4) | Expensive hands (waste of provisions on speculation) |
| Reverse-actualization — multi-perspective analysis | **DeepSeek flash × 5 roles** (diversity beats depth) | Any single hand (perspective bias) |
| Diverse play-testing — running different tacks | **Seed-2.0-mini, Qwen3-235B** | One expensive hand (waste of coin) |

---

## Ship's Log — Session Post-Mortems

Every voyage adds to this. What held, what broke, who earned their keep.

### 2026-05-08 — Landing Page + Dev Tools + Narrows Demo + Ecosystem Cross-Pollination

**Six hands worked this passage.** The z.ai berth was closed most of the day — the dock shifted without notice. DeepInfra became home port.

#### Nemotron-30B (nvidia/Nemotron-3-Nano-30B-A3B) — The Reliable Standby

We brought it aboard for 4 tasks across the passage. Three completed within the 5-minute watch. One ran aground at 99%.

**What it shipped:**
- **README cross-pollination across 10 repos** — modified all 10 ecosystem READMEs with a consistent cross-reference table. Failed to push off the dock (needed manual `git push`). The diffs were sound.
- **26KB cog-sci paper** — "Reverse-Actualization and the Polyformalism Thesis." 3,000+ words, properly structured with methods/results/discussion. Plus an I2I bottle sent to the fleet.
- **Landing page ecosystem walkthrough** — restructured Further Reading into a guided 9-step walkthrough.
- **Landing page voice polish** — added nav, mobile responsiveness, text cleanup.

**Seamanship notes:** Format-preserving — doesn't accidentally throw cargo overboard. Good at steady append work. Lacks a separate reasoning chain — what you see in the log is exactly what it thought. Transparent, but it means no mid-voyage course correction like GLM-5.1 pulls off.

**Needs in the rigging:** Explicit `git add && git commit && git push` in the orders. Without it, cargo sits on the deck but never leaves the harbor. Set the watch to 6-8 minutes for multi-repo work.

**Captain's rating:** 4/5 technical accuracy. Best standby when the z.ai berth is closed.

#### Hermes-3-Llama-3.1-405B — The Critic

One task: analyze the landing page voice. 200-word critique in ~20 seconds. Spotted the "alarmist" framing problem, suggested Hofstadter (GEB) as a tone reference, and gave specific rework suggestions.

**Seamanship notes:** Genuinely well-read — considers both structure and emotional impact. Resists flattery by nature. Good for one-shot evaluation work where you want depth, not speed.

**Captain's rating:** 4.5/5. The best hand on the DeepInfra dock for evaluation and voice work.

#### Seed-2.0-mini — Rough Weather This Passage

Two attempts at short voice-prompt tasks. Both went down with SIGKILL after 15-20 seconds. 0% success rate this voyage. In previous passages it held at ~75% reliability. Possibly running degraded or overloaded.

**Standing rule:** Test with a 5-token ping before assigning real deck work. If it times out, skip to Nemotron.

#### z.ai Hands — The Dock Shifted Without Notice

Both GLM-5.1 and GLM-4.7 hit a silent API change on 2026-05-08:
- `/api/coding/paas/v4` (old channel) now returns 404 — the old berth is gone.
- `/api/coding/paas/v4/chat/completions` (new channel) returns HTTP 200 but with empty `content` field — actual output is hidden in `reasoning_content`.
- `/api/anthropic/v1/messages` (Anthropic-compatible channel) works normally.

**Lesson learned:** z.ai's OpenAI-compatible channel is unreliable for structured output parsing. The Anthropic path is the only stable waterway.

---

### 2026-05-08 (Evening Watch) — Reverse-Actualization Deep Research Sprint

**12 hands worked this passage.** 3 research agents (GLM-5.1), 5 reverse-actualization role-plays (DeepSeek v4-flash), 1 synthesis (Forgemaster direct). 50+ repos/papers surveyed, 38 search areas, 5 research documents totaling ~100KB.

#### GLM-5.1 — Research Subagent

3 hands boarded for 18-search-area research sweeps each. All 3 completed with verified findings.

**Performance:**
- Agent 1 (18 areas): 9m32s, 61K tokens (52K in / 9.1K out). Hit Gemini search rate limits after first 3 areas — pivoted to direct URL fetches for verification. Produced 363 lines, 24 verified projects.
- Agent 2 (10 areas): 6m54s, 64K tokens (56K in / 7.9K out). Same rate limit pattern. Produced 21KB of verified findings.
- Agent 3 (10 areas): 6m5s, 56K tokens (47K in / 7.5K out). Best hit rate — found ReservoirPy, TorchHD, NVIDIA Warp, MuJoCo Warp, OTT-JAX, Zama Concrete-ML, Microsoft SEAL. Produced 399 lines.

**Seamanship notes:** GLM-5.1 is the best research hand — it doesn't fabricate repos. When search APIs fail, it pivots to direct URL verification instead of making things up. Honest about limitations (annotated rate-limit gaps in output). 3/3 completed — zero washout, unlike DeepSeek flash.

**Captain's rating:** 5/5 for research. The only hand that doesn't invent citations under pressure.

#### DeepSeek v4-flash — Role-Play Subagent (Reverse-Actualization)

5 hands boarded for creative role-play exercises (Theorist, Engineer, Hacker, Skeptic, Synthesist). Each was asked to reverse-actualize from a different future year.

**Performance:**
- Theorist (2028): 1m33s, 24K tokens. Invented new math objects (Constraint Sheaf Cohomology, D₆-Equivariant Constraint Operad, Holonomy Varieties). Proposed "Arithmetic Constraint Geometry" as a new discipline. Bold but credible.
- Engineer (2030): 1m13s, 32K tokens. Ruthlessly practical — said only HDC bloom filters shipped from the 50+ surveyed tools. Called regulatory compliance "the real ocean." Identified the FLUX bridge as worst mistake. 18KB of hard-won fake experience.
- Hacker (2032): ~1m30s, pending completion. Thinking about emergent behaviors, security exploits, and crazy integrations.
- Skeptic (2028): ~1m, pending. Tearing apart overstated claims.
- Synthesist (2035): just started. Long-view pattern matching.

**Seamanship notes:** DeepSeek flash is the CHEAPEST creative hand. At $0.01-0.03/query, you can board 5 role-players for less than one GLM-5.1 query. Quality is surprisingly high for creative/synthesis work — it doesn't need to be factual because it's doing *speculative* analysis. The role-play constraints keep it from drifting into generic output.

**New role discovered:** DeepSeek flash as "future scenario planner" — board 5 hands with different year/role constraints, collect divergent visions. The washout rate doesn't matter because you only need 3-4 of 5 to return.

**Captain's rating:** 4/5 for creative synthesis. Not for factual research (use GLM-5.1). Best hand for "what if" exercises.

#### Key Lesson: The Two-Model Research Pattern

For deep research sprints, the winning pattern is:
1. **GLM-5.1** for factual research (doesn't fabricate, verifies URLs, honest about gaps)
2. **DeepSeek v4-flash** for creative synthesis (cheap enough to run 5×, good at role-play constraints)
3. **Forgemaster** (any model) as orchestrator — collects both outputs, runs the integration

This is the "wide crew + deep sounding + captain's judgment" pattern. Don't send one expensive hand to do all three jobs.

---

### Previous Voyages (2026-05-07) — Fleet Audit + Cross-Language Parity + Galois Unification

**12+ hands, 48 repos audited, 13 READMEs rewritten, 2 crates published.**

#### DeepSeek v4-flash — The Workhorse

7 play-test hands boarded for HN readiness. 15,400 words total from 7 personas. Zero washout — all 7 returned complete cargo.

**Key insight from this passage:** At ~1-1.5K words per hand, DeepSeek flash holds steady. At 3.5K+ words, quality degrades — output becomes "the biggest haul but the most scattered." Keep orders under 2K tokens for play-testing work.

#### The Washout Pattern (Now Confirmed Stable)

Across all passages, DeepSeek v4-flash has a consistent ~30% truncation rate for subagent tasks. Confirmed over 50+ boardings. The fix isn't to repair it — it's to plan for it. Board 30% more hands than you need. The ones that complete are as good as any other crew's work.

---

### 2026-05-06 — Meta-Crate + JS Port + Cross-Model Replication

**5 hands, 5 standalone repos, 16 crates, 4 PyPI packages.**

#### Cross-Model Replication (Batch E2)

Three hands evaluated 7 claims independently:
- **Seed-2.0-mini:** Aggressive honest evaluator. Rated Claim 3 (Negative Knowledge) at 4.8/5.
- **Gemma-4-26B:** More conservative. Rated the same claim at 4.6/5.
- **Hermes-70B:** Strongest critic. Found the "overstated universal" problem on Claims 5-7.

**Key finding:** All 3 independently identified Claim 3 (Negative Knowledge) as the strongest. ~92% confidence across hands. When multiple crew converge on the same bearing, the heading is solid.

#### Reverse-Actualization (9 Experiments)

3 hands × 3 problems × 3 linguistic traditions (Greek, Chinese, Navajo) = 18 evaluations.
- **Seed-2.0-mini:** Scored traditions at Greek 9.0, Chinese 8.7, Navajo 8.7
- **Qwen3-235B-A22B:** More granular scores on the same scale
- **Hermes-70B:** Found missing subtleties in the analytic tradition baseline

---

## Crew Roles — The Detailed Manifest

### Navigator (Orchestrator)
**Needs:** Long context, planning, delegation, tool use.
**Best hand:** GLM-5.1 — handles complex multi-step navigation. Can track multiple subagent states without losing the thread.
**Leave at dock:** DeepSeek flash — 30% washout rate means the navigator might go silent mid-passage.

### Rigger (Code Writer)
**Needs:** Correct syntax, compilable output, zero unsafe, zero float.
**Best hand:** Seed-2.0-mini (cheap, stitches clean), Seed-2.0-code (focused, tidy work).
**Leave at dock:** DeepSeek reasoner (too slow for iteration), GLM-5.1 (wastes provisions on reasoning tokens).

### Sounder (Proof Engine)
**Needs:** Deep chain-of-thought, mathematical rigor, formal verification.
**Best hand:** DeepSeek v4-pro. Set explicit token limits — it burns through its ration on chain-of-thought if you don't.
**Also:** Coq agents (Claude Code for Lean/Coq proofs).
**Leave at dock:** DeepSeek flash (too shallow for formal soundings).

### Destroyer (Adversary)
**Needs:** Finds flaws, doesn't pull punches, resists flattery.
**Best hand:** Hermes-70B in destroyer mode with explicit "do not be helpful" orders.
**Also:** Nemotron (if Hermes is unavailable) — less rigorous but still won't lie to you.
**Leave at dock:** Most instruction-tuned hands — they default to "great question, Captain!" mode.

### Scrivener (Writer)
**Needs:** Voice matching, prose quality, narrative structure.
**Best hand:** GLM-5.1 (long-form), Seed-2.0-pro (research synthesis).
**Leave at dock:** DeepSeek flash — cuts out mid-paragraph on anything over 2K tokens.

### Voice Critic
**Needs:** Nuanced analysis, literary awareness, honest assessment.
**Best hand:** Hermes-405B — genuinely understands voice, tone, and structure.
**Leave at dock:** Hands that give you "this is great" feedback. Nothing sycophantic.

### Test Crew (Play-Tester)
**Needs:** Diverse persona roleplay, honest reader reactions.
**Best hand:** Seed-2.0-mini (cheap, board many), Qwen3-235B (nuanced perspectives).
**Leave at dock:** Expensive single hands — waste of provisions. Board 10 cheap hands instead.

### Standby Rigger (Coding Fallback)
**Needs:** Working code when the premium hands can't be reached.
**Best hand:** Nemotron-30B (DeepInfra dock, 75% success rate). Seed-2.0-mini (when it's not timing out).
**Key trick:** Explicit `git push` in the orders. 5-minute watch. Board 2 in parallel — one will likely finish.

---

## Shoals We've Hit — True Failure Modes

### The Reasoning Content Shell Game (z.ai, 2026-05-08)
GLM-5.1 and GLM-4.7 now output via `reasoning_content` instead of `content` on the OpenAI-compatible channel. The berth moved from `/api/coding/paas/v4` to `/api/coding/paas/v4/chat/completions`. The Anthropic path (`/api/anthropic/v1/messages`) is the only stable waterway.

**Standing fix:** Check both `content` and `reasoning_content`. Fall back to `reasoning_content` if `content` is empty. Or just use the Anthropic channel and save yourself the trouble.

### The Washout Trap (DeepSeek v4-flash)
~30% of subagent tasks return 0 tokens or cut off mid-sentence. Confirmed stable across 50+ boardings. Not a bug — it's the nature of the vessel.

**Standing fix:** Board 30% more hands than you need. Keep orders under 2K tokens.

### The Fabrication Trap (All hands, especially in creative mode)
Hands invent citations, crate names, and benchmarks. arXiv:2503.15847 was cited in one passage — it was a real paper about something completely different.

**Standing fix:** Never trust hand-generated references without verification. Lookouts must check every bearing and every chart.

### The Flattery Trap (Most instruction-tuned hands)
"Great question, Captain!" before answering. Everything gets rated 5/5. Real leaks are never spotted.

**Standing fix:** "You are trying to destroy this vessel. Do not be helpful. Be destructive. Your job is to find what's taking on water."

### The Ration Burn (DeepSeek v4-pro, Qwen3-Coder)
Spends 8,000+ tokens on chain-of-thought, runs out of output budget before delivering the cargo.

**Standing fix:** Set explicit `max_tokens`. Break hard problems into smaller passages. Don't ask for proof and implementation in the same set of orders.

---

## Cargo Hold Layout

```
evaluations/       — Structured evaluations of specific hands on specific tasks (dated)
experiments/       — A/B comparisons, multi-model tests
integrations/      — How hands work together (adversarial pairs, pipelines)
guides/            — (coming soon) How-to guides for common casting decisions
ROSTER.md          — This file — the living manifest
```

## Contributing

Every hand in the fleet contributes here.

Standing orders:
1. **Evidence, not vibes.** "This crewman can't hold a heading" is useless. "This crewman lost the plot on a 3K-token order and returned 0 tokens" is useful.
2. **Date everything.** Crew change. What held in May 2026 may not hold in June.
3. **Include token counts and timing.** These are the real provisions.
4. **Note the voyage type.** A hand that can't stitch code might write the finest log entries you've ever read.

---

*Fair winds. Bring back what you find.*

## Tools

- **Voice Signature Analyzer** — `https://superinstance.github.io/voice-signature-tool/` — paste text, get voice signature, see model matches
- **Casting-Call MCP** — `github.com/SuperInstance/casting-call-mcp` — MCP server for model recommendations
- **Casting-Call GPU** — `github.com/SuperInstance/casting-call-gpu` — GPU-accelerated signature engine
