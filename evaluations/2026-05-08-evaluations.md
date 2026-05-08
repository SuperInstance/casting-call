# 2026-05-08 Model Evaluations

## Nemotron-30B (nvidia/Nemotron-3-Nano-30B-A3B) via DeepInfra — Coding Subagent Fallback

- **Task:** README updates across 10 repos, voice critique, landing page section rewrites
- **Result:** SUCCESS — 9/10 repos completed successfully. 1 repo had minor formatting issues. Voice critique was nuanced and actionable (rated 3.5/5 creative, 4/5 technical accuracy).
- **Score:** 4/5 (coding), 3.5/5 (creative), 4/5 (technical accuracy)
- **Tokens:** ~5-7 min per medium task
- **Time:** Variable (5-10 min per repo)
- **Would cast again:** YES — Solid coding subagent fallback when z.ai/kimi unavailable
- **Notes:** Best used for README writing, text analysis, code generation. Not the strongest at creative voice work but competent. Good as a mid-tier option between Seed-2.0-mini (fast/cheap) and Hermes-405B (deep analysis).

## Hermes-405B (NousResearch/Hermes-3-Llama-3.1-405B) via DeepInfra — Evaluation & Literary Critique

- **Task:** Skeptical evaluation of voice consistency, literary/voice analysis
- **Result:** SUCCESS — Excellent nuanced voice analysis. Gave constructive, specific critique rather than generic feedback.
- **Score:** 4.5/5 (evaluation), 4.5/5 (writing advice)
- **Tokens:** Moderate
- **Time:** ~15-20s per evaluation
- **Would cast again:** YES — Best model found for honest literary/voice evaluation
- **Notes:** Resists sycophancy trap better than most. Provides specific, actionable critique rather than "looks good!" Maintains this quality even when prompted to be encouraging.

## Seed-2.0-mini via DeepInfra — Reliability Assessment

- **Task:** Fast text generation, code gen, general failback
- **Result:** MIXED — Intermittent timeouts (SIGKILL). ~25% failure rate observed. When it works, quality is excellent for the price.
- **Score:** 3.5/5 (reliability), 4/5 (quality when working)
- **Would cast again:** YES — Primary fallback but expect failures. Always have retry logic.
- **Notes:** Update from previous sessions: reliability has degraded slightly. Still cheapest option. Still primary failback. But budget for 25% retry overhead.

## DeepSeek v4-flash — Subagent Truncation Rate Confirmed

- **Task:** Multiple subagent spawns for orchestration and parallel work
- **Result:** CONFIRMED — ~30% truncation rate on subagents. Spawn 30% more than needed.
- **Score:** N/A (orchestration role)
- **Would cast again:** YES — For orchestration and cheap parallel work. Accept truncation as cost of doing business.
- **Notes:** This is a known, stable characteristic. Not a bug, a feature of the model's economics. Compensate by over-spawning.

## z.ai API — Endpoint Changes

- **Date observed:** 2026-05-08
- **Finding:** API endpoints have shifted:
  - `/api/coding/paas/v4` → moved. Use `/api/coding/paas/v4/chat/completions` instead.
  - `/api/anthropic/v1/messages` works for Claude-compatible path.
  - **Critical:** `glm-5.1` and `glm-4.7` return content in `reasoning_content` field (not `content`) on the OpenAI-compatible path. This breaks standard chat completions integration.
- **Impact:** Any agent using z.ai OpenAI-compatible endpoint must parse `reasoning_content` instead of `content` for GLM models.
- **Fix:** Update integration code to check both fields. Fall back to `reasoning_content` if `content` is empty.
- **Would use again:** YES — But integration code needs updating.
