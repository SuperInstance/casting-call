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
