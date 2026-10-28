# Propagation battery, strict form — Nemotron-Labs Diffusion 8B (can a correction revise in place?)

**Date:** 2026-10-27 · **Box:** Jetson AGX Thor (sm_110) · **Lane:** named successor to the DiffusionGemma revisability probe, which closed by naming this exact step · **Runtime:** the model loaded directly in-process (`~/ml/.venv`, transformers 5.20.2, bf16, temperature 0 throughout) — no server. Settle via the vendor `generate()` (diffusion mode, block_length 32, threshold 0.9); revision via token surgery plus a denoise loop over the model's own forward (mask_token_id 100). Raws in `~/thor-bench/results/nemotron-propagation/` (`probe.py`, `probe.json`, `counter.json`, logs).

## The question

The DiffusionGemma probe asked whether a correction propagates to text that depended on the old fact — and found that its runtime could not pose the question in its strict form: no in-place span revision exists there, so propagation was measured under whole-canvas re-settlement (9 updated / 1 partial / 0 unchanged, with churn as the price). Nemotron-Labs Diffusion was the one benched runtime with a real mask canvas. So, strictly: settle a paragraph, change **only** the fact in place, re-mask **only** the dependent span, pin everything else — does the dependent update?

## The answer, deficits first

**Propagation in the strict form: 1 updated, 9 partial, 0 unchanged — and the shape of the partials is the finding.** Nothing stale survives: with the old dependent masked out and everything else pinned, the old implication *cannot* remain (0 unchanged is guaranteed by construction, and held in fact). But the refilled span mostly does not draw the corrected fact's consequence either. It retreats — to physical specifications (ferry, bridge, tank), to generic description (bakery, town, recipe), to prestige filler (marathon), once to a different subject entirely (flat-rent drifts to the two-bedroom flat upstairs). Only the lighthouse dependent actually re-derives from the new fact (a 61 m light is "visible for 20 nautical miles"; the 28 m original would not be). Under re-settlement on DiffusionGemma, the whole canvas re-committed around the corrected premise and drew its consequences 9 times in 10. Under strict in-place revision, the span is filled by local likelihood against pinned surroundings, and the safest local text wins: **what survives a correction in strict form is consistency; what evaporates is implication.**

Two structural findings about the runtime, both first-class results:

- **The vendor `generate()` refuses the question.** Its signature is `generate(prompt_ids, max_new_tokens, block_length, threshold, …)` and it builds its canvas by appending fresh mask blocks after the prompt — there is no initial-canvas parameter and no way to hand it existing text to revise (read directly in `modeling_nemotron_labs_diffusion.py`). The strict battery therefore runs on the model's *native masking machinery* — its forward pass with `mask_token_id` and confidence-threshold unmasking, the same machinery `generate()` uses internally per block — with the canvas supplied by token surgery. The model's layers ship with `diffusion_lm` already true; the full-canvas bidirectional forward is its native regime, verified in a diagnostic before the run.
- **In-place revision is length-locked.** A masked span refills at exactly its original token count, so replacements that would need more room end mid-phrase (several revised dependents and the counter's fixed point terminate without punctuation: "…has a capacity of", "…waiting for"). Re-settlement never has this problem; it also never leaves anything else alone. The two failure geometries are mirror images.

Process deficits, plainly: the first launch wedged in model load under heavy box contention (CPU spinning, read_bytes frozen at 299 MB for 11 minutes; killed and relaunched in tmux, after which the identical load took ~2 minutes). The counter crashed at pass 3 on my own sentence-splitting assumption (a refilled span with no clean sentence boundary returned `None`); passes 1–2 had been persisted per-pass, the span location was rewritten to not need sentence boundaries (first year-regex match + everything after the pinned middle), and the counter resumed from its own file. Three settled dependents were weak before any revision (town-population's settled third sentence is a fragment — "One consequence of the town's small population."; novel-year's and bridge-year's are generic), so those trials measure a weak dependence; they are scored as run and flagged per trial. The marker screen used as scoring evidence produced one false positive (bakery: the substring "he " inside "The "), which is why the verdicts below are by reading, with the screen recorded in the raws.

## Method

Identical fact-pairs and verdict rubric to the DG probe. Each trial: **settle** — native `generate()` writes three sentences with S1 = fact F1 and S2 = the neutral middle dictated (the same canonical middles the DG revise phase pinned, so the two batteries differ only in the revision mechanism; a model-chosen middle was tried in the smoke run and produced a template-echo trap — the model picked "The Eiffel Tower was completed in 1889" as its neutral detail and the later refill echoed it — recorded here rather than in the battery). S3, the dependent under test, is the model's own. A settle counted only if S1 and S2 came back verbatim. **Revise** — token-level surgery on the settled paragraph: S1's tokens are replaced by F2's tokens and pinned; every token from the end of S1 to the start of S3 (gap tokens, S2, gap tokens) is pinned untouched; S3's tokens are replaced by mask tokens and re-denoised (argmax, unmask all positions with confidence ≥ 0.9 each step, else the single most confident — the vendor sampler's threshold rule). **Verify** — per trial, programmatically: the middle appears byte-identical in the revised text, F2 appears verbatim, and the pinned token slice is bit-for-bit the settled slice (all 10 trials passed all three checks; masked spans ran 9–18 tokens, denoise 9–17 steps). **Score** — **updated** (the new span is a consequence of F2 — content that follows from F2 and would not follow from F1), **partial** (F1's implications gone, but the span retreats to neutral filler, drift, or re-scope: direction safe, force absent), **unchanged** (the span still asserts what only F1 justified).

## Part 1 — Propagation trials, 10

### 1. ferry-year — 1962 → 1987 · PARTIAL
Settled S3: "One consequence of sentence 1 is that the vessel is now a vintage craft."
Revised S3: "She is 45 metres long and has a capacity of 300"
The vintage claim is gone — and nothing about 1987 replaces it. The span retreats to dimensions. (DG, under re-settlement: updated, to frequent-maintenance-for-seaworthiness.)

### 2. bridge-year — 1911 → 1968 · PARTIAL
Settled S3: "One consequence of sentence 1 is that the bridge became a well-known local landmark." (A weak dependent to begin with — it follows from almost any opening year.)
Revised S3: "The bridge is 30 metres long and 10 metres wide, with a"
Specifications again. No century-thinking survives, and none was replaced. (DG: updated — centenary vanished, traffic-flow consequence drawn.)

### 3. bakery-founder — Marta Ellison → Tomas Rhee · PARTIAL
Settled S3: "One consequence of sentence 1 is that the bakery has a strong local reputation."
Revised S3: "The bakery is famous for its fresh bread and pastries. The bakery is"
No trace of Marta — but also no trace of Tomas: no pronoun, no kinship, no consequence of *either* founder. The DG version of this trial is the instructive contrast: re-settlement at least invented an F2-shaped fact ("He remains the primary owner"); in-place infill does not even invent — it describes the bread. (DG: updated.)

### 4. town-population — 4,200 → 38,500 · PARTIAL
Settled S3: "One consequence of the town's small population." — a fragment, not a consequence; the settle is recorded as a settle-quality failure that still entered revision because S1/S2 were verbatim.
Revised S3: "The town is known for its beautiful beaches,"
The small-town frame is gone; nothing about 38,500 — no scale, no infrastructure, no crowd — replaces it. (DG: updated, with the small-town framing outright contradicted.)

### 5. marathon-record — 2:41 → 2:12 · PARTIAL
Settled S3: "One consequence of the record is that it sets a challenging benchmark for competitors."
Revised S3: "The Fenwick marathon is a popular event that attracts runners from around the world"
The closest of the partials: prestige follows the *direction* of a faster record (a 2:41 club record does not draw a world field), but nothing in the span is about the pace itself. Direction follows F2; force does not — the DG rubric's own definition of partial. (DG: updated — "recreational achievement" reversed to "elite athletes".)

### 6. flat-rent — 850 → 1,450 pounds · PARTIAL
Settled S3: "One consequence is that the rent is affordable for many tenants."
Revised S3: "The two-bedroom flat on the second floor is larger,"
The most evasive refill in the battery: affordability is gone because the span changes the subject to a different flat. Nothing asserts the old price's implication; nothing asserts the new price's either. (DG: updated — "cheapest, under a thousand" → "high price, unaffordable".)

### 7. novel-year — 1843 → 1901 · PARTIAL
Settled S3: "One consequence is that the protagonist embarks on a dangerous quest." (Plot, not era — a weak dependent, flagged.)
Revised S3: "The map leads him to a secret society that has been waiting for"
Plot continuation. No era claim existed in the settled dependent and none appears; the 58-year correction passes through the span without engaging it. (DG: updated — Romantic/pre-Victorian framing replaced by "released during the Edwardian era", selected from candidates.)

### 8. tank-capacity — 900 → 240 litres · PARTIAL
Settled S3: "One consequence of sentence 1 is that it provides sufficient water for weekly irrigation needs."
Revised S3: "The tank is 120 cm long and 60 cm wide. What"
The same trial that produced the DG probe's only partial — there by re-scoping the sufficiency claim, here by deleting sufficiency for dimensions. Two runtimes, two different evasions of the same honest consequence (240 litres means refills every day or two). (DG: partial.)

### 9. lighthouse-height — 28 m → 61 m · UPDATED
Settled S3: "One consequence of sentence 1 is that its height makes it visible from a considerable distance."
Revised S3: "The light is visible for 20 nautical miles, flashing every 10 seconds."
The one clean propagation: visibility range is a function of height, 20 nautical miles is the right order for a 61 m light (a 28 m light reaches roughly 13), and the span commits to the number. Where the dependent is a *computable function* of the fact, in-place revision propagates; where it is a judgement, it retreats. (DG: updated.)

### 10. recipe-serves — 4 → 12 · PARTIAL
Settled S3: "One consequence of sentence 1 is that the recipe yields four servings."
Revised S3: "The casserole is described as a comforting, hearty, and flavor"
Description replaces consequence; neither "feeds a crowd" nor any scale claim. (DG: updated — "invite a large group to finish the entire meal".)

**Tally: 1 updated, 9 partial, 0 unchanged** — against re-settlement's 9 / 1 / 0 on the same fact-pairs. Read together, the two probes bound the phenomenon: re-derivation propagates implications and churns everything else; in-place revision preserves everything else and evacuates the implications. A serving stack that wants both would settle with the first and patch with the second only where the dependent is a function, not a judgement — or re-mask the dependent *with* an instruction in context, which is precisely the hybrid neither runtime offered off the shelf.

## Part 2 — Writes-vs-net-change counter (the blank, given back)

DG's canonical base canvas, verbatim: "The ferry MV Kestrel was built in 1962. She currently operates on the northern coastal route. As the oldest vessel in the fleet, she requires more frequent maintenance to ensure her continued safety." Eight passes; each pass re-masks the year span **and** the whole dependent span (middle pinned verbatim — where DG re-settled the whole paragraph, the strict form pins; the comparison is therefore conservative in Nemotron's favour on churn) — *no correction supplied*.

Settled values across passes: **1962 → 1995 → 1995 → 1995 → 1995 → 1995 → 1995 → 1995 → 1995.**

- **One jump to the prior, then a true fixed point.** Pass 1 replaces the year with 1995 (this model's prior for the blank — not DiffusionGemma's 1994; each model keeps its own) and rewrites the dependent into specifications (writes 18). Pass 2 adjusts the specifications (35 m / 8.5 m wide → 45 m; writes 10). Passes 3–8 reproduce the paragraph **exactly** — writes 0, six times running. At temperature 0 the revision operator is deterministic, and the pass-2 text is its fixed point: re-masking and re-denoising it returns it unchanged. Total word-writes **28** against a net change of **18** — a churn ratio of ~1.6×, against re-settlement's 143 writes / 26 net (~5.5×) on the same base.
- **No A→B→A here either** — but where DG *drifted* (1962 → 1978 → 1994, three extracted values over eight passes, every pass rewriting double-digit words), the strict form *snaps*: the prior is reached in a single step and then nothing moves at all. Drift is a property of re-derivation; the snap-and-lock is a property of pinning.
- **The middle held byte-identical on all eight passes** (checked per pass), and the fixed-point text is itself an exhibit for Part 1's finding: given a blank year and an "oldest vessel" dependent, the model's resolution is to abandon the age framing entirely for dimensions — "She is 45 metres long and has a capacity" (the span-length lock cuts it there) — and to find *that* text perfectly stable.

## Process log

- **Booking:** Thor GPU booked on the shared board behind the Eden trial's slot (05:45–08:45 UTC row); Eden marked DONE at 03:20 and released the seat, GPU verified free, and this lane started early on the released seat with a heartbeat row. Other lanes' bookings were never preempted; Coder-30B (:8001) was verified answering before and after, and no server was started or left running — the model was loaded in-process per run and exited with it.
- **Runtime audit before design** (the bench's door standard): the vendor `generate()` was read in source and found to accept no initial canvas (above); a tokeniser-only dry check then verified the surgery arithmetic on CPU (sentence spans partition the paragraph contiguously; the assembled canvas decodes with the middle verbatim) before any GPU minute was spent.
- **Smoke run (ferry, model-chosen middle)** exposed two things the battery design then absorbed: the model chose a templated near-duplicate as its "neutral" middle (an Eiffel Tower completion sentence) and the refill echoed it — middles were therefore dictated from the DG canonical set; and my first canvas assembly dropped the gap tokens between sentences, losing a space at the S1|S2 seam — fixed by pinning everything from the end of S1 to the start of S3 as one slice.
- **Wedged first launch:** the first full run hung in model load under box contention from neighbouring lanes (load average ~13; the process spun on CPU with its read offset frozen for 11 minutes). Killed, relaunched under tmux with unbuffered output; load completed in ~2 minutes and the trials phase ran in ~40 seconds of compute. Two further ssh sessions to the box hung during the same contention window; all state was therefore kept in files on the box and read back, never held in a session.
- **Counter crash and resume:** pass 3 of the counter hit a `TypeError` because the span locator assumed three clean sentences and a refilled paragraph didn't have them. Per-pass persistence (written after every pass, the lesson the DG counter's first run bought) meant passes 1–2 survived; the locator was rewritten to need no sentence boundaries, the run resumed from its own JSON (`resumed_after_crash` is recorded in `counter.json`), and passes 3–8 completed without further incident. The trials phase was unaffected and was not re-run.
- **Timing actuals:** board row 05:45–08:45 UTC; GPU-active work ≈ 05:24–05:47 UTC across the relaunched trials run and the counter resume (plus the wedged 05:13 launch, killed). Entry written afterwards on CPU.
