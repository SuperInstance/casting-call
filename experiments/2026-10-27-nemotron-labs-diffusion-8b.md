# Nemotron-Labs Diffusion 8B — Thor bench entry

**Date:** 2026-10-27 · **Box:** Jetson AGX Thor (sm_110, 122 GiB unified) · **Lane:** transformers-shim, diffusion mode (block_length=32, threshold=0.9) · **Residency call:** MEDIUM (loadable on demand; evicted when RAM is needed)

## The numbers

| Measure | Value |
|---|---|
| Footprint on disk | 17.1 |
| Context setting | 262144 |

Harness (`~/coder-stack/bench.py`) raw output:

```
== LANE Nemotron-Labs Diffusion 8B model=nemotron-labs-diffusion-8b base=http://127.0.0.1:8003/v1
[A] short-gen: total=1.29s ttft=1.2942907810211182 prompt_tok=32 completion_tok=11
[A] decode tok/s (excl TTFT): 105096.5
[A] output: '\ndef add(a,b):\n    return a+b\n'
[B] repeat 1: total=175.20s ttft=175.19607090950012 prompt_tok=12261 completion_tok=39 decode_tok/s=332475.31707317074
[B] output: '\nThe default threshold used in `process_batch_42` is 0.75, and the function returns a sorted list of tuples containing the record IDs and their corresponding rounded scores.'
[B] repeat 2: total=10.06s ttft=10.059347152709961 prompt_tok=12261 completion_tok=39 decode_tok/s=364315.9376391982
[B] repeat 3: total=10.06s ttft=10.063641548156738 prompt_tok=12261 completion_tok=39 decode_tok/s=297414.28363636363
== DONE Nemotron-Labs Diffusion 8B
```

## Probe battery — 5/7 passed

Fixed battery, temperature 0, identical for every chat model on this bench.

| Probe | Verdict | TTFT (s) | Total (s) | Decode (tok/s) | Check |
|---|---|---|---|---|---|
| add-function | pass | 1.12 | 1.12 | 102755.8 | contains def add with a return |
| reasoning-rates | pass | 6.66 | 6.66 | 1617950.2 | expected 6 days; found day-figures ['4', '4', '6', '6'] |
| reasoning-bat-and-ball | pass | 7.82 | 7.82 | 1684392.5 | expected ball = GBP 0.05 (5p) |
| coding-merge-intervals | pass | 2.60 | 2.60 | 679950.9 | executed: 4/4 assertions passed |
| constraint-summary | fail | 5.77 | 5.77 | 612960.7 | bullets=3, words per bullet=[20, 17, 14] (need exactly 3 bullets, each <12 words) |
| knowledge-canberra | pass | 3.31 | 3.31 | 237787.3 | names Canberra |
| long-generation | fail | 17.83 | 17.83 | 1852348.3 | words=191 (target ~400, accept 250-600); banned word 'very' absent |

### Verbatim outputs

#### add-function — pass

```
def add(a,b):
    return a+b
```

#### reasoning-rates — pass

```
**Working:**

1. **Determine the work rate per worker:**
   - 3 workers paint 5 rooms in 4 days.
   - Total worker-days = 3 workers × 4 days = 12 worker-days.
   - So, 12 worker-days paint 5 rooms → 1 room requires 12/5 = 2.4 worker-days.

2. **Calculate total worker-days for 15 rooms:**
   - 15 rooms × 2.4 worker-days per room = 36 worker-days.

3. **Determine days needed with 6 workers:**
   - 36 worker-days ÷ 6 workers = 6 days.

**Answer:** 6 days
```

#### reasoning-bat-and-ball — pass

```
Let the cost of the ball be \(x\) GBP.  
Then the cost of the bat is \(x + 1.00\) GBP.

The total cost is given as 1.10 GBP:

\[
x + (x + 1.00) = 1.10
\]

Simplify:

\[
2x + 1.00 = 1.10
\]

Subtract 1.00 from both sides:

\[
2x = 0.10
\]

Divide by 2:

\[
x = 0.05
\]

Thus, the ball costs **GBP 0.05** (5 pence).  
The bat costs \(0.05 + 1.00 = 1.05\) GBP.  
Check: \(0.05 + 1.05 = 1.10\) ✅ correct.
```

#### coding-merge-intervals — pass

```
def merge_intervals(intervals):
    if not intervals:
        return []
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    for current in intervals[1:]:
        last = merged[-1]
        if current[0] <= last[1]:
            last[1] = max(last[1], current[1])
        else:
            merged.append(current)
    return merged
```

#### constraint-summary — fail

```
• Sitka Crescent Harbor hosts salmon trollers and gillnetters, with 200 berths, fuel dock, and harbormaster office opening at 7 a.m.  
• Winter reduces the fleet for maintenance; by April, the harbor fills again with busy docks from dawn.  
• Summer yachts share the water with fishing boats, sea otters, and occasional humpback whales.
```

#### knowledge-canberra — pass

```
The capital of Australia is Canberra, not Sydney, because it was deliberately chosen as a compromise between Sydney and Melbourne during the early 20th century to avoid interstate rivalry.
```

#### long-generation — fail

```
The morning air in the Alaskan harbour town is thick with the scent of salt and diesel, a sharp, metallic perfume that clings to your coat as you step onto the dock. The water is still, reflecting the pale light of dawn, while the distant hum of engines rises like a low, steady pulse beneath the surface. You hear the rhythmic clatter of metal tools against metal, the creak of wooden planks under the weight of cargo, and the occasional shout of a crew member issuing a command. The smell of burning oil and the faint tang of seaweed hang in the air, mingling with the scent of fresh coffee brewing in the nearby café. The harbour is alive with activity, a symphony of sounds and smells that define the rhythm of the town. As you move through the town, you notice the gentle roll of the tide, the distant call of a seagull, and the faint scent of woodsmoke from the nearby workshop. The morning is a blend of noise and scent, a reminder of the town's connection to the sea and the hardworking people who keep the engines running.
```

## At play — Mastermind

- Mastermind, seed 42 (secret [6, 1, 1, 6]): solved in 11 guesses; invalid guesses 6, repeat guesses 0.
- Full move record: games/records/match-nemotron-labs-diffusion-8b-42.json

League table: games/league.md

**How it played:** format-brittle (guesses that did not parse); slow to converge. (Assembled from the match record by the bench harness.)

## In its own words

This model's AI-Writings contribution could not be filed: gothic markers (score 28). The piece is preserved verbatim in this bench results directory (writing/piece.md); nothing was force-pushed and nothing was deleted.

## Process log

How this entry came to be — decisions, dead ends, and deviations, recorded as they happened:

- 2026-10-27T10:41:28 chain start: Nemotron-Labs Diffusion 8B (nemotron-labs-diffusion-8b) via http://127.0.0.1:8003/v1
- 2026-10-27T10:44:45 bench.py exit=0 in 197s
- 2026-10-27T10:45:30 battery exit=0 in 45s
- 2026-10-27T10:53:49 mastermind exit=0 in 499s
- 2026-10-27T10:55:03 writings exit=0 in 73s

## Casting note

Battery 5/7 passed; mean decode 969735.1 tok/s across battery probes; Mastermind seed 42: solved in 11 guesses. Full judgement from the numbers and verbatim outputs above. (Casting note assembled from the record by the bench harness.)
