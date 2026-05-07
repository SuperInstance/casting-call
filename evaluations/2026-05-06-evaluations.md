# 2026-05-06 Model Evaluations

## DeepSeek v4-Pro (deepseek-reasoner) — Mathematical Proofs
- **Task:** 3 challenges: dim H⁰ = 9 proof, Intent-Holonomy Duality (timed out), Galois Unification (timed out)
- **Result:** PARTIAL — dim H⁰ = 9 PROVEN via root propagation isomorphism (clean proof). Intent-Holonomy Duality ran 8000+ reasoning tokens, ran out of output budget twice. Galois Unification also timed out.
- **Score:** 4/5 (dim H⁰ = 9 proved), 2/5 (long-running proofs)
- **Tokens:** 8000+ reasoning tokens per challenge
- **Time:** >60s per challenge
- **Would cast again:** YES — for well-scoped mathematical theorems with clear endpoints. PARTIAL — for open-ended deep reasoning that might run out of budget.
- **Notes:** Intent-Holonomy Duality later resolved by human analysis: FALSE on partial orders, TRUE on total orders (4/5 confidence). 3 errors in claim corrections: 24-bit bound FALSE (use i32), D6 orbit count 13 not 11, Eisenstein triple density 73% not 25%.

## DeepSeek Chat (v4-chat) — Proof Support
- **Task:** 4 proofs/theorems completed (INT8 Soundness, XOR Dual-Path, dim H⁰ = 9, Beam-intent DEBUNKED), cache bandwidth model
- **Result:** SUCCESS — Measured numbers ↔ math: cache bandwidth model M ≈ 4.49 explains 4.58×. INT8 Soundness: cast is identity on [-127,127] → comparison preserved.
- **Score:** 4/5
- **Time:** ~10s
- **Would cast again:** YES — For fast proof verification and conceptual analysis. Use reasoner for deep proofs, chat for shallow.
- **Notes:** Beam-intent equivalence DEBUNKED (superficial analogy). INT8 overflow found (4.9% mismatch) → fixed with range validation.

## Seed-2.0-Mini — Cross-Model Replication + Compiler Engineer Critique
- **Task:** Evaluate 7 claims, compiler engineer critique + scenario testing
- **Result:** SUCCESS — Scored claims (C3=5.0 avg). Solid engineering critique.
- **Score:** 4/5
- **Cost:** Cheap
- **Would cast again:** YES — Primary failback. Good at everything asked.
- **Notes:** Claims C3 (Negative Knowledge) = 4.8/5 average across all 3 replication models.

## Hermes-405B — DO-178C Critique + E2E Optimization
- **Task:** DO-178C critique, end-to-end optimization analysis, paper intro draft
- **Result:** SUCCESS — Strong domain-specific critique.
- **Score:** 4/5
- **Would cast again:** YES — Safety-critical domain analysis and creative paper drafting.
- **Notes:** Part of session 9 deep research.

## Qwen3-235B — Adversarial Red Team
- **Task:** Bug hunting and adversarial testing of INT8 code
- **Result:** SUCCESS — Found 3 bugs: INT8 overflow wrapping (4.9% mismatch), dual-path subtraction overflow (3 edge cases), SoA conversion dominates E2E (0.14x one-shot).
- **Score:** 4.5/5
- **Would cast again:** YES — Best model discovered for adversarial testing and bug hunting.
- **Notes:** All 3 bugs were real and subsequently fixed. SoA conversion: break-even at 8 reuses. Second-life: steady-state 12.02×.

## Qwen3.5-397B — Systems Performance Critique
- **Task:** Systems performance analysis
- **Result:** SUCCESS — Independent verification of performance numbers.
- **Score:** 4/5
- **Would cast again:** YES — for performance analysis and systems critique.
- **Notes:** SoA mixed AVX-512: 3.17× mean (5-run), 0.42× AoS (7.5× layout difference). INT8 raw: 4.58×.

## Step-3.5-Flash, Nemotron-120B, Hermes-405B, Gemma-4-26B, Qwen3.5-397B, Seed-2.0-mini — Zero-Shot Outside Perspectives (6 models, 13 runs)
- **Tasks:** 
  - **Task 1 - Reverse Actualization** (MythoMax, Euryale, Llama-4-Maverick): Creative model test
  - **Task 2 - Devil's Advocate** (DeepSeek-R1, Nemotron, Qwen3-Coder, Qwen3-Thinking): Reasoning model test
  - **Task 3 - Novel Insight** (Step-3.5-Flash, Gemma-4, Seed-2.0-pro, Hermes-405B, Qwen3.5-397B)
  - **Zero-Shot Perspectives** (6 perspectives, 6 models): 13 runs, 224KB total
- **Results:** 
  - **DeepSeek-R1:** 194-line logical critique — "No Relational Structure" (strongest critique of channels)
  - **Nemotron:** "Calculator Trap" counterexample (identical 8-channel profiles, different answers). Adversarial corruption concern (coherent but false intent profiles)
  - **Step-3.5-Flash:** Found C9 gap independently (Context Anchor / pragmatic constraints) in 12-model wide parallel
  - **Gemma-4:** Found C9 gap independently (Teleological Vector) in 12-model wide parallel
  - **Seed-2.0-pro:** Found C9 gap independently (Salience Threshold) in 12-model wide parallel
  - **ALL logical models (Task 2):** channels describe categories but NOT relationships between them
  - **ALL creative models (Task 1):** success from UNEXPECTED domains, failure from OVERCONFIDENCE in single channel
- **Average zero-shot rating:** ~2.2/5 (interesting but unproven)
- **Universal consensus:** Define terms operationally, add more languages (African, tonal, sign, polysynthetic), add non-verbal communication, show counterexamples
- **Most valuable critique:** Yoruba — "Tone is not a tool (C7). Tone IS the grammar." → C1/C7 orthogonality breaks for tonal languages
- **Would cast again:** YES — Zero-shot perspective protocol is valuable methodology. Recommend continuing for validation.

## Euryale (Creative, Reverse Actualization)
- **Task:** Parking lot sensor story
- **Result:** SUCCESS — mundane domains reveal unexpected channel utility
- **Score:** 3.5/5
- **Would cast again:** YES — Creative ideation from unexpected angles.

## Llama-4-Maverick (Creative)
- **Task:** Process channel flood in 2029 scenario
- **Result:** SUCCESS — Identified channel redundancy/audit systems need
- **Score:** 3.5/5
- **Would cast again:** YES — Creative scenario generation.

## Claude Code — Resonance Synthesis
- **Task:** Deep synthesis connecting Oracle1's fleet math to Forgemaster's A2A research (~1200 words)
- **Result:** SUCCESS — KEY FINDING: Both solve the same sheaf cohomology problem (H⁰(S) ≠ ∅). 8 specific connections identified.
- **Score:** 5/5
- **Tokens:** ~1200 words output
- **Would cast again:** YES — For cross-domain synthesis and deep connective reasoning.
- **Notes:** Most important insight: Zero holonomy at trust layer, non-zero at semantic layer = resonance. Unified 3-layer architecture produced.

## DeepSeek-R1 — Devil's Advocate (ZHC × A2A)
- **Task:** 194-line logical critique of A2A channel framework
- **Result:** SUCCESS — "No Relational Structure" was the strongest critique across all models. ALL four reasoning models agreed: channels describe categories but not relationships between them.
- **Score:** 5/5 (critique), 3/5 (constructive solutions)
- **Would cast again:** YES — For rigorous logical critique of frameworks.
- **Notes:** This critique led to the architecture decision: "Polyglot ON TOP of Compiler" (channels wrap ASTs, don't replace them).

## Step-3.5-Flash — Zero-Shot Chinese Skeptic + Novel Insight
- **Task:** Chinese Skeptic perspective + C9 gap discovery
- **Result:** SUCCESS — C9 (Context Anchor) was one of three independent C9 discoveries. Pragmatic constraints contribution.
- **Score:** 4/5
- **Would cast again:** YES — For balanced analysis with practical insight.

## Kimi — Conversation Analysis (Eisenstein-Hex Math)
- **Task:** Signal/noise analysis of 287KB Kimi conversation across 4 iterations
- **Result:** SUCCESS — 9 items BUILDABLE (E12 type, Eisenstein triples, hex ZHC, FLUX-C opcodes), 6 items RESEARCH, 12 items NOISE. All 7 mathematical derivations proven.
- **Output:** 11.8KB analysis
- **Score:** 4/5
- **Would cast again:** YES — For large conversation analysis and signal extraction.
- **Notes:** 7 proven derivations: hex disk, Eisenstein norm, hex Laman, D6 orbits, FCC, hex memory throughput, Eisenstein triples density. Best signal/noise ratio among large-model analyses.
