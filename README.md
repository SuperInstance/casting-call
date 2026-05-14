# 🎭 Casting Call

> *Which model for which role? Empirical findings from 25+ parallel subagent runs across a 6-hour fleet session.*

This repo documents the strengths, weaknesses, and optimal workflows for each model in the fleet's casting arsenal. Based on real experience from the May 14, 2026 session: 25+ subagent spawns across 5 model types, building a complete MIDI style decomposition engine with autopilot, JEPA room, and 7 math papers.

## The Fleet Model Roster

### Seed-2.0-mini (DeepInfra, $0.00003/1K tokens)

**Cost per run:** ~$0.003

**Strengths:**
- Creative breadth — generates 3-5 options per prompt
- 5 math papers (32KB total) in a single 2.5min run
- Excellent for exploring design space before committing

**Weaknesses:**
- Frequently times out on tasks >5min with file I/O
- Output quality degrades on specific implementation tasks
- Cannot verify its own work

**Best for:** Architecture exploration, loss design, paper outlines, creative prompts
**Worst for:** Implementing verified code, debugging
**Cast FIRST** in any workflow. Explore the space, then hand off.

### DeepSeek-v4-Flash (default workhorse)

**Cost per run:** ~$0.02

**Strengths:**
- Most reliable — completed the most tasks
- Fast: 2-3min for most implementation tasks
- MAESTRO decompose: 1,276 files, 0 errors, 104 seconds
- Claude Code integration: 299 pieces, 2,001 PLATO rooms

**Weaknesses:**
- Not good at novel architecture design
- Will implement suboptimal solutions from suboptimal specs

**Best for:** Implementation from spec, tests, data processing, CLI tools
**Cast SECOND** after Seed opens the design space.

### DeepSeek-v4-Pro (heavy reasoning)

**Cost per run:** ~$0.05

**Strengths:**
- Caught a real bug: JEPA coupling matrix was non-symmetric (complex eigenvalues, no convergence guarantee)
- Formal verification, convergence proofs, eigenvalue analysis
- Reads actual code carefully, understands implications

**Weaknesses:**
- Slower than flash (2-3min vs 1-2min)
- Most expensive model
- Can over-analyze simple problems

**Best for:** Code review, bug finding, formal verification, convergence proofs
**Cast THIRD.** Review what flash built. Catch bugs Seed didn't anticipate.

### Claude Code (Anthropic, local CLI)

**Strengths:**
- Excellent at complex multi-file implementations
- Built 5 FLUX IR modules (34 tests) in 9min
- Built complete JEPA VenueRoom (7 files, 13 tests) in 3min

**Weaknesses:**
- Not available as a subagent (local, blocking)
- No research/design/verification capability

**Best for:** Large implementation tasks, multi-file builds, test generation
**Use LAST** after Seed designs and Pro verifies.

## The Concert Workflow

```
Seed (design, 2-5min) → Flash (build, 3-5min) → Pro (verify, 2-3min) → Claude (ship, 5-9min)
```

**Real example from the session:**

1. **Seed** → designed 5 loss variants for JEPA training
2. **Flash** → implemented VenueRoom with VICReg loss (13 tests, 3min)
3. **Pro** → found coupling matrix non-symmetry bug (complex eigenvalues!)
4. **Claude** → built full JEPA package (7 files, 13 tests) after fix

## What Each Model Shipped

| Artifact | Model | Time |
|----------|-------|------|
| 5 math papers | Seed | 2.5min |
| Formal verification + 48 theorems | Pro | 3min |
| MAESTRO paper (47KB, 3 theorems) | Pro | 3min |
| 5 FLUX IR modules (34 tests) | Claude | 9min |
| JEPA VenueRoom (7 files, 13 tests) | Flash+Pro | 4min |
| 299 MIDI decomposed, 2,001 PLATO rooms | Flash | 10min |
| 1,276 MAESTRO parsed, 0 errors | Flash | 3.5min |
| PredictiveWheel (70.5% convergence) | Flash | 6.5min |

## Quick Reference

| Need | Cast |
|------|------|
| "Design 3 options" | Seed |
| "Implement from spec" | Flash |
| "Is this correct?" | Pro |
| "Build the whole system" | Claude |
| "Find bugs" | Pro then Flash fix |
