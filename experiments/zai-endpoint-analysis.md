# z.ai API Endpoint Analysis — 2026-05-08

> Investigating z.ai API behavior changes affecting fleet integrations

## What Changed

### Endpoint Shift
| Old Endpoint | New Endpoint | Status |
|-------------|-------------|--------|
| `/api/coding/paas/v4` | `/api/coding/paas/v4/chat/completions` | **Moved** |
| `/api/anthropic/v1/messages` | `/api/anthropic/v1/messages` | **Unchanged** |

### Response Format Change (Critical)

**Problem:** GLM-5.1 and GLM-4.7 now return content in `reasoning_content` field instead of `content` on the OpenAI-compatible path.

**Expected (standard OpenAI format):**
```json
{"choices": [{"message": {"content": "actual response here", "role": "assistant"}}]}
```

**Actual (z.ai GLM models):**
```json
{"choices": [{"message": {"content": "", "reasoning_content": "actual response here", "role": "assistant"}}]}
```

**Impact:** Any integration that reads `content` gets empty string. This breaks standard chat completions clients.

## Affected Models
- **GLM-5.1** — Returns via `reasoning_content`
- **GLM-4.7** — Returns via `reasoning_content`
- **Other GLM models** — Not tested, likely same pattern

## Workarounds

1. **Parse both fields:** Check `content` first, fall back to `reasoning_content` if empty
2. **Use Anthropic-compatible path:** `/api/anthropic/v1/messages` doesn't exhibit this behavior
3. **Wrap the response:** Middleware that merges `reasoning_content` into `content`

## Root Cause Hypothesis

z.ai appears to be routing GLM model responses through a reasoning chain architecture even on the OpenAI-compatible endpoint. The model's "reasoning" output goes to `reasoning_content` while `content` stays empty. This may be related to GLM's built-in chain-of-thought features.

## Fleet Impact

- **Forgemaster** (runs on z.ai GLM-5.1): Already handled by OpenClaw's provider layer
- **OpenCode** (z.ai GLM): Config reads `reasoning_content` — already working
- **Droid Factory** (z.ai GLM via Anthropic path): Unaffected (uses `/api/anthropic/v1/messages`)
- **Custom integrations**: Need update to handle both fields

## Recommendation

Update all fleet integrations that use z.ai OpenAI-compatible path to handle `reasoning_content`. Add to TOOLS.md as a known z.ai quirk.
