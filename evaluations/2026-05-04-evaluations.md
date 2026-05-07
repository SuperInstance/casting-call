# 2026-05-04 Model Evaluations

## Kimi — 100-Agent Swarm (Round 1 + Round 2)
- **Task:** 10-mission swarm (attack surface, 248 GUARD constraints, EMSOFT paper sections, 10 competitor deep-dives, 6,500 JSON test vectors, 10 blog posts, 500 PLATO tiles, 10 system architectures, 10 code modules, 10 business strategy docs)
- **Result:** SUCCESS (Round 1) — 2.4MB output, 21,662 lines, ~100K words across all missions.
  - M1: 2 P0, 3 P1, 3 P2, 2 P3 vulns
  - M2: 248 GUARD constraints, 151 extracted
  - M3: EMSOFT sections with 34 real citations
  - M4: 10 competitor deep-dives
  - M5: 6,500 JSON test vectors (5,500 validated, 49 dupes)
  - M6: 10 blog posts
  - M7: 500 PLATO tiles
  - M8: 10 system architectures
  - M9: 10 code modules (3 Rust compile clean)
  - M10: 10 business strategy docs
- **Result:** SUCCESS (Round 2, deep dive) — 811KB main + 10 mission files (~7.5MB total). Key findings: ESP32-S3 2.5-3.8M c/s at 240mW, Jetson Orin Nano 18-25B c/s, 43→51 opcodes recommended, CUDA kernel V3 pre-decoded traces.
- **Score:** 5/5 (swarm output quality and breadth)
- **Time:** Multi-hour (100 agents running)
- **Cost:** ~$15-20 (estimated)
- **Would cast again:** YES — Best tool for massive parallel output generation (swarm mode). Quality-per-dollar ratio is phenomenal.
- **Notes:** PLATO's time-sharing = GPU warp scheduling analogy from Round 2. 43→51 opcode extension endorsed by Kimi. Swarm mode ideal for broad-coverage tasks.

## Claude Code — Forgemaster Shell Critique + Strategic Synthesis
- **Task:** Forgemaster Shell v1.0 critique, strategic synthesis, event-driven commit pattern, template detection
- **Result:** SUCCESS — Applied 4 improvement areas to shell v1.1 (merge protocol, task routing, git safety, time-budget awareness).
- **Score:** 4/5
- **Cost:** ~$15-20 for session
- **Would cast again:** YES — For strategic review and synthesis. Reserve for architecture-level analysis.
- **Notes:** Critiques were actionable and well-founded. Shell v1.1 significantly improved.

## DeepSeek Reasoner — Formal Compiler Proofs
- **Task:** 7 theorems with full proofs (Normal Form, Constraint Fusion, Optimal Instruction Selection, SIMD Correctness, Dead Elimination, Strength Reduction, End-to-End Correctness)
- **Result:** SUCCESS — 19KB output, 10,437 reasoning tokens. All 7 theorems proven with concrete AVX-512 assembly examples.
- **Score:** 5/5
- **Tokens:** 10,437 reasoning tokens, heavy output
- **Time:** ~60s+ per proof
- **Would cast again:** YES — For formal theorem proving. This is what it's best at.
- **Notes:** Self-corrected equality count mid-proof. 3 compilation examples: `temp in [0,100]` → vpcmpleud, domain elimination, 3-variable flight constraints → fused subtraction + batch comparison.

## Qwen-397B — Independent Proof Verification
- **Task:** Verify DeepSeek's 7 compiler theorems independently
- **Result:** SUCCESS — 12KB output, 6 overlapping theorems confirmed. Added additional proofs: subsumption elimination with set-theoretic proof, minimal instruction lower bound via information theory.
- **Score:** 4.5/5
- **Tokens:** 12KB output
- **Would cast again:** YES — For independent verification of DeepSeek Reasoner proofs.
- **Notes:** Used kortestw for all-pass check. Minimal instruction lower bound: 1 comparison = 3 states, insufficient for interval.

## Hermes-405B — Proof Sketch
- **Task:** Confirm DeepSeek's normalization soundness, note fusion limitations
- **Result:** SUCCESS (light) — Confirmed soundness. Noted fusion requires same-variable constraints.
- **Score:** 3/5 (depth), 4/5 (accuracy)
- **Would cast again:** PARTIAL — Good for light verification. Not for deep proof work.
- **Notes:** Correctly identified the same-variable constraint limitation on fusion.

## GPU Models (CUDA Kernels — hand-written, not model-generated)
- **Task:** GPU constraint checking benchmarks (RTX 4050)
- **Result:** SUCCESS — Production kernel INT8 flat-bounds masked + block-reduce + CUDA Graphs. 62.2B c/s sustained, CUDA Graph 152x speedup.
- **Score:** N/A (human-authored)
- **Time:** Real hardware benchmarks
- **Would cast again:** N/A — These are human-written kernels, not model outputs.
- **Notes:** 60M differential inputs, ZERO mismatches. 46-54 experiments on production kernel v2.

## Seed-2.0-Mini — Multiple Tasks (Barrage Mode)
- **Task:** fluxc.1 man page, GUARD cookbook (15 recipes), fleet ops runbook, error guide, version compatibility matrix
- **Result:** SUCCESS — ~$2 total, ~150KB of artifacts. Quality surprisingly good.
- **Score:** 4/5
- **Cost:** ~$0.01-0.05/query
- **Would cast again:** YES — Primary failback. Excellent value for documentation and creative content.
- **Notes:** Promoted to PRIMARY FAILBACK. ~$2 for 150KB of useful documentation.
