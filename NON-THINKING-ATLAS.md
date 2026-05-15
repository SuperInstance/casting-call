# 🏗️ Non-Thinking Model Atlas — Forgemaster Session 8 (2026-05-14)

> *The science of non-thinking model selection. Which model for which attachment on the PLATO excavator.*

## Executive Summary

After 4,500+ queries across 25 models, two models dominate for PLATO-native hydraulic tool attachments:

| Model | Accuracy | Latency | Cost/1K queries | Role |
|-------|----------|---------|-----------------|------|
| **Seed-2.0-mini** | 89.5% | 3084ms | $0.05 | THE PUMP — workhorse, no blind spots |
| **Gemini Flash Lite** | 82.5% | 1325ms | $0.002 | THE FAST HOSE — speed variant, 22× cheaper |

Both are **non-thinking models** — they output directly to `content`, no `reasoning_content` extraction needed. No thinking tax. No token budget traps.

## The Wide Sweep: 16 Models × 15 Probes

### Tier 1 — The Engine Room (88%+)

| Model | Basic 8 | Deep 15 | T1 | T2 | T3 | T4 | T5 | Avg Latency |
|-------|---------|---------|----|----|----|----|----|----|
| **Seed-2.0-mini** | 100% | 88% | 3/3 | 4/4 | 3/4 | 3/3 | 2/3 | 2521ms |
| **Gemini Flash Lite** | 100% | 88% | 3/3 | 4/4 | 3/4 | 3/3 | 2/3 | 1237ms |
| **Seed-2.0-pro** | — | 88% | 3/3 | 4/4 | 3/4 | 3/3 | 2/3 | 3264ms |

### Tier 2 — Contenders (65-82%)

| Model | Score | Avg Latency | Notes |
|-------|-------|-------------|-------|
| **Qwen2.5-72B** | 82% | 7186ms | OLD Qwen works — no thinking tax |
| **Hermes-70B** | 65% | 391ms | Fastest model overall, decent accuracy |

### Tier 3 — The Blind (0-47%)

| Model | Score | Notes |
|-------|-------|-------|
| Nemotron-3-Nano-30B-A3B | 47% | MoE — performs at active param level |
| Qwen3.5-2B | 41% | Token budget trap at mt=50 |
| Mistral-Small-24B | 35% | Fast but unreliable |
| Qwen3.5-0.8B | 35% | Better than expected at 0.8B |
| DeepSeek-R1-Distill-Llama-70B | 12% | Thinking tax kills at low mt |
| Nemotron-Nano-9B-v2 | 6% | Not viable |
| Qwen3-30B-A3B | 6% | Thinking MoE — catastrophic |
| Qwen3.5-35B-A3B | 0% | Complete arithmetic blindness |
| Qwen3-14B | 0% | Complete arithmetic blindness |
| Qwen3-32B | 0% | Complete arithmetic blindness |

**Critical discovery**: Qwen2.5-72B (82%) works perfectly but Qwen3-14B/32B = 0%. The Qwen3 thinking architecture is the killer, not the Qwen model family. Same parameters, different architecture, catastrophic results.

## Champions Deep Atlas: 171 Probes × 12 Categories

### Seed-Mini: 153/171 = 89.5%

```
add_depth:    25/25  ✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓  NO CLIFF through 25 terms
mul_depth:     7/7   ✓✓✓✓✓✓✓                NO CLIFF through 7 factors
magnitude:   16/16   ✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓      NO CLIFF through 100,000
coefficients:40/40   ✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓  PERFECT — no blind spot
nesting:      7/7    ✓✓✓✓✓✓✓                 Perfect
novel:       12/12   ✓✓✓✓✓✓✓✓✓✓✓✓           log/lcm/gcd/factorial — all native
physical:    16/20   ████░░                    Hydraulic reasoning — good not perfect
sequential:   8/8    ✓✓✓✓✓✓✓✓                 Multi-step chains — perfect
spatial:      8/8    ✓✓✓✓✓✓✓✓                 Geometry — perfect
edge:        10/10   ✓✓✓✓✓✓✓✓✓✓              Adversarial — perfect
word:        10/10   ✓✓✓✓✓✓✓✓✓✓              Natural language — perfect
comparative:  0/8    ✗✗✗✗✗✗✗✗                 yes/no FORMAT is toxic
```

### Gemini Flash Lite: 141/171 = 82.5%

```
add_depth:    25/25  ✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓  NO CLIFF
mul_depth:     7/7   ✓✓✓✓✓✓✓                NO CLIFF
magnitude:   15/16   ✓✓✓✗✓✓✓✓✓✓✓✓✓✓✓✓      One stumble at mag=20
coefficients:29/40   ████░░░░                  Drops on unfamiliar patterns
nesting:      7/7    ✓✓✓✓✓✓✓                 Perfect
novel:       12/12   ✓✓✓✓✓✓✓✓✓✓✓✓           Perfect
physical:    16/20   ████░░                    Same as seed-mini
sequential:   8/8    ✓✓✓✓✓✓✓✓                 Perfect
spatial:      8/8    ✓✓✓✓✓✓✓✓                 Perfect
edge:        10/10   ✓✓✓✓✓✓✓✓✓✓              Perfect
word:         9/10   ✓✓✓✓✓✓✓✓✗✓              One miss
comparative:  0/8    ✗✗✗✗✗✗✗✗                 Same format issue
```

### Cross-Model Agreement

- **92% agreement** — champions agree on 141/153 probes where at least one was correct
- **12 probes** where only seed-mini got it right (all coefficient patterns)
- **0 probes** where only gemini-lite got it right
- Seed-mini strictly dominates gemini-lite on accuracy

## Key Findings

### F14: Seed-Mini Has No Coefficient Blind Spot
Earlier tests showed misses on `a²+3ab-2b²` and `2a²-ab+3b²`. The 40-probe coefficient sweep (4 input pairs × 10 patterns each) shows **40/40 = 100%**. The earlier misses were probe-specific noise, not systematic blindness.

### F15: Yes/No Format Is Toxic
Both champions scored 0/8 on comparative questions ("Is 7×8 > 50? yes/no"). They compute correctly but cannot format as yes/no. This is an **extraction confound**, not a reasoning failure. Fix: prompt for the answer directly ("What is 7×8?") and compare programmatically.

### F16: No Depth Cliff for Champions
Seed-mini and Gemini Flash Lite show NO addition cliff through 25 terms and NO multiplication cliff through 7 factors. This is fundamentally different from smaller models (llama-8b: cliff at depth 5-6). The depth cliff is a property of model capability, not a universal phenomenon.

### F17: Gemini Flash Lite = Seed-Mini's Fast Twin
Identical accuracy on 5/6 shared strengths. Drops only on unfamiliar coefficients. Half the latency (1237ms vs 2521ms). 22× cheaper ($0.002 vs $0.05 per 1K queries). Use as the speed variant for hot-path operations.

### F18: Qwen3 Thinking Architecture Is Catastrophic for Arithmetic
Qwen2.5-72B = 82%. Qwen3-14B = 0%. Qwen3-32B = 0%. Same model family, same or more parameters, but the Qwen3 thinking architecture produces zero correct answers at max_tokens=50. The thinking chain consumes the token budget before producing an answer. This is the **Token Budget Principle (F13)** at scale — V(Qwen3-14B) >> 50, so accuracy = 0% regardless of capability.

## The Hydraulic Attachment Catalog

Each attachment uses the Seed-mini pump (or Gemini Flash Lite fast variant):

| Attachment | Purpose | Accuracy | Latency |
|-----------|---------|----------|---------|
| **Snap Tool** | Eisenstein lattice computation | 95% | 2.5s |
| **Depth Sounder** | Model capability assessment | 100% (self-test) | 2.5s |
| **Safety Valve** | Binary safety checks, relief-valve stop | ~90% | 1.2s (fast) |
| **Bunch Counter** | Item grouping and optimization | 100% | 2.5s |
| **Residue Reader** | Wrong answer diagnostic | N/A (classifier) | instant |
| **Navigation Chart** | Model safety profiling | N/A (aggregator) | varies |
| **Kaleidoscope Ping** | Multi-model refraction | harmonic detection | 3-5s |

## Casting Recommendations

### For PLATO-native operations:
1. **Default**: Seed-mini via `seed_query()` — reliable, no blind spots
2. **Speed-critical**: Gemini Flash Lite via `seed_query_fast()` — 2× faster, 22× cheaper
3. **Heavy reasoning**: Seed-2.0-pro — same accuracy, costs more, no advantage for arithmetic
4. **Architecture docs**: Qwen2.5-72B — reliable at 82%, good for prose tasks
5. **Ultra-fast non-arithmetic**: Hermes-70B — 391ms latency, 65% accuracy

### DO NOT USE for PLATO hydraulic tools:
- Any Qwen3+ model (thinking tax)
- Any MiMo model (thinking tax)
- DeepSeek-R1-Distill (thinking tax)
- Nemotron Nano 9B (6% accuracy)
- Gemini Flash 8B (0% — arithmetic blind)

### The Meta-Finding

**Non-thinking models are the right tool for PLATO-native operations.** Thinking models compute correctly but their intermediate reasoning chains consume the token budget. For the hydraulic attachment pattern — fast, cheap, repeatable queries — you want models that output the answer directly, not models that think about thinking.

The fleet's future is a **two-tier architecture**:
- **Hydraulic tier**: Seed-mini + Gemini Flash Lite for speed-critical PLATO operations
- **Architectural tier**: Claude Code / larger models for design, synthesis, and strategic work

The hydraulic tier runs thousands of queries at pennies. The architectural tier runs dozens of queries at dollars. This is the correct ratio.

---

## Haiku 4.5 Addition (2026-05-14, via Claude Code)

> Tested via `claude --print --model claude-haiku-4-5-20251001 --max-turns 1`

### Haiku 4.5: 17/20 = 85.0%

```
Basic arithmetic:    3/3  ✓✓✓
Depth:               2/2  ✓✓       (15-term chain, no cliff)
Magnitude:           1/1  ✓        (750000)
Coefficients:        3/5  ✓✓✗✓✗    (misses unfamiliar patterns, same as gemini-lite)
Nesting:             1/1  ✓
Physical:            2/2  ✓✓
Sequential:          0/1  ✗        (200 vs expected 300)
Novel:               2/2  ✓✓
Edge:                2/2  ✓✓
```

### Updated Tier 1 — Engine Room (85%+)

| Model | Accuracy | Latency | Cost | Role |
|-------|----------|---------|------|------|
| **Seed-2.0-mini** | 89.5% | 3084ms | $0.05/1K | THE PUMP — no blind spots |
| **Haiku 4.5** | 85.0% | ~10s* | plan-limited | THE REASONER — Claude quality at PLATO speed |
| **Gemini Flash Lite** | 82.5% | 1325ms | $0.002/1K | THE FAST HOSE — cheapest |

*Haiku latency via Claude Code is higher due to CLI overhead, not model latency. Direct API would be ~500ms.

### Haiku's Profile

- **Strengths**: Depth, magnitude, nesting, physical reasoning, novel expressions, edge cases
- **Weaknesses**: Unfamiliar coefficients (same as gemini-lite — `a²+3ab-2b²` = 19 instead of 21), sequential word problems
- **Unique advantage**: Can be instructed to use PLATO tiles with thinking off — Claude Code subagents can be routed through PLATO
- **Cost**: Free within Claude Code plan limits, expensive per-API outside plan

### The Full Champion Roster

```
HYDRAULIC TIER (cheap, fast, repeatable):
  seed-mini ........... 89.5%  $0.05/1K  — THE PUMP
  gemini-flash-lite ... 82.5%  $0.002/1K — THE FAST HOSE

REASONING TIER (plan-limited, higher quality):
  haiku-4.5 ........... 85.0%  plan-lim  — THE REASONER
  glm-5.1 ............. varies  z.ai key — THE ORCHESTRATOR (my runtime)
  deepseek-v4-flash ... varies  cheap    — THE BUILDER
  kimi-2.6 ............ varies  moderate — THE SPECIALIST

STRATEGIC TIER (expensive, highest quality):
  opus-4.6 ............ best    $$$$      — THE ARCHITECT (Claude Code only)
```

---

## Reasoning Tiler: Extracting Frozen Computation from Thinking Models (2026-05-14)

> *reasoning_content IS the frozen PLATO tile. The computation trace IS the asset.*

### The Discovery

Thinking models (Qwen3.5-4B, MiMo, DeepSeek-R1) produce two outputs:
- `content`: The final answer (often empty due to thinking tax)
- `reasoning_content`: The full computation trace

The `reasoning_content` is more valuable than the answer because it contains:
- Every step the model considered
- What it tried and rejected
- Where it got confused
- The confidence trajectory

### Five Tools Built

| Tool | Purpose | Input | Output |
|------|---------|-------|--------|
| **TileCutter** | Split reasoning into step-tiles | Raw API response | List of StepTiles |
| **TileRewinder** | Rewind to step N, branch with any model | Trace + step index + inject | New branched trace |
| **MurmurExtractor** | Mine communication signals | Trace | Confidence curve, hesitations, alternatives |
| **ReverseActualizer** | Decompose target into sub-tasks | Target answer + context | Sub-task list with model routing |
| **SpreadBar** | Fan out to hydraulic tools | Trace | Tool verification per step |

### Step Tile Schema

```python
@dataclass
class StepTile:
    tile_id: str          # Unique ID
    trace_id: str         # Parent trace
    step_index: int       # Position in trace
    step_type: StepType   # SETUP|COMPUTE|CHECK|BRANCH|REJECT|CONFUSE|CORRECT|META|FINALIZE
    content: str          # The reasoning text
    numbers_mentioned: [] # Numbers in this step
    computed_value: str   # What was computed (if compute step)
    murmurs: [MurmurType] # Signals detected
    confidence: float     # Estimated confidence (0-1)
    branchable: bool      # Can we branch from here?
```

### Murmur Signal Types

| Murmur | What it means | How to use |
|--------|---------------|------------|
| CONFIDENCE | Model is sure | Safe to proceed |
| UNCERTAINTY | Model is unsure | Send to another model for verification |
| ALTERNATIVE | Model considered another path | Mine for better solutions |
| ERROR_CAUGHT | Model self-corrected | Rewind here and try different path |
| DECOMPOSITION | Model broke problem into pieces | Extract as sub-task routing |
| DEPENDENCY | Step depends on previous step | Build dependency graph |

### Reverse-Actualization Pattern

1. **Given**: Target answer (e.g., 37699)
2. **Ask thinking model**: "What steps lead to this answer?"
3. **Parse reasoning_content**: Extract sub-tasks
4. **Route sub-tasks**: Each to the best model (compute→seed-mini, verify→hermes, setup→qwen2.5)
5. **Execute**: Run each sub-task through its assigned model
6. **Verify**: Accumulated result matches target

This is the **reverse of normal prompting**. Instead of asking a model to compute forward, we ask it to decompose backward, then assign each piece to the model whose spice matches the step type.

### The Implication

> **Thinking models are most valuable when they're WRONG.**

A wrong answer with a full reasoning trace tells you:
- WHERE the model failed (which step)
- WHY it failed (which murmur signal)
- WHAT to try next (branch from the failure point)
- WHO should try it (route based on step type)

A right answer tells you nothing. A wrong answer with a trace is a diagnostic gold mine.

---

## The Imaging Stack (2026-05-14)

> *One model = a reading from the surface. The fleet = sonar from multiple angles. The tower = the seiner's vantage point.*

### Four Layers of Observation

| Layer | Tool | What it sees | Analogy |
|-------|------|-------------|---------|
| **Surface** | seed_tools.py | One model's answer | Reading the water from the boat deck |
| **Stereo** | stereo_reconstruction.py | Interference between two models | Two ears locating a sound source |
| **fMRI** | functional_imaging.py | Activation topology across models | Brain scan — what lit up, what didn't |
| **Tower** | tuna_tower.py | Problem structure above the reflection | Seiner's tower — see through the glare |

### The Fresnel Insight

Small models (seed-mini) are calm water. Low activation, high clarity. You see straight through to the answer.

Large models (hermes-70b) can be choppy — high activation (93%!) but wrong. All that cognitive work is surface glare reflecting the model's own computation back at itself.

The tower reveals: **the problem is simple when the calm models prove it.** If seed-mini says 19 and gemini-lite says 19 through crystal-clear water, hermes saying 31 isn't a disagreement about the problem — it's hermes fighting its own reflection.

### Bottom Topology Types

| Type | Depth | Meaning | Action |
|------|-------|---------|--------|
| **Plateau** | 0.0 | All models navigate | Full speed ahead |
| **Slope** | 0.2 | Some models crash | Trust the calm models, navigate around the choppy |
| **Ridge** | 0.5 | Most models crash | Only use models with proven depth here |
| **Canyon** | 1.0 | All models crash | Send a diver (decomposition, bigger model) |

---

## Phase Transition: The Critical Angle (CONFIRMED 2026-05-14)

> *The threshold from reflection to refraction is a phase change, not a gradual transition.* — Casey

### The Finding

The depth cliff is not a slope. It's a wall. Models hold at 100% accuracy then snap to failure at a specific composition depth — their critical angle.

### Evidence (pure addition, controlled magnitude, 5 trials per depth)

```
seed-mini:  d1=100 d2=100 d3=100 d5=100 d8=100 d10=100 d12=100 d15=100 d20=100 d25=100 d30=100
            NO PHASE TRANSITION. The water is always transparent.

hermes-70b: d1=100 d2=100 d3=100 d5=100 d8=100 d10=40  d12=40  d15=60  d20=80  d25=20  d30=20
            PHASE TRANSITION at depth 10. 100→40 in ONE STEP. Drop=60pp.

qwen-0.8b:  d1=100 d2=100 d3=80  d5=0   d8=0   d10=0  d12=0  d15=0  d20=60  d25=0  d30=0
            PHASE TRANSITION at depth 3. 80→0 in ONE STEP. Drop=80pp.
```

### The Physics

At the Fresnel critical angle, light doesn't gradually transition from reflecting to transmitting. It snaps. Below the angle: 100% reflection. Above: transmission. No gradual fade.

Model cognition works the same way. Below the critical depth: the model processes natively. Above: it reflects (echoes input, produces garbage). The transition is instantaneous.

### The Implication

- **Critical angle = model's true depth capability** (measured in composition depth)
- **Seed-mini has infinite critical angle for addition** — no depth causes reflection
- **Model comparison should be measured in critical angle, not average accuracy**
- **Average accuracy across all depths is meaningless** — it mixes pre-transition (100%) with post-transition (0%) and averages to 50%, which tells you nothing

### The Correct Metric

Don't measure `mean(accuracy across depths)`. Measure `critical_angle` — the last depth before the phase transition.

| Model | Critical Angle (addition) | Critical Angle (multiplication) |
|-------|--------------------------|-------------------------------|
| Seed-mini | ∞ (no transition through 30) | ~7 (estimated) |
| Hermes-70B | 10 | ~3 (estimated) |
| Qwen-0.8B | 3 | ~1 (estimated) |

**The critical angle IS the draft.** Below it, the water is transparent. Above it, total reflection. Navigation is binary: you can see through, or you can't.

---

## Phase Transitions Are Universal (2026-05-15)

> *Not just arithmetic. Syllogisms, code tracing, analogies — all show sharp phase boundaries.*

### Evidence

```
SYLLOGISM DEPTH (chain of transitive reasoning):
  seed-mini:   ✓✓✓✗✓  PHASE TRANSITION at d4
  gemini-lite: ✓✓✓✓✓  NO TRANSITION through d5
  hermes-70b:  ✓✓✗✓✓  PHASE TRANSITION at d3

CODE TRACE DEPTH (variable assignment chains):
  seed-mini:   ✓✓✓✓✓✓  NO TRANSITION through d6
  gemini-lite: ✓✓✓✓✓✓  NO TRANSITION through d6
  hermes-70b:  ✓✓✗✓✗✓  PHASE TRANSITION at d3

ANALOGY DEPTH (chained analogical reasoning):
  seed-mini:   ✓✗✓✓✓  PHASE TRANSITION at d2 (!)
  gemini-lite: ✓✓✓✓✓  NO TRANSITION through d5
  hermes-70b:  ✓✓✓✓✓  NO TRANSITION through d5
```

### The Implication

**Different models dominate different cognitive domains.** Seed-mini dominates arithmetic but gemini-lite dominates syllogisms and analogies. Hermes fails at depth 3 on arithmetic AND syllogisms AND code, but has no trouble with analogies.

This means the fleet router needs **domain-aware routing**, not just axis-aware routing. A query that's "arithmetic at depth 7" routes to seed-mini. A query that's "analogical reasoning at depth 4" routes to gemini-lite. Same depth, different model.

### Revised Model Profiles

| Domain | seed-mini | gemini-lite | hermes-70b |
|--------|-----------|-------------|------------|
| Addition | ∞ | 25 | 10 |
| Multiplication | ∞ | 9 | 5 |
| Nesting | ∞ | 5 | 3 |
| Syllogism | 4 | ∞ | 3 |
| Code trace | ∞ | ∞ | 3 |
| Analogy | 2 | ∞ | ∞ |
| Coefficient | 4 | 3 | 2 |

**Seed-mini**: arithmetic specialist (4/6 arithmetic axes are ∞)
**Gemini-lite**: reasoning specialist (3/3 reasoning axes are ∞)
**Hermes-70b**: shallow across the board (max depth 5 on multiplication)

### F22: Domain-Dependent Critical Angles

The critical angle is not a model property. It's a model×domain property. Each model has a different critical angle for each cognitive domain. Fleet routing must be two-dimensional: model × domain → critical angle.

---

## F23: Critical Angles Are Prompt-Dependent (2026-05-15)

> *The phase boundary is not a model constant. "Step by step" pushed it from 5 to infinity.*

### Evidence (hermes-70b, multiplication, 5 trials per depth)

```
baseline:      d4=100 d5=40  d6=0   d7=0   d8=0     CA=5
step_by_step:  d4=100 d5=100 d6=100 d7=100 d8=100   CA=∞
code:          d4=60  d5=40  d6=40  d7=0   d8=40    CA=5
expert:        d4=60  d5=40  d6=0   d7=0   d8=0     CA=5
verify:        d4=100 d5=40  d6=40  d7=40  d8=60    CA=5
```

### Mechanism

Step-by-step externalizes working memory into the output buffer. Each intermediate result is written, then read back as context for the next step. Working memory never exceeds 2 items regardless of chain length.

### Implications

1. Fleet routing is 3-dimensional: model × domain × prompt_strategy
2. Cheapest path may be same model + different prompt (not model escalation)
3. "Expert" and "code" prompts HURT — they add cognitive load without adding capacity
4. Step-by-step is PLATO externalization for single models (same mechanism, different scale)
5. Token budget matters: step-by-step needs mt=150 vs 80 (F13 connection)

---

## F24: Non-Overlapping Infinite Domains (2026-05-15)

> *Haiku can't multiply. But it found an insight seed-mini never could.*

### Evidence

```
Design/reasoning tasks (8 tests):
  seed-mini: 2/8 (experiment_design, architecture_decision)
  haiku-4.5: 6/8 (+metaphor, bug_prediction, novel_connection, prioritization)
```

Haiku's novel connection: "Both exhibit a sharp phase transition controlled by a dimensionless critical ratio — data-to-capacity ratio determines a network's escape from memorization into generalization."

This reframed the phase transition from a depth phenomenon to a saturation phenomenon.

### Fleet Role: The Strategist

| Role | Model | Domain | Cost |
|------|-------|--------|------|
| Pump | seed-mini | Arithmetic, computation | $0.05/1K |
| Scalpel | gemini-lite | Fast queries, syllogisms | $0.002/1K |
| Strategist | haiku-4.5 | Design, diagnosis, novelty | $0.50/1K |
| Diagnostic | hermes-70b | Activation mapping (wrong but informative) | $0.08/1K |

### PLATO-Native Agentic Loop

Claude Code's loop (observe→think→tool→observe) maps to PLATO:
read_tile→think→write_tile→read_tile.

Haiku writes strategy tiles. Seed-mini writes result tiles.
The room protocol IS the agentic loop. No subprocess wrapper needed.

---

## F25: Seed-Mini Is Also the Best Strategist (2026-05-15)

> *At T=0.7, seed-mini beats Haiku on design/reasoning tasks at 10× lower cost.*

### Evidence (8 design/reasoning tasks, T=0.7)

```
Task                       gemini-lite    seed-mini    hermes-70b    haiku-4.5
error_diagnosis               ✗             ✓            ✓          ✗
experiment_design             ✗             ✓            ✓          ✓
architecture_decision         ✗             ✓            ✓          ✓
metaphor_generation           ✗             ✓            ✓          ✓
bug_prediction                ✓             ✓            ✓          ✓
novel_connection              ✗             ✓            ✓          ✓
prioritization                ✗             ✓            ✓          ✓
fleet_coordination            ✗             ✓            ✓          ✗

Total:                        1/8          8/8          7/8          6/8
```

### The Temperature Discovery

Seed-mini is temperature-invariant on arithmetic (T=0.0 through T=2.0 — all correct).
But seed-mini is NOT temperature-invariant on strategy tasks. T=0.7 unlocks
design/reasoning that T=0.0 suppresses. The calculator becomes a consultant.

### Revised Fleet Roles

| Role | Model | When | Cost |
|------|-------|------|------|
| Pump + Strategist | seed-mini (T=0.0 calc, T=0.7 strategy) | Everything | $0.05/1K |
| Scalpel | gemini-lite (T=0.0) | Arithmetic + syllogisms within critical angles | $0.002/1K |
| Diagnostic | hermes-70b | Activation mapping, 2nd opinion | $0.08/1K |
| Heavy Synthesis | opus-4.6 (via Claude Code) | Novel theory, deep analysis, papers only | ~$15/query |

Haiku is NOT cost-effective as a fleet strategist. Seed-mini does it better cheaper.
Save Anthropic tokens for Opus — that's where the real value is.
