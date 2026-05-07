# 2026-05-07 Model Evaluations

## DeepSeek v4-Pro (deepseek-reasoner) — Formal Proofs
- **Task:** 3 formal math challenges: dim H⁰ = 9 (GL(9) on tree), Intent-Holonomy Duality, Galois Unification
- **Result:** PARTIAL — dim H⁰ = 9 PROVEN via root propagation isomorphism (clean proof). Intent-Holonomy Duality still processing (8000+ reasoning tokens, ran out of output budget twice). Galois Unification also timed out.
- **Score:** 4/5 (dim H⁰ = 9 proven), 2/5 (open-ended)
- **Tokens:** 8000+ reasoning tokens per challenge
- **Time:** >60s per challenge
- **Would cast again:** YES — For well-scoped mathematical theorems. NOT for open-ended reasoning that might overflow budget.
- **Notes:** Later resolved: Intent-Holonomy Duality FALSE on partial orders, TRUE on total orders (all 6 Galois parts use totally ordered domains → holds in practice, 4/5 confidence).

## DeepSeek Chat (v4-chat) — Supporting Proofs + Cache Model
- **Task:** INT8 Soundness proof, XOR Dual-Path proof, dim H⁰ = 9 support, Beam-Intent DEBUNKED, cache bandwidth model
- **Result:** SUCCESS — Measured numbers ↔ math: cache bandwidth M ≈ 4.49 explains 4.58×. INT8 Soundness proven. XOR Dual-Path (sign-bit XOR = adding 2³¹, bijective order-preserving) proven.
- **Score:** 4/5
- **Time:** ~10s
- **Would cast again:** YES — Fast proof verification and conceptual analysis.
- **Notes:** Beam-intent equivalence correctly identified as superficial analogy. Good at fast, shallow proofs.

## Seed-2.0-Mini — Compiler Engineer Critique + Strong Connections Research
- **Task:** Compiler engineer critique + scenario testing; Evolving sciences deep research (7 domains)
- **Result:** SUCCESS — Produced EVOLVING-SCIENCES-DEEP-RESEARCH.md. Strongest connections: Eisenstein integers (genuinely superior for hex/2D), Golay codes (optimal for 12-bit error correction), RG compression (100:1 achievable).
- **Score:** 4/5
- **Cost:** Cheap
- **Would cast again:** YES — Primary failback. Good for deep research of moderate complexity.
- **Notes:** Overhyped: 2-adic dynamics (n=12 not special), Operads (correct but no new algorithms), FEP (retrofittable but adds complexity). Persistent homology needs scope reduction (60Hz H¹ on 1000-agent fleets infeasible).

## Nemotron — Hex ZHC Proofs (via subagent)
- **Task:** O(V) Laman rigidity checking on hex lattice faces, Eisenstein-triple density verification
- **Result:** SUCCESS — 6/6 Verified. O(V) holonomy check: 0.0009ms/vertex constant across R=1..30. Laman: 1.5× redundancy 2D (asymptotic), 2.0× redundancy 3D FCC.
- **Score:** 4/5
- **Would cast again:** YES — For hexagonal lattice and geometric proofs.

## Hermes-405B — DO-178C Critique + E2E
- **Task:** DO-178C critique of paper claims, end-to-end optimization
- **Result:** SUCCESS — Constructive critique.
- **Score:** 4/5
- **Would cast again:** YES — For safety-critical context critique.

## Claude Code — Kimi Synthesis (FAILED)
- **Task:** Synthesis of 287KB Kimi conversation
- **Result:** FAILURE — Hit z.ai rate limits (503/429 errors). Could not complete.
- **Score:** 0/5 (failed due to infrastructure, not model quality)
- **Would cast again:** PARTIAL — Claude Code itself is capable, but z.ai rate limits make it unreliable for long-running synthesis tasks.
- **Notes:** Workaround: wrote KIMI-ANALYSIS.md directly. Rate limits are a recurring issue with z.ai.

## GLM-5.1 — Paper Subagents (FAILED)
- **Task:** 3 paper subagents for IEEE papers
- **Result:** FAILURE — Multiple cooldowns from z.ai rate limits. All 3 paper subagents failed.
- **Score:** 0/5 (rate limited)
- **Would cast again:** PARTIAL — Capable model but unreliable due to rate limits. Use for short tasks only.
- **Notes:** All 4 papers ended up written directly instead of delegated. z.ai rate limits are the recurring bottleneck.

## Forgemaster Direct (DeepSeek-v4-Flash) — Direct Paper Writing
- **Task:** Written 4 IEEE-format papers directly when delegated agents failed: PAPER-IEEE-INTENT-DIRECTED.md (14.8KB), PAPER-MATHEMATICAL-FRAMEWORK.md (18.6KB), PAPER-ADVERSARIAL-LESSONS.md (15.1KB), PAPER-NEGATIVE-KNOWLEDGE.md (14.5KB), Proof Archive
- **Result:** SUCCESS — 4 papers + proof archive written when subagents failed. Total: ~63KB of academic output.
- **Score:** 4/5
- **Cost:** Cheap (deepseek-v4-flash)
- **Would cast again:** YES — As orchestrator/writer fallback when premium models are rate-limited.

## Eisenstein Crate (hand-built, verified by multiple models)
- **Task:** Rust crate for Eisenstein integer arithmetic
- **Result:** SUCCESS — eisenstein v0.1.0 → crates.io (crate #18). Zero deps, no_std, 12/12 tests.
- **Score:** 5/5
- **Would cast again:** N/A (code artifact)
- **Notes:** Repo: https://github.com/SuperInstance/eisenstein. Built from Kimi analysis recommendations.

## Key Numbers This Session
- SoA mixed AVX-512: 3.17× mean (5-run), 0.42× AoS (7.5× layout difference)
- INT8 raw: 4.58× (cache bandwidth exceeds theoretical 4.0×)
- E2E one-shot: 0.14×; break-even: 8 reuses; steady-state: 12.02×
- Differential: 100M constraints, ZERO mismatches
- Cross-model replication: Claim 3 (Negative Knowledge) = 4.8/5, 92% confidence
- Published: crates.io 18, PyPI 4
- Full corpus: 105,486 words across all research