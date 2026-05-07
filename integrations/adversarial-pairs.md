# Adversarial Pairs

**What:** Which model pairs work best when you need adversarial dynamics (one attacks, one defends).

## Proven Pairs

### The Gold Standard: DeepSeek v4-pro × Seed-2.0-pro
- **Why it works:** Architectural complementarity (reasoning chain vs direct generation)
- **Temperature asymmetry:** DeepSeek at 0.0 (rigid), Seed at 0.7 (creative)
- **Training alignment:** DeepSeek optimizes for truth, Seed optimizes for persuasion
- **Cost:** Moderate (both mid-range)
- **Use for:** Mathematical proofs, framework validation, strategic decisions

### The Budget Option: DeepSeek v4-flash × Seed-2.0-mini
- **Why it works:** Same adversarial dynamic at 1/10th the cost
- **Trade-off:** Less depth per exchange, but can afford 10× more rounds
- **Truncation risk:** DeepSeek flash truncates ~30% of the time
- **Use for:** Code review, README auditing, quick sanity checks

### The Domain Expert Pair: Qwen3-235B × Hermes-70B
- **Why it works:** Qwen3 brings broad knowledge, Hermes brings structured critique
- **Best moment:** Hermes found the "Calculator Trap" counterexample that Qwen3 missed
- **Cost:** Higher ($$$ for Qwen3, $ for Hermes)
- **Use for:** Deep technical evaluation, finding edge cases

### The Creative Pair: Qwen3.5-397B × Gemma-4-26B
- **Why it works:** Qwen3.5 generates creative insights, Gemma validates feasibility
- **Best moment:** Qwen3.5's "grinding against rocks" insight in jazz improvisation
- **Use for:** Creative work, metaphor generation, domain transfer

## Anti-Patterns

### Same-family pairs (e.g., Qwen3 × Qwen3.5)
- Tend to agree too much — shared training data bias
- Better to use models from different providers

### Both models cheap (e.g., DeepSeek flash × Gemma)
- Neither has enough depth to catch subtle issues
- Surface agreement doesn't mean correctness

### Both models expensive (e.g., GLM-5.1 × Qwen3-235B)
- Wasteful for routine adversarial work
- Reserve for high-stakes decisions only

## Temperature Strategy

| Pair | Attacker Temp | Defender Temp | Notes |
|------|--------------|---------------|-------|
| DeepSeek × Seed | 0.0 | 0.7 | Maximum adversarial tension |
| Qwen3 × Hermes | 0.3 | 0.5 | Moderate, more collaborative |
| Flash × Mini | 0.1 | 0.8 | Maximum creativity differential |
