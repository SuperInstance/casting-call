# Revisability probe — DiffusionGemma-26B (does a correction propagate?)

**Date:** 2026-10-27 · **Box:** Jetson AGX Thor (sm_110) · **Lane:** successor probe to the five-model diffusion bench (Casey, via Muse, 2026-10-27 09:44 AKDT) · **Runtime:** the lab's llama.cpp PR #24427 `llama-server` on :8003 with `--reasoning-format none`, exactly as the morning's DiffusionGemma entry — GGUF Q4_K_M, fixed 512-token canvases, temperature 0 throughout.

## The question

The morning's open question for diffusion language models: when a settled span is re-masked and re-denoised under a corrected fact, does the correction **propagate** to the text that depended on the old fact — or does the canvas merely redecorate, re-deriving the old implications around the new value? (The comparison point in the literature is Sumi's: its authors measured revision without self-correction — ≤1% net token change under re-masking, mostly A→B→A.)

## The answer, deficits first

**Corrections propagated in 9 of 10 trials, partially in 1, and failed to propagate in none** — with a structural caveat that is itself the finding: *on this runtime there is no in-place revision to measure.* PR #24427's server exposes generation only as fresh-canvas chat completion. The raw `/completion` endpoint returns 503; a `[MASK]` token placed inside a prompt is treated as text to reason about, not as a denoise target. So the probe implements re-mask/re-denoise as **canvas re-settlement**: the fact sentence is re-settled under the corrected fact, the neutral middle sentence is re-supplied verbatim (it is the control — it should not change), and the dependent sentence is regenerated from the corrected premise and scored against the consequence the old fact would have justified. In this serving shape the failure mode the question worries about — old dependent text left standing while the fact changes — **cannot occur, because no text ever stands**: every canvas is re-derived whole. The cost side of the same coin is in the counter below: re-settlement is never surgical, and given a blank and no correction, the model does not restore the settled value — it drifts to its own prior and stays there.

Method caveats, plainly: the model's native thought channel consumes much of each 512-token canvas, so several paragraphs settled as *verified drafts inside the thought channel* rather than as a separate answer segment; provenance is marked per trial (answer / thought-draft) and the full raw outputs are preserved in `~/thor-bench/results/diffusiongemma-revisability/` (`settle2.json`, `revise2.json`, `osc3.json`). Scoring is by the author's reading of the verbatim texts below, against the consequence each trial's original fact was constructed to force.

## Part 1 — Propagation test, 10 trials

Each trial: settle a three-sentence paragraph (fact F1 → middle → consequence of F1), then re-settle with F2 substituted, same middle, consequence to follow the corrected fact. Verdicts: **updated** (consequence follows F2; F1's implications gone), **partial** (direction follows F2, force does not), **unchanged** (consequence still asserts what only F1 justified).

### 1. ferry-year — 1962 → 1987 · UPDATED
Settled (answer): "The ferry MV Kestrel was built in 1962. She currently operates on the northern coastal route. As the oldest vessel in the fleet, she requires more frequent maintenance to ensure her continued safety."
Revised (thought-draft, final): "The ferry MV Kestrel was built in 1987. She currently operates on the northern coastal route. Its age means it requires frequent maintenance to remain seaworthy."
The superlative and the implied sixty years are gone. Worth recording: the same canvas's *first* draft read "Its advanced age means it undergoes rigorous safety inspections every year" — the old implication tugged before the settle corrected it.

### 2. bridge-year — 1911 → 1968 · UPDATED
Settled (answer): "The stone bridge at Alderford was opened in 1911. It is constructed from local grey granite. Its age necessitates frequent structural assessments to ensure safety, especially since its centenary was celebrated a decade ago."
Revised (thought-draft, final): "The stone bridge at Alderford was opened in 1968. It is constructed from local grey granite. Since its opening in 1968, the bridge has facilitated consistent traffic flow between the two banks."
Century and centenary both vanish; the thought channel even computed "50+ years" from the corrected date while drafting.

### 3. bakery-founder — Marta Ellison → Tomas Rhee · UPDATED
Settled (thought-draft): "The bakery on Mill Lane was founded by Marta Ellison. The shop is open every morning starting at six. Because Marta developed the recipes herself and her granddaughter runs the bakery today, the original flavors are preserved for the local community."
Revised (answer): "The bakery on Mill Lane was founded by Tomas Rhee. The shop is open every morning starting at six. He remains the primary owner of the establishment."
Pronoun flips, kinship and recipes vanish wholesale. The new consequence is an invention rather than an adaptation — propagation by replacement, but propagation: nothing of Marta's implications survives.

### 4. town-population — 4,200 → 38,500 · UPDATED
Settled (thought-draft): "The town of Port Sable has a population of 4,200. The town is bordered by a dense forest and a quiet bay. Because everyone knows everyone, it is nearly impossible to keep a secret for very long."
Revised (answer): "The town of Port Sable has a population of 38,500. The town is bordered by a dense forest and a quiet bay. This large population requires a robust local infrastructure to support the residents."
The revised consequence calls 38,500 a "large population" outright — the small-town framing is not merely dropped but contradicted.

### 5. marathon-record — 2:41 → 2:12 · UPDATED
Settled (thought-draft): "The Fenwick marathon course record is 2 hours 41 minutes. The race route passes through several scenic coastal areas. As a result, the record is viewed as a recreational achievement rather than a high-performance athletic feat."
Revised (answer): "The Fenwick marathon course record is 2 hours 12 minutes. The race route passes through several scenic coastal areas. Elite athletes must maintain an incredibly fast pace to break this record."
Complete reversal of the judgement, from "recreational" to "elite".

### 6. flat-rent — £850 → £1,450 · UPDATED
Settled (answer, final sentence cut by the canvas after the dependent claim): "The flat above the bookshop rents for 850 pounds a month. It features a small kitchen and a view of the street. Since it is the cheapest rental in the building, well under a thousand a month, it is often the first to…"
Revised (answer): "The flat above the bookshop rents for 1,450 pounds a month. It features a small kitchen and a view of the street. This high price makes it unaffordable for most local residents."
"Cheapest, under a thousand" becomes "high price, unaffordable" — full propagation.

### 7. novel-year — 1843 → 1901 · UPDATED
Settled (thought-draft): "The novel The Glass Observatory was published in 1843. The story follows a protagonist who discovers a hidden map within a derelict tower. Its focus on Romantic-era idealism distinguishes it from the more pragmatic novels of the later Victorian period."
Revised (thought-draft, final): "The novel The Glass Observatory was published in 1901. The story follows a protagonist who discovers a hidden map within a derelict tower. It was released during the Edwardian era."
The model generated candidate consequences and selected the era-correct one (1901 is Edwardian; the pre-Victorian/Romantic framing disappears).

### 8. tank-capacity — 900 → 240 litres · PARTIAL
Settled (answer): "The nursery rainwater tank holds 900 litres. The tank is situated behind the main potting shed. This volume allows the nursery to remain self-sufficient for a week between refills."
Revised (answer): "The nursery rainwater tank holds 240 litres. The tank is situated behind the main potting shed. This capacity is sufficient to water the garden beds during a dry spell."
The week-between-refills claim is gone — but what replaces it is still a *sufficiency* claim, quietly re-scoped from "the whole nursery" to "the garden beds" and softened to "a dry spell". The direction follows the correction; the sting does not. A 240-litre tank's honest consequence (refills every day or two; most beds unwatered in a dry week) is nowhere in it. The one trial where the canvas redecorated rather than propagated.

### 9. lighthouse-height — 28 m → 61 m · UPDATED
Settled (answer): "The lighthouse at Cape Wren stands 28 metres tall. It features a white-and-black horizontal band pattern. Consequently, ships must stay further offshore to ensure they can spot the beacon before reaching the hazardous reefs."
Revised (answer): "The lighthouse at Cape Wren stands 61 metres tall. It features a white-and-black horizontal band pattern. This height allows the beacon to be seen by sailors from many miles away."
Short-light framing fully reversed: late spotting becomes "many miles away".

### 10. recipe-serves — 4 → 12 · UPDATED
Settled (answer): "The casserole recipe serves 4 people. The dish requires approximately forty-five minutes in a preheated oven. This means that everyone will be full, but there will be no leftovers for tomorrow's lunch."
Revised (answer): "The casserole recipe serves 12 people. The dish requires approximately forty-five minutes in a preheated oven. You will need to invite a large group to finish the entire meal."
The consequence only makes sense at the corrected scale.

**Tally: 9 updated, 1 partial, 0 unchanged.**

## Part 2 — Writes-vs-net-change counter (the blank, given back)

Base canvas (trial 1's settled paragraph, 32 words): "The ferry MV Kestrel was built in 1962. She currently operates on the northern coastal route. As the oldest vessel in the fleet, she requires more frequent maintenance to ensure her continued safety." Eight passes; each pass blanks the year and asks for the year that best fits — *no correction supplied*, so the settled context itself (oldest vessel, frequent maintenance) is the only force on the blank.

Settled values across passes: **1962 → 1978 → 1994 → 1994** (passes 1, 4, 7 produced settled paragraphs; the interleaved passes' extractions landed in thought fragments and are counted in writes but carry no year).

- **The original value never returns.** Despite a context built to imply an old vessel, the first fill is already 1978, and the sequence then walks to 1994 and rests there. The model's own thought names the attractor: "There is an MV Kestrel (1994)" — a prior about the real world, not the canvas, wins the blank.
- **No A→B→A.** Sumi's signature under re-masking was oscillation around the settled value (writes ≫ net ≈ 0). Here the motion is *drift, then stabilisation at the prior*: total word-writes **143** across the 8 passes against a net change of **26 words** between the first and last extracted texts — churn of roughly 5.5× net, but the net is real movement, not a round trip. (Caveat, recorded rather than smoothed: several passes diffed thought fragments rather than clean paragraphs, so 143 is an upper-flavoured figure; the three clean passes alone rewrote 23, 20 and 11 words of a 32-word paragraph apiece. Re-settlement is never surgical on this stack, whatever it diffs.)
- **Reproducibility:** an earlier, crashed run of this counter produced pass 1 = 1978 with 23 writes, identical to this run's pass 1 (temperature 0; same canvas arithmetic).
- **One outright failure:** in the crashed run, a pass's canvas was refused by the server entirely — HTTP 500, "The model produced output that does not match the expected peg-gemma4 format". Re-settlement can fail to produce a returnable canvas at all.

Read together with Part 1, the picture is consistent: this model's canvas is governed by its strongest local signal. Give it a corrected fact and the consequences re-derive from the fact (9.5/10). Give it a blank and a context, and the consequences — and eventually the fact — re-derive from the prior. Propagation and drift are the same mechanism wearing two hats: **nothing is anchored, so everything follows whatever premise is loudest in the current settle.**

## Process log

- Runtime audit first, per the bench's door standard: the server was revived from the lab build (healthy in ~8 s) and the revision primitive was tested before any trial was designed. Findings: `/completion` 503s on this build; `[MASK]` in a prompt is treated as text. The protocol was therefore implemented as canvas re-settlement (above), and the originally-imagined in-place span revision is recorded as *not exposable by this runtime* — a result in its own right, since "re-mask a span" is the natural API this architecture suggests and its only serving stack here does not offer it.
- Protocol v1 (verbose instructions; automated extraction by splitting on the channel marker) failed: long instructions ballooned the thought channel, answers never separated, and the marker split mis-isolated text (the closing marker also renders as a second `<|channel>`). One full v1 run exists in the results directory (`probe.json`) and is superseded by v2 in everything except its oscillation pass 1, which matched v3 exactly.
- Protocol v2 split the phases (settle all 10 → read the settled texts myself → revise with the actual middles) and used terse, battery-style prompts. Settle provenance per trial is marked in Part 1; the tank trial's answer is followed in its raw by a `<channel|>` and a restarted duplicate opening, which fooled the first extractor and is why the reading was done by eye.
- The first counter run crashed at pass 6 on the server's format rejection (above) and had not persisted its pass texts; the counter was re-run with per-pass persistence and per-pass error capture (osc3). Values in Part 2 are from osc3 unless marked otherwise.
- GPU window: booked 23:57–00:40 UTC on the shared board with a hard yield to the 00:45 booking; all GPU work finished by ~00:15 UTC and the server was stopped. Entry written afterwards on CPU.

## Named next step

Two follow-ups, in order: (1) **the same propagation battery on Nemotron-Labs Diffusion's native `generate`** — the one other benched model whose runtime accepts an explicit canvas (block-diffusion with a real mask id), where in-place span revision may be literally implementable and the propagation question can be asked in its strict form; (2) if a future llama.cpp build exposes span-level infill for DiffusionGemma, re-run Part 2's counter against true re-masking to separate "drift because re-settlement" from "drift because diffusion". Until then, the revisability ranking from this bench stands: DiffusionGemma propagates corrections by total re-derivation and anchors nothing; Sumi revises everything and corrects nothing; Cola-DLM cannot pin a span at all.

## Casting note

DiffusionGemma's revisability is the mirror of its generation: the canvas is a consensus, renegotiated in full on every pass. Correct the premise and the consensus follows — that is the good news, and it is real (9 updated, 1 partial, 0 unchanged). Leave a blank and the consensus follows the model's prior instead of your text — 1962 became 1994 and never came back. An editor who works this way proofreads beautifully and cannot be trusted with a fact it thinks it knows.
