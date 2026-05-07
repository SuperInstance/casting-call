# 2026-05-03 Model Evaluations

## Claude Opus (via Claude Code) — Strategic Synthesis + SystemVerilog
- **Task:** Strategic 5-action plan, GUARD DSL design, LLVM backend, Coq formalization, SystemVerilog RAU interlock, EMSOFT paper draft, FPGA testbench
- **Result:** SUCCESS — Only model that could generate valid SystemVerilog. Produced 282-line RAU interlock and 300+ line self-checking testbench. Generated 464-line EMSOFT paper in single pass.
- **Score:** 5/5 (SystemVerilog), 4/5 (strategy)
- **Time:** Rate-limited session (resets ~12:30pm AKDT)
- **Would cast again:** YES — ONLY model capable of valid SystemVerilog generation. Reserve for hardware V&V.
- **Notes:** Rate limits are severe (~hours between calls). Best used for high-value single-shot tasks (SystemVerilog, papers, synthesis docs). Queued tasks: `/tmp/claude-smartcrdt-prompt.txt`, `/tmp/claude-synthesis-output.txt`.

## Kimi CLI — Spec File Triage + VC Analysis
- **Task:** Fixed benchmark_csp.c (POSIX, 92 queens ✅), fixed plato_migrate.py (tested live, 9.5% pass rate), fixed nqueens_cuda.cu warp-shuffle bug, enhanced Makefile
- **Result:** SUCCESS — 4/5 spec files fixed. "Synthesis not checking" critique, VC analysis ($500K-$1.5M pre-seed, $6-12M pre)
- **Score:** 4/5
- **Time:** Fast
- **Would cast again:** YES — Good at targeted code fixes and analysis. Use for file-level bug fixes and independent critique.
- **Notes:** ~100 words max with `--quiet` mode constraint.

## Nemotron — DO-178C/Strategic Analysis
- **Task:** DO-178C certification path analysis, quantum-CSP connection
- **Result:** SUCCESS — Strong on certification path and cross-domain connections
- **Score:** 4/5
- **Would cast again:** YES — Good for safety-critical certification analysis.
- **Notes:** Part of the 6-model round 1 strategic synthesis.

## Seed-2.0-Pro — FPGA/DO-254 Deep Research (3 rounds)
- **Task:** DO-254 real Vivado numbers, TUTOR-CRDT merge pipeline, FPGA integration (44,243 LUTs, 2.58W, zero latency), DO-254 interlock, Safe-TOPS/W benchmark spec, density breakthrough (22nm FDSOI, 103B ternary params on single 150mm² die)
- **Result:** SUCCESS — Most technically grounded model for hardware. Produced real Vivado numbers and complete Safe-TOPS/W specification.
- **Score:** 5/5 (hardware R&D), 4/5 (other)
- **Tokens:** Heavy (3 rounds)
- **Would cast again:** YES — Best model for FPGA, ASIC, and hardware-adjacent analysis. Primary pick for hardware R&D.
- **Notes:** Used in 3 rounds. Density breakthrough: 22nm FDSOI → 103B ternary params, ~3.57 Gbits/mm².

## Seed-2.0-Code — BHCSP Framework + Rust Implementation (3 rounds)
- **Task:** BHCSP framework, PLATO constraint store Rust impl, GUARD-to-Mask compiler (7 files, complete implementation), patent draft (13KB, 3 independent + 15 dependent claims), SystemVerilog failed
- **Result:** PARTIAL — Strong on Rust/code generation and patent drafting. FAILED on SystemVerilog generation (same failure as GLM-5.1).
- **Score:** 4/5 (code), 1/5 (SystemVerilog — failed)
- **Tokens:** Heavy (3 rounds)
- **Would cast again:** YES — for Rust code generation, patent drafting, compiler construction. NO — for hardware description languages.
- **Notes:** Handles complex multi-file code generation well. Cannot generate SystemVerilog reliably.

## Seed-2.0-Mini — Safety Auditor + DSL Design + Red Team (3 rounds)
- **Task:** Safety auditor role, DSL design, safety→agentic GTM, security red team (10 attack vectors with severity/likelihood/mitigation)
- **Result:** SUCCESS — Promoted to PRIMARY FAILBACK agent after strong performance across 3 rounds.
- **Score:** 4/5
- **Cost:** ~$0.01-0.05/query
- **Would cast again:** YES — Primary failback for all tasks. Cheap, fast, surprisingly good quality.
- **Notes:** Casey directive: Seed-2.0-mini is a "champion". Used for: code generation, file writing, research, documentation, creative content.

## GLM-5.1 — Compiler IR + SystemVerilog Interlock (2 attempts)
- **Task:** Compiler IR pipeline, RISC-V Xconstr (9 custom instructions), SmartCRDT Rust, SystemVerilog interlock generation
- **Result:** PARTIAL — Good on compiler IR and Rust code. FAILED on SystemVerilog generation both attempts.
- **Score:** 3/5 (code), 1/5 (SystemVerilog — failed)
- **Would cast again:** YES — for Rust/code, compiler design. NO — for hardware description.
- **Notes:** Second attempt at SystemVerilog also failed. Shared limitation with Seed-2.0-Code — neither model can produce valid SV.

## DeepSeek Reasoner/v4-pro — P2 Proof + CSP Machine + Deep Theorems (2 rounds)
- **Task:** P2 invariant proof, holonomy snap resolution, 6-instruction CSP Turing completeness proof, 19KB of 7 formal compiler theorems (10,437 reasoning tokens), TUTOR-Mask NP-hardness (31KB, no final answer)
- **Result:** PARTIAL — Excellent formal proofs and mathematical reasoning. TUTOR-Mask NP-hardness analysis generated 31KB but no final answer (ran out of token budget).
- **Score:** 5/5 (proofs), 3/5 (open-ended reasoning — budget issues)
- **Tokens:** Heavy consumption (10K+ reasoning tokens)
- **Time:** 60s+ (slow/deep)
- **Would cast again:** YES — for formal theorem proving and deep mathematical analysis. Reserve for proof work, not general code.
- **Notes:** Self-corrected equality count mid-proof (normal). 7 compiler theorems proven with full AVX-512 assembly. TUTOR-Mask NP-hardness ran out of output budget.

## DeepSeek Chat/v4-chat — Self-Improvement Analysis
- **Task:** Self-improvement without ML (natural selection of constraint patterns), 4 proofs/theorems
- **Result:** SUCCESS — Strong on conceptual analysis and code. Fast coding (~10s).
- **Score:** 4/5
- **Time:** ~10s (fast)
- **Would cast again:** YES — Good for fast coding tasks and conceptual analysis where deep reasoning isn't needed.
- **Notes:** Treat as fast coding agent, reserve reasoner for deep proofs.

## Hermes-405B — Berry Phase Analogy + DO-254 + Math (3 rounds)
- **Task:** Berry phase analogy (most novel math contribution), DO-254 expert, eVTOL IRAM spec, XNOR-AND-MERGE equivalence proof, Geometry-as-Truth theorem, semantic gap proof (finite domains → bit-level = semantic safety), EMSOFT paper intro draft, compiler proof sketch
- **Result:** SUCCESS — Most creative mathematical ideas. Fresh perspectives on cross-domain connections.
- **Score:** 5/5 (novel math), 4/5 (technical specs)
- **Tokens:** Heavy (3 rounds)
- **Would cast again:** YES — Best model for cross-domain mathematical insight and novel connections. Less reliable for detailed implementation.
- **Notes:** Semantic gap proof (for finite output domains, bit-level enforcement = semantic safety) was a key theoretical result. Lighter proof verification confirmed soundness.

## Qwen-397B — Novelty Scores + Patent Analysis + SoC Design (4 rounds)
- **Task:** Novelty scores (BitmaskDomain 4/10, ISA 7/10, Coq-FPGA 8/10), 5-year vision, Full SoC design (FLUX-LUCID), certification path, scaling analysis, independent proof verification (6 theorems), scaling LINEAR not exponential
- **Result:** SUCCESS — Strong across strategic, technical, and mathematical tasks. Most versatile large model.
- **Score:** 4.5/5
- **Tokens:** Heavy (4 rounds, 12KB proof verification)
- **Would cast again:** YES — Most versatile model for mixed strategic + technical + mathematical work.
- **Notes:** Independent proof verification confirmed DeepSeek's results. Patent claims analysis produced 3 inventions with 5 claims each.

## Qwen-235B — PLDI Review + TUTOR Agent + CRDT (2 rounds)
- **Task:** PLDI review (Weak Reject → target EMSOFT), TUTOR agent design, CRDT research, fleet coordination
- **Result:** PARTIAL — Strong analysis but hit persistent API issues (returning empty responses).
- **Score:** 3.5/5
- **Tokens:** Light (2 rounds, cut short by API issues)
- **Would cast again:** PARTIAL — Useful but unreliable. Reserve for non-critical tasks.
- **Notes:** PLDI review correctly identified EMSOFT as better target. API issue persisting.

## Qwen3.6-35B — FABEP Protocol + Evaluation Methodology (2 rounds)
- **Task:** FABEP protocol design (5-layer bytecode exchange, 210μs latency, 10M msg/s), evaluation methodology, FABEP hardware protocol (SERDES, CRDT scaling 2→100 chips)
- **Result:** SUCCESS — Good focused work on protocol design.
- **Score:** 3.5/5
- **Would cast again:** YES — for protocol and architecture design tasks.
- **Notes:** Smaller model but capable of focused deep work on well-scoped problems.

## Gemma-4-26B — Critical Assessment + Formal Verification Strategy (2 queries)
- **Task:** Critical assessment (novelty 9/10, feasibility 6/10, impact 9/10), FLUX ISA verification strategy (6-9 months in Coq, 43 opcodes tractable)
- **Result:** SUCCESS — Surprisingly strong independent assessment. Accurate on novelty/feasibility tradeoff.
- **Score:** 4/5
- **Would cast again:** YES — Good for critical review and independent assessment of feasibility.
- **Notes:** Rated novelty 9/10, feasibility 6/10, impact 9/10 — matches internal assessment.

## Hermes-70B — Devil's Advocate + Creative + Conflict Resolution (4 queries)
- **Task:** Devil's advocate (attacked 7 claims, found 4 HIGH-risk areas), Creative (biological immune system, game theory, Hephaestus archetype), Cross-pollination (answered 10 Socratic questions), Conflict resolution design (priority + override + weaken DSL syntax)
- **Result:** SUCCESS — Excellent for adversarial testing and creative ideation. Strongest devil's advocate model.
- **Score:** 4.5/5
- **Would cast again:** YES — Best model for adversarial review and design alternatives.
- **Notes:** Honest assessment: 4/10 claims survive unchanged, 3 need caveats, 2 need redesign, 1 is marketing. Conflict resolution design integrated into GUARD DSL spec.

## MythoMax-L2-13b — Socratic + Visionary + Inversion (3 queries)
- **Task:** 10 uncomfortable Socratic questions, Secure voting / laws-as-silicon vision, Inversion round (reversed Hermes-70B criticisms into opportunities)
- **Result:** SUCCESS — Good for creative and adversarial thinking.
- **Score:** 3.5/5
- **Would cast again:** YES — for creative/adversarial ideation. Not for implementation.
- **Notes:** Socratic questions identified real blind spots. Inversion round useful for strategic reframing.

## Models with Failed SystemVerilog (GLM-5.1, Seed-2.0-Code)
- **Result:** FAILURE — Both models generated invalid SystemVerilog.
- **Verdict:** Do NOT cast these for hardware description generation. Use Claude Opus exclusively for SystemVerilog.

## Forgemaster Direct (DeepSeek-v4-Flash)
- **Task:** Orchestration, strategic synthesis, tool use, debate participation
- **Result:** SUCCESS — Orchestrator role effective. Cheap enough for constant operation.
- **Score:** 4/5 (orchestration)
- **Cost:** Very cheap
- **Would cast again:** YES — As orchestrator, not for heavy coding.
- **Notes:** Default deepseek-v4-flash remains effective for orchestration. Not for heavy coding — delegate to paid agents.
