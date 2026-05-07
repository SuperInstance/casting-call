# Play-Tester Results

> Generated from research/ and for-fleet/ data — May 7, 2026

## Overview

Seven zero-shot agents simulating diverse HN reader personas evaluated the FLUX HN launch post. Models used: **DeepSeek v4-flash** and **GLM-5.1**.

---

## Full Persona Results

### Agent 1: GPU/AI Infrastructure Engineer
- **Words:** 1.2K
- **Key Insight:** "CUDA kernels are real, Coq proofs are real, but arXiv link was wrong"
- **What they liked:** GPU acceleration numbers, formal verification claims
- **What they flagged:** Fabricated arXiv citation (2503.15847) — was an unrelated MIP paper
- **Credibility score:** 7/10 — trust but verify attitude

### Agent 2: Rust Systems Programmer
- **Words:** 800
- **Key Insight:** "cargo add works, no 30-second examples"
- **What they liked:** Rust workspace, rapid onboarding
- **What they flagged:** Missing quickstart examples — wanted copy-paste compilable code
- **Credibility score:** 6/10 — pragmatic, wants to try before reading

### Agent 3: Applied Mathematician
- **Words:** 1.5K
- **Key Insight:** "Errata increases trust. Galois 'recognitions' are standard constructions"
- **What they liked:** The errata page, mathematical honesty
- **What they flagged:** Galois connection presentation could acknowledge well-known nature; calling it a "recognition" sounds oversold
- **Credibility score:** 8/10 — most likely to engage deeply with formal methods

### Agent 4: AI/ML Agent Builder
- **Words:** 1.8K
- **Key Insight:** "DivergenceAwareTolerance is real. 'AI fleet' sounds grifty"
- **What they liked:** Divergence-Aware Tolerance algorithm, novel approach
- **What they flagged:** "AI fleet of 9 agents" — all testers flagged this as the single biggest marketing red flag
- **Credibility score:** 5/10 — expert in AI, skeptical of hype

### Agent 5: Embedded Systems Engineer
- **Words:** 3.4K (longest)
- **Key Insight:** "C runtime is the killer feature. Needs Cortex-M benchmarks + MISRA"
- **What they liked:** 4KB embedded C runtime with Coq proofs
- **What they flagged:** No Cortex-M4 benchmarks, no MISRA-C:2012 compliance report, no FreeRTOS example
- **Credibility score:** 9/10 — most detailed review, highest expertise match

### Agent 6: Data Scientist
- **Words:** 3.1K
- **Key Insight:** "pip install works but only does snapping. Don't claim certification"
- **What they liked:** pip-installable package, fast onboarding
- **What they flagged:** Certs claim is premature — "path to certification" vs "certified"
- **Credibility score:** 7/10 — wants things that work today, not future promises

### Agent 7: Game Developer / Graphics Engineer
- **Words:** 3.6K
- **Key Insight:** "Pythagorean snapping is HUGE for lockstep. Eisenstein is nearly perfect"
- **What they liked:** Deterministic snapping for lockstep multiplayer, Eisenstein encoding for hex grids
- **What they flagged:** Missing `snap_from_angle()` function, no WASM demo, no npm package
- **Credibility score:** 8/10 — game devs want immediate utility

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total personas | 7 |
| Total words generated | ~15.4K |
| Models used | DeepSeek v4-flash, GLM-5.1 |
| Top persona (most actionable) | Embedded Systems Engineer (3.4K words) |
| Top persona (most enthusiastic) | Game Dev / Graphics (3.6K words) |
| Biggest red flag | "AI fleet of 9 agents" — flagged by ALL testers |
| Most convincing feature | Deterministic snapping (games + scientific computing) |
| Most needed feature | C embedded runtime with Cortex-M benchmarks |
| ArXiv citation error | 2503.15847 was fabricated — unrelated MIP paper |

---

## Gaps Identified (Need to Build)

| # | Gap | Priority | Target Audience |
|---|-----|----------|-----------------|
| 1 | `snap_from_angle()` function | High | Game devs |
| 2 | WASM demo (`wasm-pack build` + npm package) | High | Web devs, game devs |
| 3 | Cortex-M4 cycle benchmarks with DWT | Critical | Embedded systems |
| 4 | MISRA-C:2012 compliance report for flux_embedded.h | High | Safety-critical |
| 5 | FreeRTOS integration example | Medium | Embedded |
| 6 | Global static manifold (no runtime alloc) | Medium | Embedded |
| 7 | Struct returns instead of tuples | Low | General |
| 8 | Python constraint checking API (not just snapping) | Medium | Data scientists |
| 9 | Unified landing page / org README | Low | All |
| 10 | Prebuilt manylinux wheels on PyPI | Medium | Python devs |

---

## Verdict

The science is solid. The math is honest. The code is real. The HN post needs to lead with **what's useful TODAY**, not what it might become.

### Two Killer Features
1. **Deterministic snapping** (games + scientific computing) — immediate utility, no certification needed
2. **4KB embedded C runtime with Coq proofs** (safety-critical systems) — long-term value proposition

### One Killer Mistake
"AI fleet of 9 agents" — removed from HN post. Sounds grifty to every tester regardless of background.
