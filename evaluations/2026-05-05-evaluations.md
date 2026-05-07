# 2026-05-05 Model Evaluations

## Claude Code — Monorepo Chapters + Architecture Docs
- **Task:** Written chapters ch08 (GPU for non-GPU people, 2,297 words), ch09 (embedded runtime, ARM Cortex-R), ch10 (10 industry deep dives, 1,385 words), ch11 (certification roadmap 18-month plan, 3,097 words), constraint-theory-formalized.md (4,453 words)
- **Result:** SUCCESS — Produced 4 substantive chapters totaling ~11,260 words + formalization doc.
- **Score:** 4/5
- **Cost:** ~$15-20 (entire session)
- **Would cast again:** YES — For long-form technical writing and architecture docs. Best for multi-page document generation.
- **Notes:** Used for heavy lifts during monorepo consolidation. Chapters integrated into constraint-theory-ecosystem.

## Seed-2.0-Mini — Cross-Model Replication
- **Task:** Evaluate 7 claims from navigation metaphor series (Anchors Not Curve, Fair Curve First, Negative Knowledge, Draft Determines Truth, Speed Beats Truth, Survival ≠ Art, Embodiment Missing)
- **Result:** SUCCESS — Scored each claim. Strongest: Negative Knowledge 5.0/5.
- **Score:** 4/5
- **Would cast again:** YES — For evaluation and scoring tasks.
- **Notes:** Claim scores: C1=3.0, C2=4.0, C3=5.0, C4=3.0, C5=4.0, C6=4.0, C7=4.0. Average: 3.86/5.

## Gemma-4-26B — Cross-Model Replication
- **Task:** Same 7 claims evaluation as Seed-2.0-mini
- **Result:** SUCCESS — Scored each claim. Connected Negative Knowledge to Friston's Free Energy Principle with 95% confidence.
- **Score:** 4/5
- **Would cast again:** YES — For independent evaluation with domain connections.
- **Notes:** Claim scores: C1=3.0, C2=4.0, C3=5.0, C4=4.0, C5=4.0, C6=4.0, C7=4.0. Average: 4.0/5. Strongest cross-domain connector of the 3 replication models.

## Hermes-70B — Cross-Model Replication
- **Task:** Same 7 claims evaluation
- **Result:** SUCCESS — Slightly more conservative scoring. Flagged C5, C6, C7 as "overstated as universal."
- **Score:** 4/5
- **Would cast again:** YES — For evaluation with honest critical assessment.
- **Notes:** Claim scores: C1=3.5, C2=4.0, C3=4.5, C4=3.0, C5=4.0, C6=3.5, C7=4.0. Average: 3.79/5. Most critical of the three.

## All Language Implementation Models (21+ languages via code generation)
- **Task:** Generate identical INT8 constraint checking implementations across 42 languages
- **Result:** SUCCESS — 42 implementations, all with identical API. Cross-language differential: 10K golden vectors, 6 verified ZERO mismatches.
- **Score:** 5/5 (consistency across languages)
- **Would cast again:** YES — For multi-language SDK generation where cross-language consistency is critical.
- **Notes:** Languages: Ada, Assembly, C, Clojure, COBOL, Crystal, C#, CUDA, Dart, Elixir, Erlang, F#, Fortran, Gleam, Go, Haskell, Java, JS, Julia, Kotlin, Lua, MATLAB, Nim, OCaml, Pascal, Perl, PHP, PowerShell, Python, R, Ruby, Rust, Scala, Scheme, Shell/Bash, Swift, SystemVerilog, TypeScript, V, VBA, VHDL, WebGPU, Zig. 6 verified runners: Python, JS, Go, Perl, Shell, TypeScript.

## Guard Parser (subagent — likely Seed-2.0-mini or Kimi)
- **Task:** Extended test coverage from 5,500 vectors
- **Result:** SUCCESS — 100/100 extended tests passed.
- **Score:** 4/5
- **Would cast again:** YES — subagent reliably handles test generation.

## Safe-TOPS/W Benchmark Models
- **Task:** Compute Safe-TOPS/W for FLUX-LUCID vs competitors
- **Result:** SUCCESS — FLUX-LUCID 20.19, Hailo-8 1.30, Mobileye 0.50, everyone else 0.00.
- **Score:** 4/5
- **Would cast again:** Yes — for benchmark comparison tasks.
- **Notes:** FLUX-LUCID dominates at DAL A. Tooling: safe_tops_per_watt.py.
