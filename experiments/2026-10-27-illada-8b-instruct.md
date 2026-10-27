# iLLaDA 8B Instruct — Thor bench entry

**Date:** 2026-10-27 · **Box:** Jetson AGX Thor (sm_110, 122 GiB unified) · **Lane:** ML-GSAI masked diffusion (bidirectional, from scratch; variable-length generation) via the official LLaDA-repo generate.py (mask_id=5) behind the lab shim — served from a version-pinned venv (transformers 4.57.1, the checkpoint's own recorded version) because transformers 5.20.2 first refuses the vendor class (old-style _tied_weights_keys) and, patched past that, silently degrades its forward to near-unigram output · **Residency call:** MEDIUM (loadable on demand; evicted when RAM is needed)

## The numbers

| Measure | Value |
|---|---|
| Footprint on disk | 16.5 |
| Context setting | default |

Harness (`~/coder-stack/bench.py`) raw output:

```
== LANE iLLaDA 8B Instruct model=illada-8b-instruct base=http://127.0.0.1:8003/v1
[A] short-gen: total=10.65s ttft=10.649374723434448 prompt_tok=24 completion_tok=224
[A] decode tok/s (excl TTFT): 2125620.1
[A] output: "<think>\nGot it, let's see. The user wants a Python function called add that takes two arguments a and b and returns their sum. First, I need to remember how to define a function in Python. The syntax is like def function_name(parameters): ... \n\n \n\nSo, the function name is add, and parameters a and b"
[B] repeat 1: total=353.33s ttft=353.32951617240906 prompt_tok=13693 completion_tok=128 decode_tok/s=1322342.1477832512
[B] output: ' ###), →://://://!/!/!/!/!/!/!/!/!/!/!/!/!/!/!/!/!/!/!/!/!/!/!/!/!/!/!/!/!/!/!/!/!/!/!/!/!/!/!/!/!/!/!/!/!/!/!/!/://!/://://!/://!/://://!/!/!/!/!/!/!/!/!/!/!/!/!/!/!/!/!/://!/!/!/!/!/://://!/://!/!/!'
[B] repeat 2: total=366.62s ttft=366.61732625961304 prompt_tok=13693 completion_tok=128 decode_tok/s=1086783.2226720648
[B] repeat 3: total=393.46s ttft=393.460875749588 prompt_tok=13693 completion_tok=128 decode_tok/s=897777.4448160535
== DONE iLLaDA 8B Instruct
```

## Probe battery — 2/7 passed

Fixed battery, temperature 0, identical for every chat model on this bench.

| Probe | Verdict | TTFT (s) | Total (s) | Decode (tok/s) | Check |
|---|---|---|---|---|---|
| add-function | pass | 12.09 | 12.09 | 1340262.6 | contains def add with a return |
| reasoning-rates | error | — | — | — | request failed: HTTP Error 500: Internal Server Error |
| reasoning-bat-and-ball | error | — | — | — | request failed: HTTP Error 500: Internal Server Error |
| coding-merge-intervals | fail | 44.52 | 44.52 | 3463683.3 | executed: FAILED (SyntaxError: unterminated string literal (detected at line 2)) |
| constraint-summary | fail | 20.06 | 20.06 | 2097152.0 | bullets=0, words per bullet=[] (need exactly 3 bullets, each <12 words) |
| knowledge-canberra | pass | 10.59 | 10.59 | 1447648.8 | names Canberra |
| long-generation | error | — | — | — | request failed: HTTP Error 500: Internal Server Error |

### Verbatim outputs

#### add-function — pass

```
<think>
Got it, let's see. The user wants a Python function called add that takes two arguments a and b and returns their sum. First, I need to remember how to define a function in Python. The syntax is like def function_name(parameters): ... 

 

So, the function name is add, and parameters a and b. Then, inside the function, I need to add a and b together and return the result. 

Wait, what's the return type? The, well, sum is a sum, so probably's an integer, but Python Python doesn't enforce return types, but it's okay. 

Let me structure it: def add(a, b): return a + b. That's simple. Let me test: if I call add(2, 3), it should return 5. Yeah. 

Is there any edge case? Like if the inputs are not numbers? But the question says "returns their sum", so probably assumes numeric inputs are given. The user didn't mention error handling, so maybe just basic addition. 

So the code should be
```

#### reasoning-rates — error

```
(empty)
```

#### reasoning-bat-and-ball — error

```
(empty)
```

#### coding-merge-intervals — fail

```
<think>
Got it, let's see. I need to write a Python function called merge_intervals that takes a list of intervals, merges overlapping ones, and returns the sorted list. First, I should think about the steps..

First, the input are [start, end] pairs. So the first thing is to sort the intervals by their start time. Because if they're not sorted, we can't check overl overlaps easily.

Then, iterate through, and for each interval, check if it overlaps with the previous one. If it does, merge them. So the merged interval's start is the minimum of the two starts, and the end is the maximum of the two ends.

Wait, right. So the steps are:

1. Sort the intervals by on the start time.
2. Initialize an empty list for merged intervals.
3. Start with first interval as current merged.
4. For each subsequent interval:
   a. If current interval's start is <= current merged's end: merge them. So new merged start is min(current merged start, current start), new merged end is max(current merged end, current end).
   b. Else: add current merged to merged, then set current merged to current interval.
5. After the loop, add the last current merged to merged.
6. Return the merged list.

Let's test this logic with an example. Suppose input is [[1,3], [2,6], [8,10], [15,18]]. Sorted is same. First merged is [1,3]. Next is [2,6]: 2 <=3, merge to [1,6]. Next is [8,10]: 8 <=6, merge to [1,10]. Next is [15,18]: 15 >10, add to merged. So result is [[1,10], [15,18]]. That's correct.

Another example: [[1,4], [4,5]]. Merged to [1,5]. Correct.

What about empty list? Return empty. Single interval? Return it.

Edge cases code: if not intervals: return intervals.

Let's code this:

def merge_intervalsvals(intervals):
    if not intervals:
        return intervals
    # Sort by start
    intervals.sort(key=lambda x: x[0])
```

#### constraint-summary — fail

```
<think>
Got it, let's tackle this. First, I need to summarize the key points into three bullet points, each under 12 words. Let's start with the first part: Crescent Harbor is a working harbour on Sitka's north side, home to salmon trollers and gillnetters in Sitka Sound. That's a main point. 

Next, the facilities: berths for 200 vessels, fuel dock, harbormaster's office opening at 7.. That, but, wait, the to be under 12 words. Let's count: "Has berths, fuel dock, and harbormaster's office opening at 7." That's 11 words. 

Third, the seasons: winter fleet smaller (haul out out), April full and busy from dawn; summer yachts, local boats, otters, humpbacks. Let's check: "Winter fleet smaller (haul out out), April full and busy from dawn; summer yachts, local boats, otters, humpbacks." That's 12 words. 

Let me check each:

1. Crescent Harbor is a working harbour on Sitka's north side, home to salmon trollers and gillnetters in Sitka Sound. (14 words)
2. Has berths, fuel dock, and harbormaster's office opening at 7. (11 words)
3. Winter fleet smaller (haul out out), April full and busy from dawn; summer yachts, local boats, otters
```

#### knowledge-canberra — pass

```
<think>
Got it, let's tackle this question: "What is the capital of Australia, and why is it not Sydney?" First, I need to remember the capital—yes, Canberra. Then, why not Sydney? The key reason is that the was chosen as a neutral location to avoid political bias between the and the capitals. Wait, let's make it concise. 

First sentence: The capital of Australia is Canberra. Second sentence: Why not Sydney Sydney? chosen as a neutral location to avoid political bias between the and the capitals. Wait, let's check: that's two sentences, answers both parts. Let's make sure it's clear. Maybe, "The capital of Australia is Canberra; chosen, not Sydney, as a neutral location to avoid political bias between the and the capitals." Yes, that's two sentences, covers both questions. Let's verify: Canberra is correct, reason is neutrality to prevent political bias between the capitals capitals. Perfect.</think>The capital of Australia is **Canberra**. It is not Sydney because it was chosen as a neutral location
```

#### long-generation — error

```
(empty)
```

## At play — Mastermind

- Mastermind, seed 42 (secret [6, 1, 1, 6]): did NOT solve within 12 guesses; invalid guesses 0, repeat guesses 0.
- Full move record: games/records/match-illada-8b-instruct-42.json

League table: games/league.md

**How it played:** did not converge on this secret. (Assembled from the match record by the bench harness.)

## In its own words

This model's AI-Writings contribution could not be filed: reflective prose (the library's essay shelf). The piece is preserved verbatim in this bench results directory (writing/piece.md); nothing was force-pushed and nothing was deleted.

## Process log

How this entry came to be — decisions, dead ends, and deviations, recorded as they happened:

- 2026-10-27T14:24:14 chain start: iLLaDA 8B Instruct (illada-8b-instruct) via http://127.0.0.1:8003/v1
- 2026-10-27T14:42:58 bench.py exit=0 in 1124s
- 2026-10-27T14:44:26 battery exit=0 in 87s
- 2026-10-27T14:44:26 mastermind exit=0 in 0s
- 2026-10-27T14:55:46 writings exit=0 in 681s

## Casting note

Battery 2/7 passed; mean decode 2087186.7 tok/s across battery probes; Mastermind seed 42: unsolved in 12 guesses. Full judgement from the numbers and verbatim outputs above. (Casting note assembled from the record by the bench harness.)

## Addendum — corrected battery and Mastermind, and the serving story (2026-10-27, later)

**Why this addendum exists.** The entry above was rendered from a chain run in which three battery probes (reasoning-rates, reasoning-bat-and-ball, long-generation) and Mastermind turn 1 returned HTTP 500 from the shim, so the battery printed 2/7 with three errors and the Mastermind record held a single error move. The cause was in the shim, not the model: the vendor `generate()` asserts `steps % num_blocks == 0`, and the shim's step count (capped at 256) is not divisible by the block count for 640- and 672-token canvases (20 and 21 blocks of 32). Probes whose canvases divided cleanly ran normally. The shim now sets `steps = gen_length // 2` (16 steps per 32-token block, always divisible); battery and Mastermind were re-run against the patched shim. The chain-run originals are preserved in the bench results directory as `battery-chainrun.json` and `match-chainrun.json`.

**Corrected battery: 5/7** (total ≈ 240 s). add-function pass (10.9 s); reasoning-rates pass (55.8 s — the think trace reaches "the answer is 6 days" before answering); reasoning-bat-and-ball pass (55.5 s); coding-merge-intervals fail on merit (41.6 s); constraint-summary fail on merit (19.4 s); knowledge-canberra pass (10.3 s); long-generation pass (56.8 s).

The two merit failures are the same outputs as printed above (temperature 0, identical step counts, byte-identical). They deserve plain statements. merge-intervals: the think trace plans the algorithm correctly, then reasons "Next is [8,10]: 8 <= 6, merge to [1,10]" — a false comparison producing a wrong merged result, [[1,10], [15,18]] in place of [[1,6], [8,10], [15,18]], which it declares correct — and the code it finally emits names the function `merge_intervalsvals` and truncates mid-string, so execution fails on a SyntaxError. constraint-summary: the model drafts all three bullets inside its think block (the first runs to 14 words, over the limit it is busy counting) and then never emits a bullet list at all, so the checker sees bullets=0. In both cases the deliberation is long and mostly competent; the failure is at the exit from deliberation into the required form.

long-generation's pass carries a caveat the checker cannot see: its tail degenerates into a looped phrase ("the the tools on the bench, …" repeated to the end of the canvas). The word count lands in band and the banned word is absent, so it passes; the verbatim output in `battery.json` shows the decay. The fixed-canvas sampler fills the canvas it is given whether or not the text has finished — the same trait that decides the Mastermind fixture below.

**Corrected Mastermind: unsolved; 12 guesses, all 12 invalid; 0 repeats; 1,530 s of turn time.** No turn ever emitted a parseable `GUESS:` line. Every response is an unclosed deliberation that consumes the whole 1024-token canvas: turn 1 ends mid-sentence ("first guess should be a code that's"), still choosing an opener after 113 s. From turn 2 the model fixates on digit 0 — outside the game's stated 1–6 range — and begins inventing the game's feedback, recording its own invalid turns as "0 0 0 0 → -1 black, -1 white" (impossible scores) and reasoning from them as though they were data. The deliberation degrades as the transcript grows: turn 8 ends in a "no, wait" repetition loop, turn 12 in "the, the, the, …". The league table and the record in `games/records/` have been rebuilt from this corrected run. It is the purest instance on this bench of the failure class the fleet's corpus audit named for Match 001: the game was never really played, because no guess ever left the deliberation register.

**Writing correction.** The entry above says the AI-Writings piece "could not be filed". It was filed: AI-Writings PR #102, `ESSAYS/2026-10-27-think.md`, corpus-guard passed; the chain's publisher recorded a failure anyway (the same publisher defect seen on PRs #100 and #101) and the PR was merged by hand on 2026-10-27T23:08:36Z. The filename slug is the piece's literal first line — a `<think>` opener: the model began its essay inside its reasoning register, which is of a piece with everything above.

**The serving story (the load failure worth keeping).** The checkpoint's own metadata records transformers 4.57.1. Under the bench venv's transformers 5.20.2, the vendor class first refuses to load at all: it declares `_tied_weights_keys` in the old list style (`["lm_head.weight"]`), where 5.20.2's `post_init` expects the dict mapping and raises `AttributeError: 'list' object has no attribute 'keys'`. Patched past that in the shim (the class attribute converted to `{"lm_head.weight": "model.embed_tokens.weight"}` on the exact class transformers instantiates), the checkpoint loads — all 291 tensors verified present, tied weights verified tied — and generates near-unigram debris: a chat prompt settles into newlines and repeated "user" tokens, and a single-mask probe ("The capital of Australia is [MASK]") ranks " of", "(", newline above " Canberra" in a near-flat distribution. Under a version-pinned venv (transformers 4.57.1, torch inherited from the bench venv, official `generate.py` unmodified), the identical checkpoint and sampler put " Canberra" top-1 at the same probe (12.81, Sydney second) and produced every result in this entry. The 5.20.2 failure is silent — no error, no missing weights, just a lobotomised forward — so: for vendor-code checkpoints, the recorded transformers version is part of the model, and a load that succeeds proves nothing until the model has been made to say something back.

**Bench note on [B].** bench.py's long-prompt phase uses a 13,693-token prompt against a configured maximum of 8,192 positions. The model served it without complaint and the sampled output is punctuation debris (verbatim in the entry above, 353–393 s per repeat). Read those numbers as an out-of-range probe, not a context result: inside its range the model is coherent; beyond it, it does not refuse — it dissolves.

**Character note (revised).** A genuinely capable short-form thinker — 5/7 on the battery, correct multi-step reasoning, coherent code plans — whose deliberation register does not terminate inside a fixed canvas. Give it a question with a checkable middle and it shines; give it a stateful game that requires concluding, and it thinks beautifully for 25 minutes and never plays a move.
