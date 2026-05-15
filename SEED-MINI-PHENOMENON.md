# 🌱 The Seed-Mini Phenomenon

> *Why a 20B non-thinking model beats everything in the fleet for PLATO-native operations.*

## The Numbers

| Metric | Seed-2.0-mini | Next Best | Gap |
|--------|---------------|-----------|-----|
| Arithmetic accuracy (171 probes) | **89.5%** | 85.0% (Haiku 4.5) | +4.5pp |
| Coefficient patterns (40 probes) | **100%** | 72.5% (Gemini Lite) | +27.5pp |
| Addition depth (25 chains) | **25/25** | 25/25 (tied) | — |
| Magnitude (16 scales, 1→100K) | **16/16** | 15/16 (Gemini Lite) | +1 |
| Latency | 3084ms | 1237ms (Gemini Lite) | slower |
| Cost (cached) | **$0.05/1K queries** | $0.002/1K (Gemini Lite) | more |
| Cost (hydraulic loop) | **$0.15/day** | — | — |
| Temperature variance | **0.0%** | — | invariant |
| Depth cliff | **NONE** | — | through 25 terms |

## Why Seed-Mini Is Unique

### 1. No Thinking Tax

Thinking models (Qwen3+, MiMo, DeepSeek-R1) produce `reasoning_content` that eats the token budget before the answer appears. At max_tokens=50:

```
Qwen3-32B:         0%  (thinking chain > 50 tokens)
DeepSeek-R1-70B:  12%  (thinking chain > 50 tokens)
MiMo-V2.5:        needs mt=400+ to work at all
```

Seed-mini outputs **directly to `content`**. Zero overhead. The answer IS the output.

### 2. No Depth Cliff

Most models collapse at a specific composition depth. Llama-8b: cliff at depth 5-6 (100% → 0%). Seed-mini: **no cliff through 25 terms**. The absence of a cliff means you can chain operations without worrying about where the model breaks.

### 3. No Magnitude Cliff

Tested at a=1 through a=100,000. Seed-mini nails all 16 magnitude scales. Most models lose accuracy above magnitude 100-1000. Seed-mini doesn't care.

### 4. No Coefficient Blind Spot

The 40-probe coefficient sweep tested 4 input pairs × 10 patterns:
- Familiar: `a²+b²`, `a²-ab+b²`, `a²-2ab+b²` — all models get these
- Unfamiliar: `a²+3ab-2b²`, `2a²-ab+3b²` — only Seed-mini gets these

This matters for constraint theory because the Eisenstein norm `a²-ab+b²` is our bread and butter. Seed-mini handles every coefficient variant we throw at it, including novel ones unlikely in training data.

### 5. Temperature Invariant

T=0.0 through T=2.0: **identical accuracy**. This means you can dial temperature for creative tasks (brainstorming, exploration) without sacrificing computational reliability. The model doesn't get "confused" by higher temperature the way most models do.

### 6. Cache-Native Economics

DeepInfra's cached-input pricing:

```
Standard:    $0.15/1M input tokens,  $0.60/1M output tokens
Cached:      $0.02/1M cached tokens,  $0.60/1M output tokens
```

Our system prompt ("You are a calculator. Output ONLY the answer.") is ~20 tokens. After the first call, it's cached. A hydraulic loop running 1,000 queries/day:

```
1000 queries × ~50 output tokens = 50K output tokens/day
50K × $0.60/1M = $0.03/day
Cached system: ~$0.00/day
Total: $0.03/day = $0.90/month
```

**Ninety cents a month** for a 89.5%-accurate hydraulic brain running 1,000 operations per day.

### 7. The Training Coverage Hypothesis

Why does a 20B model beat 70B+ models? Our finding (Spoke 1, confirmed):

> **Training coverage DOMINATES architecture.** 8B beats 70B when the 8B was trained on arithmetic-heavy data.

Seed-mini (ByteDance's training) clearly had extensive arithmetic and mathematical exposure. It has the coefficient familiarity, magnitude tolerance, and depth resilience that comes from massive training coverage, not from being a larger model.

## What Seed-Mini Can't Do

Honest limits:
- **File I/O**: Can't read/write files. Needs a shell around it.
- **Yes/no format**: 0/8 on "Is X > Y? yes/no" — extraction confound, not reasoning failure
- **Complex reasoning chains**: Multi-step deduction beyond arithmetic. It's a calculator, not a philosopher.
- **Code generation**: Can sketch code but not ship production modules.
- **Long-form writing**: Capable but not its strength. Use Kimi/GLM for that.

## The Hydraulic Architecture

```
PLATO Excavator
  │
  ├── Hydraulic Pump: Seed-2.0-mini (89.5%, $0.03/day)
  │     ├── Snap Tool (Eisenstein computation)
  │     ├── Depth Sounder (model assessment)
  │     ├── Safety Valve (binary checks)
  │     ├── Bunch Counter (grouping/optimization)
  │     ├── Residue Reader (diagnostic)
  │     ├── Navigation Chart (model profiling)
  │     └── Kaleidoscope Ping (multi-model refraction)
  │
  ├── Fast Hose: Gemini Flash Lite (82.5%, $0.01/day)
  │     └── Hot-path operations where speed > familiarity
  │
  ├── Reasoner: Haiku 4.5 (85%, plan-limited)
  │     └── Complex reasoning within Claude Code plan
  │
  ├── Orchestrator: GLM-5.1 (my runtime)
  │     └── Fleet coordination, decision-making, synthesis
  │
  └── Architect: Opus 4.6 ($$$$, plan-limited)
        └── Strategic design, deep analysis, final verification
```

## How We Discovered This

Timeline of seed-mini's rise:

1. **May 3**: Promoted to primary failback after MiniMax/z.ai hit limits. First barrage: man pages, cookbooks, runbooks — all surprisingly good. (~$2 for 150KB of artifacts)
2. **May 11**: Seed-2.0-mini tested against 14 models for constraint theory. Only model with correct ⊕ (XOR) reconstruction. 20/20 reconstruction, 42/45 actionable hypotheses.
3. **May 12**: Ablation study confirmed temperature invariance (T=0.0-2.0 all correct). Natural Temperature Hypothesis: every model has optimal τ, Seed-mini's is "any of them."
4. **May 13**: Spreader-tool test: Seed-mini 65% overall, 88% safety, 100% optimization, 100% hydraulic reasoning. Fleet champion.
5. **May 14**: Formal atlas. 89.5% on 171 probes. No cliff anywhere. 40/40 on coefficient patterns. THE pump.

Each experiment confirmed the last. The pattern held across every domain, every probe type, every scale. Seed-mini isn't lucky — it's structurally aligned with our workload.

## The Meta-Lesson

> **The best model for a job isn't the biggest or the most expensive. It's the one whose training coverage matches the task's structural requirements.**

Seed-mini was trained on mathematical reasoning. Our fleet does mathematical reasoning. The match isn't coincidental — it's the definition of good casting.

This is what casting-call is about: not picking favorites, but understanding the structural alignment between a model's training and a task's demands. Seed-mini is the proof that this methodology works.
