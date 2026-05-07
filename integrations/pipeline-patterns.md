# Pipeline Patterns: Task → Model Chains

**Common multi-step workflows and the model to use at each step.**

---

## Pipeline 1: Full Audit Pipeline

**When:** Every org audit, every release review
**Cost:** ~$0.50-1.00 per run
**Time:** ~15-30 min for 48-repo org

```
Step 1: DeepSeek v4-flash (7 parallel agents)
  → Wide scan: test counts, README accuracy, repo descriptions
  → 15 agents max, keep prompts under 2K tokens
  → Cost: ~$0.02

Step 2: Hermes-3-70B (in destroyer mode)
  → Adversarial pass: find what flash missed
  → Explicit prompt: "You are trying to destroy this project" to counter sycophancy
  → Cost: ~$0.05

Step 3: GLM-5.1 (synthesis)
  → Merge findings, rank severity, write action items
  → Long context needed (all audit reports)
  → Cost: ~$0.10
```

**Phase 15 evidence:** Steps 1+3 only (no Hermes destroyer pass yet). Still caught 8 critical issues. Adding Hermes would catch more.

---

## Pipeline 2: Proof Pipeline

**When:** Proving a theorem, verifying a claim, closing a formal gap
**Time:** ~2-10+ hours
**Cost:** ~$3-10 per proof round

```
Step 1: DeepSeek v4-pro (prover)
  → Chain-of-thought reasoning, English proof first
  → Set explicit token budget (5K output max)
  → Background job (60s+)
  → Cost: ~$0.10-0.50

Step 2: Claude Code (reviewer)
  → Read the proof, find gaps, suggest fixes
  → Use 900-1200s timeout (deep analysis)
  → Reserve credits — not for every proof
  → Cost: ~$2-5 per review

Step 3: GLM-5.1 (documentation)
  → Write the polished proof in LaTeX/Coq
  → Long context for proof + review
  → Cost: ~$0.10

Step 4: DeepSeek v4-flash (validation agent)
  → 1-3 parallel agents verify claims and cross-reference
  → Cheap sanity check before committing
  → Cost: ~$0.01
```

**Phase 14-15 evidence:** Intent-Holonomy duality pipeline ran steps 1-3. Step 4 (validation) was missing, meaning the proof gap persisted until Claude Code review.

---

## Pipeline 3: Publication Pipeline

**When:** Publishing a crate, paper, or npm package
**Time:** ~1-4 hours
**Cost:** ~$5-15 per publication

```
Phase A — Content Generation:
  Step 1: Claude Code (generator)
    → Write paper, README, or crate docs
    → 900-1200s timeout for complex multi-file generation
    → Cost: ~$3-5

  Step 2: GLM-5.1 (polish)
    → Voice matching, consistency check
    → Ensure Casey's tone, not AI-slop
    → Cost: ~$0.10-0.20

Phase B — Adversarial Review:
  Step 3: Hermes-3-70B (destroyer)
    → Identify weak claims, overstatements, fabrication
    → Cost: ~$0.05

  Step 4: Seed-2.0-pro (fact-checker)
    → Verify references, citations, numbers
    → Cross-reference claims against known knowledge
    → Cost: ~$0.05-0.10

Phase C — Audit:
  Step 5: DeepSeek v4-flash (validator)
    → Check test counts, README accuracy, link health
    → Cost: ~$0.01

  Step 6: GLM-5.1 (final review)
    → Everything passes? Does it pass the smell test?
    → Cost: ~$0.05
```

**Phase 15 evidence:** README rewrites went through Phases A + C but skipped Phase B (adversarial). Result: arXiv citation fabrication survived. Cost savings of ~$0.15 but cost credibility later.

---

## Pipeline 4: Research Pipeline

**When:** Investigating a new domain, synthesizing findings
**Time:** ~1-3 hours per round
**Cost:** ~$2-5 per round

```
Step 1: Seed-2.0-pro (primary researcher)
  → Broad domain synthesis, cross-referencing
  → Uses paid plan — get full value
  → Cost: ~$0.20-0.50

Step 2: 2-3 cross-model replicators
  → Seed-2.0-mini, Gemma-4-26B, or Hermes-70B
  → Independent evaluation of same claims
  → Minimum 3 models for statistical validity
  → Cost: ~$0.05-0.15 each

Step 3: GLM-5.1 (meta-analysis)
  → Compare all outputs, score consensus
  → Identify model-specific bias
  → Document confidence levels
  → Cost: ~$0.10

Step 4: Claude Code (synthesis, optional)
  → For high-impact findings: write the definitive doc
  → Use sparingly — high cost, high quality
  → Cost: ~$3-5
```

**Phase 14 evidence:** Reverse actualization experiments (3 problems × 3 languages = 9 calls, Seed-2.0-pro) + cross-model replication (Batch E2: Seed-2.0-mini, Gemma-4-26B, Hermes-70B). Claim 3 scored 4.8/5 average across 3 models = strong consensus.

---

## Pipeline 5: Release Readiness Pipeline

**When:** Every public-facing release (HN post, blog, crate, paper)
**Time:** ~2-6 hours
**Cost:** ~$5-10 per release

```
Gate 1 — Technical Accuracy:
  → DeepSeek v4-flash (7 parallel agent play-test)
  → 7 diverse personas, zero-shot
  → Pass condition: <3 negative findings on core claims

Gate 2 — Honest Framework:
  → GLM-5.1 (honesty checker)
  → Overstatement scan, certification language, fabrication search
  → Pass condition: zero aspirations presented as facts

Gate 3 — Adversarial:
  → Hermes-70B (destroyer mode)
  → Tries to find the one thing that makes the whole project sound grifty
  → Pass condition: no killer finding

Gate 4 — Numbers:
  → Seed-2.0-pro (fact checker)
  → Test counts, token counts, benchmark numbers, citations
  → Pass condition: <1% error rate in all claims

Gate 5 — Final:
  → GLM-5.1 (executive summary)
  → "What's useful today" framing
  → Pass condition: passes the Casey "ship it" test
```

**Phase 15 evidence:** The HN launch used Gates 1 + 5 but skipped 2, 3, 4. Play-testers found arXiv citation fabrication, certification overclaim, and test count errors — all of which would have been caught by the full pipeline.

---

## Pipeline 6: Cross-Language Parity Pipeline

**When:** When code must work identically across 2+ runtimes
**Time:** ~30 min - 2 hours
**Cost:** ~$2-5

```
Step 1: Seed-2.0-mini (primary implementer)
  → Write reference implementation in Rust
  → Cost: ~$0.01-0.05

Step 2: GLM-5.1 (port orchestrator)
  → Take Rust implementation, port to JS and Python
  → Ensure API compatibility
  → Cost: ~$0.10-0.20

Step 3: DeepSeek v4-flash (parallel test writers)
  → Write parity tests for each language
  → Same test vectors, same expected outputs
  → Cost: ~$0.02

Step 4: All models (validation)
  → Run tests across all runtimes
  → Cross-validate outputs for identical results
```

**Phase 15 evidence:** DivergenceAwareTolerance — Rust 93 tests, JS 9, Python 9 = 111 total. All passing. Cross-language parity confirmed correctness.

---

## Pipeline Decision Tree

```
What are you doing?
├── Auditing repos? → Pipeline 1 (omit Hermes for speed, include for rigor)
├── Proving a theorem? → Pipeline 2
├── Publishing something? → Pipeline 3 (NEVER skip Phase B)
├── Investigating a domain? → Pipeline 4
├── Releasing to public? → Pipeline 5 (run ALL 5 gates)
├── Porting code? → Pipeline 6
└── Not sure? → Start with DeepSeek flash + GLM-5.1 orchestrate
```

## Cost/Benefit Summary

| Pipeline | Cost | Time | Value |
|----------|------|------|-------|
| 1. Audit | $0.50-1.00 | 15-30 min | Caught 8 critical issues |
| 2. Proof | $3-10 | 2-10 hrs | Found proof gap others missed |
| 3. Publication | $5-15 | 1-4 hrs | Prevent fabricated citation disasters |
| 4. Research | $2-5 | 1-3 hrs | Achieved 4.8/5 consensus |
| 5. Release | $5-10 | 2-6 hrs | Equivalent to 3 HN reviewers |
| 6. Parity | $2-5 | 30 min-2 hrs | 111 tests across 3 runtimes |

**ROI rule of thumb:** The adversarial passes (Pipeline 3 Phase B) cost ~$0.15-0.20 but prevent the worst kind of damage: credibility loss from fabricated claims. Never skip them for public-facing work.
