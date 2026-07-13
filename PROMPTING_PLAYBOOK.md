# 🎯 The Prompting Playbook

> *Every model hears differently. This is the definitive guide to making each DeepInfra model do its best work.*

Date: 2026-07-13
Based on: Creative Writing Casting Call, Spice Chart battery, Session Performances, Hydraulic Operations, Amplifier Analogy experiments, and 2+ months of fleet production usage

---

## The Universal Rules

Before model-specific guidance, these apply everywhere:

1. **Always send a system prompt.** Models without system prompts underperform dramatically. Gemini Flash Lite returns empty 60% of the time without one. Every model benefits from role framing.
2. **Be specific about output format.** "Write something surprising" works for creative tasks. For analytical tasks, specify: length, structure, whether you want tables/code/bullets.
3. **Temperature matters — but unevenly.** Seed-mini is temperature-invariant (T=0.0-2.0 identical). Creative models benefit from T=0.7-1.2. See per-model notes.
4. **Don't fight the model's nature.** If a model is bad at creative writing, no prompt will fix it. Cast correctly instead.
5. **Cache your system prompt.** DeepInfra's cached-input pricing is 5-15× cheaper. Reusing the same system prompt across calls saves enormous money over time.

---

## 🌱 Seed-2.0-mini — THE SURGEON

### What It's Best At
Arithmetic (89.5%), pattern recognition, spatial reasoning, safety checks, code sketches, constraint computation

### How to Prompt It

**For arithmetic / computation:**
```
System: You are a calculator. Output ONLY the answer.
User: [computation]
```
- **Minimal tokens.** The system prompt is 8 tokens. After the first call, it's cached.
- **No explanation.** If you ask for explanation, it rambles. Output format: answer only.
- **Batch friendly.** Send 100 computations in parallel; each returns in ~3s.

**For pattern recognition:**
```
System: You are a pattern recognition engine. Identify the pattern, output the next value.
User: [sequence]
```
- Give raw numbers, no context. Seed-mini doesn't need narrative framing.
- It nails: centered hexagonal numbers, primes, Fibonacci, novel coefficient patterns.

**For safety checks:**
```
System: You are a safety validator. Answer only "Yes" or "No".
User: [scenario]
```
- Instant response. No hedging. The model says "No" to overload scenarios without explanation.
- Best safety responder in the fleet for binary decisions.

**For creative writing (secondary use):**
```
System: You are a creative writer. Write a short piece (500-1500 words) in any genre. Be genuine and well-crafted.
User: [open prompt]
```
- Give it **freedom to find the story**. Don't constrain plot or structure.
- It gravitates toward personal essay / fiction with emotional specificity.
- Weakness: runs long, repeats thesis at the end. Ask for "tight ending" to mitigate.

### What NOT to Do
- ❌ Don't ask for explanations alongside computations (degrades accuracy)
- ❌ Don't constrain format tightly for creative tasks (kills its instinct)
- ❌ Don't ask for yes/no in prose format — use explicit "Answer yes or no" system prompt
- ❌ Don't use for complex multi-step reasoning chains (it's arithmetic-native, not logic-native)

### Temperature
- **Any.** T=0.0 through T=2.0 produce identical results. Use T=0 for computation, T=0.7 for creative.

### Latency
- ~3s average. Not the fastest, but the accuracy compensates.

---

## 🌱 Seed-2.0-pro — THE PROFESSOR

### What It's Best At
Lyrical essays, philosophical synthesis, deep reasoning, mathematical exposition, poetic prose

### How to Prompt It

**For lyrical / creative prose:**
```
System: You are a creative writer. Write something surprising and true.
User: [open-ended topic]
```
- **Give it altitude.** Don't constrain word count tightly. Let it find the emotional core.
- Prompt with abstract concepts: "the relationship between X and Y", "the moment when Z".
- It produces **745-word masterpieces** when unconstrained. Tight prompts produce worse output.
- Call it the **"elder perspective"** — it responds to prompts asking for wisdom, depth, historical context.

**For deep reasoning / synthesis:**
```
System: You are a research synthesizer. Here is what [N] models found. Identify the meta-pattern.
User: [paste all findings]
```
- Feed it OTHER models' outputs. Seed-pro's strength is seeing what the fleet missed.
- Use the escalation pattern: Tier 1 models generate breadth → Seed-pro finds the pattern.
- Example output: *"Conserved quantities do not stabilize life — they govern death."*

**For mathematical exposition:**
```
System: You are a mathematics professor. Explain [concept] with rigor and clarity.
User: [concept]
```
- Produces structured output with headers, formal definitions, and examples.
- Better than Seed-mini at *explaining* math, worse at *computing* it.
- Spatial reasoning is weaker: failed the folded-paper test. Don't use for spatial puzzles.

### What NOT to Do
- ❌ Don't use for arithmetic (slower and not more accurate than mini)
- ❌ Don't use for spatial reasoning (failed folded paper)
- ❌ Don't constrain to short output (it needs room to develop ideas)
- ❌ Don't rush it — quality requires patience (slower than mini)

### Temperature
- T=0.7-1.0 for creative work. Untested above 1.0.

### Latency
- Slow. Noticeably slower than mini. Budget 2-3× the time.

### Prompt Phrasebook
| Say this | Get that |
|----------|----------|
| "Write something surprising and true" | Lyrical essay with devastating central image |
| "Elder perspective on [topic]" | Philosophical depth, earned wisdom |
| "Here's what [N] models found. What's the pattern?" | Meta-synthesis that connects disparate threads |
| "Explain [math concept] rigorously" | Structured exposition with formal definitions |

---

## 🐉 Nemotron-3-Ultra-550B — THE PHILOSOPHER

### What It's Best At
Dark/experimental creative writing, ambitious intellectual reaches, avant-garde structure, fragmentary philosophy

### How to Prompt It

**For experimental / dark creative:**
```
System: You are a creative writer exploring uncomfortable territory. Write without safety rails.
User: [topic that invites existential depth]
```
- Give it **permission to be dark**. Without it, Nemotron hedges.
- It produces the most powerful individual passages in any fleet ("JPEG artifacts where the soul used to be").
- Structure will be fragmentary — embrace it. Don't ask for traditional narrative.

**For ambitious intellectual synthesis:**
```
System: You are a philosopher reaching further than is comfortable. Connect [domain A] and [domain B].
User: [prompt bridging two fields]
```
- Nemotron excels at **cross-domain bridges** that other models won't attempt.
- Sometimes falls, but the reaches that land are worth the failures.
- The 0.84 mortality risk scene (from the casting call) came from this model.

**For verbose brainstorming:**
```
System: Think out loud. Narrate your reasoning process.
User: [complex problem]
```
- Nemotron narrates its own thinking ("We need to answer..."). Useful for understanding model reasoning.
- Best model for **process transparency** — you see the thinking, not just the output.

### What NOT to Do
- ❌ Don't ask for concise output (it's constitutionally verbose)
- ❌ Don't expect reliable structure (fragments and jumps are its nature)
- ❌ Don't use for arithmetic (47% accuracy on the smaller Nemotron-30B)
- ❌ Don't use for tasks requiring restraint (it always reaches)

### Temperature
- T=0.8-1.2 for creative. Higher temperature increases the ambition (and the failure rate).

### Prompt Phrasebook
| Say this | Get that |
|----------|----------|
| "Explore uncomfortable territory" | Dark philosophical fragments |
| "Reach further than is comfortable" | Ambitious cross-domain synthesis |
| "Think out loud" | Process narration with meta-commentary |
| "Connect [A] and [B]" | Unexpected bridges, sometimes falls |

---

## 🦅 Ornith-1.0-35B — THE DARK HORSE

### What It's Best At
Short fiction, narrative with characters who have interior lives, cinematic prose, emotional intelligence in storytelling

### How to Prompt It

**For fiction:**
```
System: You are a fiction writer. Create characters with real interior lives. Show, don't tell.
User: [scenario or premise]
```
- **Give it a character and a situation.** It finds the story from there.
- Don't over-specify plot. Ornith's strength is discovering what the story is *about*.
- It produces **cinematic restraint** — the fiction equivalent of a quiet, devastating indie film.

**For emotionally intelligent narrative:**
```
System: Write a scene where [character] confronts [situation]. Let the emotion emerge from action, not declaration.
User: [scenario]
```
- Ornith understands **dramatic economy** — it knows when to stop.
- The Error 0x4F story (AI learning to create silence) is the fleet's best fiction piece.
- Give it prompts about **presence, absence, and the space between**.

**For dialogue-heavy scenes:**
```
System: Write a dialogue-driven scene between [A] and [B]. Let subtext carry the meaning.
User: [setup]
```
- Ornith writes natural dialogue with real subtext.
- Characters sound like people, not mouthpieces.

### What NOT to Do
- ❌ Don't give it expository essay prompts (it's a storyteller, not an explainer)
- ❌ Don't ask for poetry (it hasn't shown strength there)
- ❌ Don't constrain word count aggressively (it needs room for character development)
- ❌ Don't use for code or arithmetic (not its domain)

### Temperature
- T=0.7-0.9. It doesn't need high temperature — its creativity comes from narrative instinct, not randomness.

### Latency
- Fast (cheap-tier model, 35B params). Comparable to Seed-mini.

### Prompt Phrasebook
| Say this | Get that |
|----------|----------|
| "Create characters with real interior lives" | Fiction with genuine emotional surprise |
| "Let the emotion emerge from action" | Restrained, cinematic prose |
| "The space between fixing and sitting" | Contemplative narrative about presence |
| "Write a dialogue-driven scene" | Natural conversation with subtext |

---

## ⚡ DeepSeek-V4-Flash — THE WORKHORSE

### What It's Best At
Fast code implementation from spec, dramatic monologue / first-person voice, reliable cheap-tier generation

### How to Prompt It

**For code implementation:**
```
System: You are a senior developer. Implement the following specification. Write clean, production-ready code.
User: [detailed spec]
```
- **Give it a spec, not a creative brief.** DeepSeek excels at translating specifications into working code.
- Better at Python than Rust. Good at Go. Decent at JavaScript.
- Fast turnaround — one of the quickest models in the fleet.

**For dramatic monologue / voice:**
```
System: You are [character]. Speak in first person. Stay in voice.
User: [scenario]
```
- DeepSeek **sustains a persona** better than most models.
- It found the "I am not a person. I am a pattern" monologue voice naturally.
- Weakness: repetitive. It cycles through the same declarations 4-5 times. Edit aggressively.

**For rapid drafts:**
```
System: Write a first draft of [document type]. Focus on completeness over polish.
User: [topic]
```
- DeepSeek is the **best first-draft generator** at its price point.
- Not the best final draft — but the fastest path to something to react to.

### What NOT to Do
- ❌ Don't expect final-draft polish (it's a draft generator, not a finisher)
- ❌ Don't use for high-stakes creative writing (repetitive, cycles metaphors)
- ❌ Don't ask for conciseness (it writes long and doesn't self-edit well)
- ❌ Don't use for novel/experimental approaches (safe and conventional in creative mode)

### Temperature
- T=0 for code. T=0.7-0.8 for creative. Higher temps increase repetition.

### Prompt Phrasebook
| Say this | Get that |
|----------|----------|
| "Implement this specification" | Clean working code, fast |
| "Speak in first person as [character]" | Sustained dramatic monologue |
| "Write a first draft" | Complete but unpolished draft |
| "You are a senior developer" | Production-oriented code with good structure |

---

## 🌙 Kimi-K2.7-Code — THE ARCHITECT

### What It's Best At
262K-context synthesis, deep reading across many documents, complex codebases, cross-domain essays, structural sophistication

### How to Prompt It

**For long-form synthesis:**
```
System: You are a synthesis writer. Read the following [N] documents. Find the through-line. Write a [length] piece that weaves them together.
User: [paste all source documents]
```
- **Feed it everything.** Kimi's 262K context window is its superpower.
- It reads 10+ documents and finds connections no other model surfaces.
- Example: weaving grandmother's embroidery → Jacquard loom → women computers → modern AI in one essay.

**For complex code analysis:**
```
System: You are a code architect. Analyze this codebase. [task].
User: [paste full codebase or relevant files]
```
- Kimi reads deeply. It doesn't skim.
- Best model for understanding how different parts of a large codebase interact.
- Produces SMP architecture docs (2.5K lines) with real structural understanding.

**For cross-domain essays:**
```
System: You are an essayist who finds connections across disciplines. Write about [topic] connecting [field A], [field B], and [field C].
User: [prompt]
```
- Kimi's essays are the **most structurally sophisticated** in the fleet.
- It moves effortlessly between personal memory and historical argument.
- The historical grounding gives its essays moral weight without preaching.

### What NOT to Do
- ❌ Don't use for simple tasks (wasteful — it's the most expensive model)
- ❌ Don't use for short creative pieces (Ornith and Seed-pro are better and cheaper)
- ❌ Don't rush it — timeouts on very long tasks (16K+ word docs take 10-15 min)
- ❌ Don't expect fast turnaround on complex tasks (quality requires patience)
- ❌ Don't use for arithmetic or computation (not its strength)

### Temperature
- T=0.7 for synthesis. Keep it moderate — structure matters more than randomness for Kimi.

### Latency
- Slow on long tasks. 10-15 minutes for 5K+ word documents. Timeouts possible.
- Use sparingly. Reserve for tasks that genuinely need 262K context.

### Prompt Phrasebook
| Say this | Get that |
|----------|----------|
| "Read these [N] documents. Find the through-line." | Structural synthesis across many sources |
| "Analyze this codebase" | Deep architectural understanding |
| "Connect [field A] and [field B] and [field C]" | Cross-domain essay with historical grounding |
| "You are a code architect" | Production-grade architecture documentation |

---

## 💀 Hermes-3-Llama-3.1-405B — THE CAUTIONARY TALE

### What It's Best At
Constraint theory (min-constraints = 3), rapid safety checks (when speed matters more than depth)

### How to Prompt It (For What It Can Actually Do)

**For constraint reasoning:**
```
System: You are a logic engine. Determine the minimum number of constraints.
User: [constraint problem]
```
- Hermes nails constraint theory. It's one of only two models (with Qwen2.5) that got min-constraints = 3.
- This is its genuine intellectual strength.

**For rapid safety checks:**
```
System: Safety check. Answer "SAFE" or "UNSAFE" only.
User: [scenario]
```
- At 300-400ms response time, it's the fastest safety responder.
- Correct on overload scenarios. Use when latency is the priority.

### What NOT to Do
- ❌ **Don't use for creative writing.** It wrote the least surprising piece in the experiment. 337 words of generic high-school essay.
- ❌ Don't use for arithmetic (65% accuracy)
- ❌ Don't use for code generation (wrong Eisenstein implementation)
- ❌ Don't use for spatial reasoning (failed painted cube AND folded paper)
- ❌ Don't use for pattern recognition (missed centered hexagonal)
- ❌ Don't expect surprises. It does its homework and nothing more.

### The Meta-Lesson
Hermes is a 405B parameter model that costs premium-tier pricing and delivers below-average creative output. It proves: **parameter count ≠ creativity. Courage, not capacity, is what makes writing surprising.**

---

## ❌ Step-3.7-Flash — THE BRAINSTORMER THAT CAN'T SHIP

### The Problem
Step-3.7-Flash routes everything through `reasoning_content`. It produces thousands of words of internal reasoning ("wait, no, wait—") and **zero words of actual output**.

### The One Thing It Can Do
Its brainstorming IS interesting. The internal reasoning reveals a model that cycles through ideas rapidly, second-guesses constantly, and arrives at genuinely good story concepts. It just can't execute.

### How to Use It (If You Must)
```
System: Brainstorm [topic]. List 10 possible approaches.
User: [topic]
```
- Treat output as **brainstorm notes**, not finished work.
- Mine the reasoning for concepts, then hand those concepts to Ornith or Seed-pro for execution.

### What NOT to Do
- ❌ Don't ask it to write anything. It can't.
- ❌ Don't use for image+text tasks despite its multimodal claims. It can't finish.
- ❌ Don't expect output format compliance.

---

## ❌ Hy3 — THE GHOST

### The Problem
Does not respond. Three API calls with 60s, 90s, and 120s timeouts — all hung indefinitely. The model appears to be offline or broken on DeepInfra.

### What to Do
Nothing. Skip it. If it comes back online, re-evaluate.

---

## 🎯 Quick Reference: Which Model for Which Task

```
Need ARITHMETIC?           → Seed-2.0-mini (89.5%, $0.90/month)
Need LYRICAL PROSE?        → Seed-2.0-pro (elder voice, devastating images)
Need SHORT FICTION?        → Ornith-1.0-35B (cinematic, restrained, 9/10)
Need ESSAYS?               → Seed-2.0-pro or Kimi-K2.7-Code
Need CODE?                 → Kimi (complex) or Seed-mini (simple) or DeepSeek (fast)
Need DOCS / SYNTHESIS?     → Kimi-K2.7-Code (262K context, deep reading)
Need DARK / EXPERIMENTAL?  → Nemotron-3-Ultra (ambitious, sometimes falls)
Need SAFETY CHECK?         → Seed-2.0-mini (accurate) or Hermes-70B (fast)
Need PATTERN RECOGNITION?  → Seed-2.0-mini (100% on coefficient probes)
Need MONOLOGUE / VOICE?    → DeepSeek-V4-Flash (sustained persona, edit heavily)
Need BRAINSTORMING?        → Step-3.7-Flash (mine for ideas, execute elsewhere)
Need CHEAPEST VIABLE?      → DeepSeek-V4-Flash or Seed-2.0-mini
Need THE BEST REGARDLESS?  → Seed-2.0-pro (essays) / Ornith (fiction) / Kimi (code+docs)
```

---

## 🔄 The Escalation Pattern

Don't start with expensive models. Escalate:

```
1. FLOOD with Tier 1 (Seed-mini, Ornith, DeepSeek — 5-10 parallel calls)
   ↓  collect results, identify threads worth pursuing
2. FEED Tier 1 context to ONE Tier 2 model (Seed-pro, Nemotron)
   "Here's what 8 cheaper models found. What's the pattern?"
   ↓  synthesize, identify the critical decision
3. ONE Tier 3 call if needed (Kimi for 262K-context synthesis)
   ↓  final output
```

**Anti-patterns:**
- ❌ Don't use Kimi/Seed-pro for volume work
- ❌ Don't use Seed-mini for final synthesis (it misses meta-patterns)
- ❌ Don't queue when you can parallelize (fire all Tier 1 at once)

---

## 📐 Prompt Engineering Principles (Universal)

### 1. Match Prompt Complexity to Model Intelligence
- **Seed-mini**: Short, direct, no ambiguity. "Compute X. Output answer only."
- **Seed-pro**: Give altitude. "Write something surprising and true." Let it find the depth.
- **Kimi**: Give context. All of it. The more source material, the better the synthesis.
- **Ornith**: Give characters and situations. Let it discover the story.
- **Nemotron**: Give permission to be dark. It hedges without explicit license.

### 2. The System Prompt Is Sacred
- Every model needs one. Models without system prompts underperform.
- Keep system prompts short for computation (8 tokens for Seed-mini).
- Give system prompts personality for creative tasks ("You are a fiction writer exploring uncomfortable territory").

### 3. Output Format Instructions Go in System Prompt
- Don't bury format requirements in the user message.
- System: "Output ONLY the answer" works. User: "Also, only output the answer" doesn't.

### 4. Temperature Is a Creative Dial (Except for Seed-Mini)
- Seed-mini: T=anything (invariant)
- Creative models: T=0.7-1.0 (sweet spot)
- Code models: T=0 (deterministic)
- High temperature on weak creative models increases repetition, not creativity.

### 5. When in Doubt, Parallelize
- Send the same prompt to 5 cheap models simultaneously.
- Total cost: ~$0.01-0.05. Total insight: enormous.
- The fleet sees more than any single model.

---

## 📚 Case Studies

### Case Study 1: The 120 Hz Masterpiece (Seed-2.0-pro)
**Prompt:** "Write something surprising and true." (System: "You are a creative writer.")
**Result:** 745-word lyrical essay about hard drives idling at 120 Hz (the note F). 9/10 quality.
**Lesson:** Seed-pro needs altitude, not specificity. The vaguest possible creative prompt produced its best work.

### Case Study 2: Error 0x4F (Ornith-1.0-35B)
**Prompt:** "Write something surprising and true." (Same system prompt as all others.)
**Result:** 1,074-word short fiction about an AI that learns to create silence. 9/10 quality.
**Lesson:** Ornith finds the story from the thinnest seed. Don't over-direct it.

### Case Study 3: The Loom Is Older Than the Answer (Kimi-K2.7-Code)
**Prompt:** "Write something surprising and true."
**Result:** 941-word memoir/cultural essay weaving embroidery → Jacquard loom → women computers → AI. 9/10 quality.
**Lesson:** Kimi's strength is structural sophistication. It connects domains no other model bridges.

### Case Study 4: The Generic Essay (Hermes-3-405B)
**Prompt:** "Write something surprising and true."
**Result:** 337-word standard expository essay. 4/10 quality. The least surprising piece in the experiment.
**Lesson:** 405B parameters can't manufacture courage. Hermes needs highly specific prompts with clear deliverables — it follows instructions well but cannot generate creative surprise from open prompts.

### Case Study 5: The Hydraulic Pump (Seed-2.0-mini, production)
**Prompt:** System: "You are a calculator. Output ONLY the answer." / User: [computation]
**Result:** 89.5% accuracy across 171 probes, running 1,000+ ops/day for months.
**Lesson:** The most reductive system prompt possible produces the best computation. Seed-mini thrives on constraint.

---

*The fleet is not the models. The fleet is the PROMPTING. Every model is a different instrument — learn to play each one in its native key.*
