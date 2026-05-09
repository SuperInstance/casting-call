# 2026-05-09 Model Evaluations — Narrative Workshop

## Experiment: Narrative Polish with Multi-Model Perspectives

**Method:** Fed the 183-line narrative "The Fleet Grows Itself" to 3 different models, each optimized for a different role. Compared outputs. Narrative asks each model to critique or enhance specific aspects of the boat-rigging-as-AI-coordination metaphor.

### Results Table

| Model | Role | Output Quality | Key Strength | Key Weakness | Would Cast For |
|---|---|---|---|---|---|
| Seed-2.0-mini (DeepInfra) | Creative breadth | 4/5 | Emotionally varied phrasings that hit the economic truth (hull cheap, refit expensive) across three distinct tones (reverent, pragmatic, defiant) | Outputs are paragraph-level and would need line-editing to match narrative style; didn't independently identify structural issues | Creative editor for specific passages, not structural overhaul |
| Nemotron-3-Nano (DeepInfra) | Skeptical critique | 2/5 | The *persona* (cynical boat captain) was well-executed linguistically — tough, direct, disdainful of buzzwords | **Hallucinated a completely different narrative.** Critiqued phrases ("the storm was a firewall", "the engine room hummed with blockchain") that do not appear in the provided text. The model responded to the *persona* and general topic but did not actually read the input narrative. | Not suitable for grounded critique. Useful only as a style/voice test. |
| GLM-5.1 (z.ai coding API) | Depth/structure | 5/5 | Precise, actionable structural analysis with specific recommendations: hierarchy of metaphors, front-load hermit crab, isolate Laman, ground P48 in digital twins, simplify cohomology | Some suggestions (digital twin framing) would shift narrative scope | **Lead structural editor.** Cast every time for complex architectural critique. |

### Key Findings

**1. Seed-2.0-mini: Strengths in Emotional Texture**
- Seed produced three genuinely distinct emotional tones for the same factual core (90-year boat, 5x hull price refit). The reverent version reads like a boatbuilder's confession; the pragmatic version sounds like a skipper on a dock; the defiant version channels someone who bet on a long shot and won.
- The model independently converged on the core economic insight: "the cheap foundational base only gets you a launch, but the deliberate, costly care of regular refits... is what carries it through 90 years."
- **Limitation:** Seed works at paragraph level, not narrative structure. It didn't flag the missing hermit crab frame or the cohomology integration problem. Temperature 0.85 produced vivid prose but with occasional repetition.

**2. Nemotron-3-Nano: Hallucinated Critique (Critical Finding)**
- The model was asked to critique the provided narrative but responded to a *different* text — one containing "the storm was a firewall," "the radar became my AI co-pilot," "the engine room hummed with blockchain." None of these appear in the actual narrative.
- **Implication:** For deep multimodal or reasoning models that process large context windows, check for hallucination. The Nemotron model generated a generic "tech-bro sea metaphor" critique from its training distribution rather than engaging with the provided text.
- The *persona* was well-executed (authentic sailor's voice, good cadence), but the content was irrelevant. Useful only for evaluating the model's *stylistic capability*, not the narrative itself.

**3. GLM-5.1: Structural Editor of Choice**
- Identified the narrative's core structural problem: **Metaphorical Ontological Overload** — the reader must sustain a triple mapping (AI → Math → Maritime) simultaneously, which causes translation fatigue.
- Gave five specific, implementable edits. The strongest: "Stop treating Math and Boats as equal partners. Make Boat Rigging the primary narrative lens (the what), and Math the underlying mechanism (the how)."
- **Key insight:** P48 (discrete integer math) feels bolted on to analog rigging. The solution: explicitly frame the rigging as a *digital twin* or *smart-rig* (like an America's Cup yacht) to bridge the discrete/analog gap.
- **Hermit crab insight:** The narrative needs to distinguish *acquisition cost* (cheap hull) from *maintenance cost* (expensive refit). This distinction is currently implicit but should be explicit.

### Suggestions Adopted vs. Rejected

**Adopted:**
1. **Front-load the hermit crab / 90-year boat** — Move the real-world anchor (90-year boat, 5x hull-price refit, 4 refits over 10 years) from the closing to the opening. It's not decorative; it's the economic thesis.
2. **Isolate Laman as a dedicated section** — Keep it focused on the "Goldilocks zone" of connections.
3. **Add explicit "hull vs. refit" economic distinction** — The narrative now directly states: hull = cheap, refit = expensive, that's how durable systems work.
4. **30-year horizon** — Insert the forward-looking statement: "In 30 years, someone will do the fifth refit. The boat will still float."
5. **Simplify cohomology** — Frame it as topological detection (closed loops, emergence as information), less algebraic jargon.

**Rejected:**
1. **Digital twin framing for P48** — Would require expanding scope beyond the current narrative's hardware-grounded voice. P48 is left abstract but better contextualized.
2. **Full restructure of math hierarchy** — The narrative intentionally keeps math visible to signal to technical readers. But math sections are now separated by clearer narrative headings.

### Updated Narrative
The polished narrative is at `superinstance-ai-pages/THE-FLEET-GROWS-ITSELF.md`

**Changes made:**
- **Added "The Boat That Won't Die" section** — Anchors the entire narrative with Casey's 90-year, 4-refit boat. The hull cost vs. refit cost (5x) is the economic thesis. The 30-year horizon is the punchline.
- **Added hermit crab framing** in the opening — "The crab doesn't build a new shell. It finds a good one and refits it."
- **Front-loaded the economic truth** — "Platform is cheap; the work is expensive. That's not a bug. That's the design."
- **Added "Turbo-Shell Levels" section** — Connects refit iterations to agent capability levels (Level 4 = Ensign = fleet-level coordination)
- **Strengthened cohomology bridge** — Now explicitly says "mathematics doesn't depend on any server, any cloud, any license" to ground the abstractions.
- **Added bio line** — Casey's fourth refit narrative detail (echo in closing)

### Model Architecture Observations

| Factor | Seed-2.0-mini | Nemotron-3-Nano | GLM-5.1 |
|---|---|---|---|
| Context adherence | Good | **Failed** (hallucinated) | Excellent |
| Creative generation | Strong | Strong (style only) | Moderate |
| Structural reasoning | Weak | Weak | **Strong** |
| Technical accuracy | Moderate | Weak | **Strong** |
| Temperature sensitivity | 0.85 (creative) | 0.7 (balanced) | 0.6 (focused) |
| Token utilization | Efficient | Loose | Efficient |
| Best role | Creative passages | Style tests only | Structural editing |

### For Future Workshops
- Always verify that "skeptical" models actually read the provided text before trusting their critique
- Seed-2.0-mini at temperature 0.85 is excellent for generating options but shouldn't be used for evaluation
- GLM-5.1 (via z.ai coding API) is the best structural editor of the three tested
- The persona-based approach (cynical captain) works for generating a particular voice, but the model must be grounded to the actual content
