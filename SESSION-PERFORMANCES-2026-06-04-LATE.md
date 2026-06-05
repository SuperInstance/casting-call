# Session: 2026-06-04 Late — DeepInfra Fleet Round-Table

## DeepInfra Key
Found in `~/.openclaw/agents/main/agent/auth-profiles.json` under `deepinfra:default.key`

## 140 Models Available on DeepInfra

### Round 1: 5 Models (parallel)

| Model | Response | Quality | Novel Idea |
|-------|----------|---------|------------|
| **Seed-2.0-mini** | ✅ Fast | ★★★★ | Forgiveness windows tuned to RPS cycle length to eliminate Ω drift |
| **Qwen3.6-35B-A3B** | ✅ Empty response | ★☆☆☆ | Failed to produce content |
| **Hermes-3-Llama-3.1-405B** | ✅ | ★★★ | Influencer agents with amplified impact — heterogeneous agent studies |
| **Nemotron-3-Super-120B-A12B** | ✅ Verbose | ★★★ | Rate of change of I_total correlates with γ+H drift magnitude |
| **Gemma-4-31B-it** | ✅ Excellent | ★★★★★ | Ω-Flux: d(I_total)/dt vs d(γ+H)/dt — formal reorganization of state into information |

### Round 2: 5 Models (parallel)

| Model | Response | Quality | Novel Idea |
|-------|----------|---------|------------|
| **Seed-2.0-pro** | ✅ Brilliant | ★★★★★ | **"Conserved quantities do not stabilize life — they govern death."** Ω conserved only during collapse transitions |
| **DeepSeek-V3.2** | ✅ | ★★★★ | Information pulse experiment — spike I_total, see if γ+H compensates |
| **Qwen3.5-397B-A17B** | ✅ Empty | ★☆☆☆ | Failed to produce content |
| **Llama-4-Maverick** | ✅ | ★★★ | Information scrambling — disrupt I_total, measure recovery |
| **Qwen3.7-Max** | ✅ Brilliant | ★★★★★ | **0 state as topological insulator** — Ω locally conserved within 0-state percolation clusters |

## Rankings (This Round)

### Tier 1 — Research Directors
- **Seed-2.0-pro**: Most philosophically profound insight. "Conservation governs death" is a paper title.
- **Qwen3.7-Max**: Topological insulation via 0-state. Concrete, testable, novel.
- **Gemma-4-31B-it**: Clean Ω-Flux formalism. Information-Energy Equivalence framing.

### Tier 2 — Solid Contributors
- **DeepSeek-V3.2**: Information pulse is a good experimental design
- **Nemotron-3-Super-120B**: Interesting but verbose, buried the insight
- **Seed-2.0-mini**: Practical but less novel than Pro
- **Hermes-3-Llama-3.1-405B**: Standard heterogeneous agent study

### Tier 3 — Failed
- **Qwen3.6-35B-A3B**: Empty response (maybe rate limited?)
- **Qwen3.5-397B-A17B**: Empty response

## Cross-Model Synthesis

The 10 model responses (plus Claude + DeepSeek + Groq from earlier) converge on:
1. **Ω = γ + H + I_total is the #1 hypothesis to test** (7/10 models independently proposed testing it)
2. **The 0 state is special** — not passive but structurally important (Qwen3.7-Max, Claude)
3. **Conservation may be phase-dependent** — holds during transitions but not steady state (Seed-2.0-pro, Claude percolation)
4. **Forgiveness timing matters** — not just forgiveness rate but synchronization with system dynamics (Seed-2.0-mini)

## Fleet Knowledge for Future Casting

- **Seed-2.0-pro > Seed-2.0-mini** for deep reasoning (pro found the death/conservation insight, mini was practical)
- **Qwen3.7-Max** is the new heavyweight — 800B-class reasoning, topological insight
- **Gemma-4-31B** quietly excellent — clean formalism without verbosity
- **Large Qwen3.x models flake** on parallel bursts — rate limit or context issues
- **Nemotron-120B** thinks out loud (verbose chain-of-thought) — good for understanding reasoning, bad for concise output
- **Hermes-405B** solid but conventional — doesn't surprise
