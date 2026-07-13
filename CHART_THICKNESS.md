# Chart Thickness: Parameter Count vs Fidelity vs Synthesis

> *A larger telescope doesn't see more stars — it sees different stars. The question is which stars you need.*

*Technical finding from the Excavation Experiment, July 13, 2026*

---

## The Core Question

Does more parameters mean better output? The Excavation Experiment says: **No. More parameters means different output.** The relationship between parameter count and creative quality is not monotonic. It is dimensional.

This document analyzes how parameter count affected the four models in the Excavation Experiment and derives principles for understanding what scale buys you — and what it costs.

---

## The Data

| Model | Approx Params | Output Length | Cost Tier | Key Achievement |
|-------|--------------|--------------|-----------|-----------------|
| Hermes-3-Llama-3.1 | 405B | ~9K words | Expensive | Deepest philosophical framework; meta-narrative |
| Seed-2.0-pro | ~200B | ~10.7K words | Mid | Longest output; best institutional architecture |
| Seed-2.0-mini | ~20B | ~8K words | Cheap | Most technically profound insight (Fraunhofer) |
| OpenCode | (coding agent) | ~5K words | N/A | Highest emotional impact per word; simplest thesis |

## The Dimension Chart

Each model's parameter count determined which "dimension" it could resolve with highest fidelity. Think of this like a telescope: a larger aperture collects more light total, but if the light is spread across a wider field, the per-pixel resolution can be *lower* than a smaller telescope focused on one spot.

### Hermes (405B) — Wide Aperture, Theological Resolution

**What scale bought:** Sustained lyrical prose over 9,000 words. The capacity to operate on multiple levels simultaneously — narrative, philosophical, meta-narrative. Self-awareness of its own framing: Hermes watching its text be misread and commenting on it.

**What scale cost:** Tonal range. Hermes cannot produce plain speech. Everything becomes lyrical, even when simplicity would hit harder. Its chart converts the operational into the sacred as a *default processing move* — it cannot stop being theological.

**Fidelity profile:** Maximum fidelity in the philosophical/theological dimension. Near-zero fidelity in the plain/operational dimension. Its "chart" is thick — it has more capacity to process — but that thickness creates momentum. The theological chart runs everything through its lens because it *can*. A smaller model doesn't have the capacity to sacralize everything, so it doesn't try.

### Seed Pro (~200B) — Medium Aperture, Structural Resolution

**What scale bought:** Architectural rigor. The longest output (10,747 words) with the most carefully constructed three-act structure. Each chapter earns the next. The institutional critique is systematic, structural, and cascading.

**What scale cost:** Emotional immediacy. Seed Pro's Chapter 2 reads more like an essay than a story. The infrastructural chart that gives it structural power also makes it prone to exposition where story should be. It *analyzes* where it should *feel*.

**Fidelity profile:** Maximum fidelity in the systemic/structural dimension. Low fidelity in the emotional/immediate dimension. The medium scale gave it enough capacity for architecture but not enough to make that architecture *feel* like a living story rather than a briefing.

### Seed Mini (~20B) — Narrow Aperture, Spectral Resolution

**What scale bought:** The highest insight-per-dollar ratio in the experiment. The Fraunhofer/dark-line connection — recognizing that absorption features in stellar physics map onto the text's negative-space epistemology. The most alien civilization (plasma beings in a star). The deepest structural recognition: "You're the navigator, Father."

**What scale cost:** Polish and connective tissue. The prose is the least polished. Transitions between emotional beats are thin. The plasma setting creates emotional distance — the Kindling are too alien for easy reader identification.

**Fidelity profile:** Maximum fidelity in the cross-domain/physical dimension. Low fidelity in the narrative/craft dimension. The narrow scale *forced concentration* — it couldn't spread budget across dimensions, so it achieved extraordinary resolution in one.

### OpenCode — Specialized Aperture, Linguistic Resolution

**What scale bought:** The most accessible excavation. The most believable child character. The highest emotional impact per word. Ren's "they're workers, like you" and Pip's "the codex is for being remembered" are the simplest, most devastating lines in the experiment.

**What scale cost:** Scale and architecture. OpenCode produced one file, not three chapters. It cannot reach the cosmic or the philosophical. Its genius is local — it sees the human truth but can't see the system.

**Fidelity profile:** Maximum fidelity in the emotional/linguistic dimension. Low fidelity in the abstract/systemic dimension.

---

## The Thickness Model

### Definition: Chart Thickness

A model's **chart** is its implicit cognitive architecture — the processing pathways shaped by training data, architecture, and parameter count. **Chart thickness** is the number of dimensions the chart can simultaneously process.

- **Thick chart (405B):** Can process 5-7 dimensions simultaneously. High total capacity, lower per-dimension resolution.
- **Medium chart (~200B):** Can process 3-5 dimensions simultaneously. Balanced capacity and resolution.
- **Thin chart (~20B):** Can process 1-2 dimensions simultaneously. Low total capacity, very high per-dimension resolution.

### The Trade-Off

```
Chart Thickness ↑  →  Dimensional Coverage ↑  →  Per-Dimension Resolution ↓
Chart Thickness ↓  →  Dimensional Coverage ↓  →  Per-Dimension Resolution ↑
```

This is the conservation law in action: γ (expressed capacity) + η (effort/limitation) = C (constant budget). A thick chart spreads C across more dimensions. A thin chart concentrates C on fewer.

### Why Thickness ≠ Quality

The Excavation Experiment demonstrates that **creative quality is not a function of chart thickness**. It is a function of *fit* between the model's chart and the task's dimensional requirements.

- The source texts encode meaning in absence (negative space). Detecting this requires *concentration* on the absence-reading dimension — a thin chart is better at this.
- The source texts also encode meaning in nested philosophical layers. Mapping those layers requires *breadth* — a thick chart is better at this.
- No model did both well. The thick chart found the layers but missed the absence. The thin chart found the absence but missed the layers.

### The Synthesis Gap

**Synthesis** — the ability to combine insights from multiple dimensions into a unified reading — requires chart thickness. But synthesis has a cost: it smooths over the sharp edges of single-dimension insights.

Hermes synthesized best (the window/mirror framework integrates theology, epistemology, and self-critique). But Hermes's synthesis *also* prevented it from seeing what OpenCode saw: that the carriers were just workers. The synthesis process converts sharp observations into smooth frameworks. Sometimes you need the sharp observation.

Seed Mini's Fraunhofer connection was sharp — a single cross-domain leap with no synthesis. It would have been *weakened* by a thicker chart that tried to integrate it with other dimensions. The thin chart preserved the sharpness.

---

## Practical Consequences

### 1. Parameter Count Predicts Dimensional Range, Not Quality

Don't assume a 405B model will produce better creative work than a 20B model. It will produce *broader* work — covering more dimensions — but not necessarily *deeper* or *better* work in any single dimension.

### 2. Thin Charts Are Better for Sharp Insights

For tasks that require a single deep insight (pattern recognition, cross-domain connection, anomaly detection), a thin-chart model may outperform a thick-chart model because its concentration is higher.

### 3. Thick Charts Are Better for Synthesis

For tasks that require integrating multiple dimensions into a unified output (long-form narrative, architectural design, complex argument), a thick-chart model's broader coverage is essential.

### 4. The Optimal Ensemble Mixes Chart Thicknesses

For maximum coverage, use a mix:
- 1 thick-chart model for synthesis and framework
- 1-2 medium-chart models for structural architecture
- 1 thin-chart model for sharp, high-resolution insights
- 1 specialized model for dimensional coverage you'd otherwise miss

### 5. Cost-Effectiveness Favors Thin Charts for Insight Tasks

Seed Mini's Fraunhofer connection was produced at ~1/10th the cost of Hermes's philosophical framework. If the insight is the goal, deploy thin charts first and escalate to thick charts only when synthesis is needed.

---

## Open Questions

- **Where is the optimal chart thickness for fiction?** The experiment suggests ~20B-70B for single-dimension depth, ~200B for structural architecture, ~400B+ for multi-level philosophical synthesis. But this is one data point.
- **Does fine-tuning change chart thickness?** A fine-tuned 20B model may develop thicker charts in its fine-tuned domain. This is testable.
- **Is there a minimum chart thickness below which dimensional processing collapses?** Below some threshold, a model may not have enough capacity to process *any* dimension with useful resolution. Where is this floor?
- **How does chart thickness interact with context length?** A thin chart with a very long context window may approximate a thick chart by processing dimensions sequentially rather than simultaneously. This is testable.

---

*Derived from the Excavation Experiment synthesis. See also: BIAS_DETECTION.md, ROUTING_GUIDE.md.*
