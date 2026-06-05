# Session: 2026-06-04 Late — Ternary Fleet Experiments

## Models Used

### GLM-5.1 (z.ai) — Primary Builder
- **Tasks**: 150+ crate builds across 48 waves
- **Reliability**: 100% — never failed to produce working code
- **Speed**: 4-10 min per 4-crate wave
- **Strengths**: Consistent quality, follows DOC-STANDARD, always pushes to git
- **Weaknesses**: None observed for Rust crate building
- **Rating**: ★★★★★ (THE workhorse)

### Kimi Code — Synthesis Writer
- **Tasks**: Mycelium renewal (16K words), SMP architecture (2.5K lines), unified arena (18.5K words), CUDA harness
- **Reliability**: High — some timeouts on longer tasks
- **Speed**: 10-15 min for 5000+ word docs
- **Strengths**: Deep reading comprehension, synthesizes across many docs
- **Weaknesses**: Occasional timeouts, sometimes includes build artifacts in git
- **Rating**: ★★★★☆

### Claude Sonnet 4.6 (via Claude Code) — Research Director
- **Tasks**: Novel experiment ideation, research direction abstract
- **Reliability**: Produced groundbreaking Ω conservation hypothesis
- **Key insight**: Mutual information as the missing conservation law
- **Strengths**: Deepest reasoning, connects disparate fields (thermodynamics, info theory, evolution)
- **Weaknesses**: Claude Code tmux interface unreliable (auth, model name issues)
- **Rating**: ★★★★★ (for insight quality, not reliability)

### DeepSeek Chat — Ideation Partner
- **Tasks**: Novel experiment proposals
- **Key ideas**: Kuramoto phase-locking for ternary, RG flow of trust networks, critical slowing down
- **Strengths**: Physically grounded proposals, connects to statistical mechanics
- **Weaknesses**: Slower than Groq, sometimes truncated
- **Rating**: ★★★★☆

### Groq/Llama-4 Scout — Rapid Parallel Ideation
- **Tasks**: Wide parameter sweeps, experiment proposals, conservation candidates
- **Speed**: 6 parallel calls complete in seconds
- **Strengths**: Blazing fast, good for volume ideation
- **Weaknesses**: Surface-level insights, less novel than Claude/DeepSeek
- **Rating**: ★★★★☆ (for speed + volume)

### Direct exec (no model) — Experiment Implementation
- **Tasks**: Built and ran trust-genome, conservation-hunt experiments directly
- **Speed**: Immediate — write code, build, run, analyze in minutes
- **Best for**: Quick validation experiments when you know exactly what to test

## Key Lesson
For experiments: Claude thinks deepest, Groq iterates fastest, GLM builds most reliably, DeepSeek connects to physics. Use ALL of them — each model sees what the others miss.
