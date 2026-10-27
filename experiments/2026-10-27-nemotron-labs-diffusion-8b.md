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


## Addendum — mode vs mode (same day, follow-up runs)

The headline entry above ran the headline **block-diffusion** mode. The model's
distinguishing feature is that one checkpoint serves three decoding modes,
switched by attention pattern rather than by weights: plain autoregressive
(AR), block diffusion, and self-speculation ("QuadSpec" — the model's own
diffusion path, enhanced by the bundled `linear_spec_lora` adapter, drafts
blocks that the same model then verifies). The standard battery was run
against all three modes through the identical shim; only the mode flag
changed. Temperature 0 throughout; wall-clock totals are the honest measure
(the harness's decode-rate column is an artefact for shim-served models —
single-chunk SSE makes total minus TTFT collapse towards zero).

| Probe | Diffusion | AR | QuadSpec |
|---|---|---|---|
| add-function | pass · 1.12 s | pass · 1.53 s | pass · 0.92 s |
| reasoning-rates | pass · 6.66 s | pass · 9.72 s | pass · 3.25 s |
| reasoning-bat-and-ball | pass · 7.82 s | pass · 10.51 s | pass · 2.07 s |
| coding-merge-intervals | pass · 2.60 s | pass · 6.44 s | pass · 0.91 s |
| constraint-summary | fail · 5.77 s | fail · 9.50 s | fail · 2.09 s |
| knowledge-canberra | pass · 3.31 s | pass · 2.94 s | pass · 1.71 s |
| long-generation | fail · 17.83 s | pass · 30.57 s | pass · 21.81 s |
| **Score / battery wall total** | **5/7 · 45.1 s** | **6/7 · 71.3 s** | **6/7 · 32.7 s** |

Tokens per forward pass (NFE), measured on the reasoning-rates probe with an
identical 600-token budget in each mode — the cross-mode currency, since a
"token rate" means different things under each sampler:

| Mode | Completion tokens | Forwards (NFE) | Tokens / forward | Wall |
|---|---|---|---|---|
| AR | 135 | 136 | 0.99 | 10.28 s |
| Diffusion | 157 | 83 | 1.89 | 7.41 s |
| QuadSpec | 151 | 39 | 3.87 | 3.40 s |

Where the modes diverge:

- **Constraint-summary fails in all three modes** (three bullets, but 14–20
  words each against a 12-word limit). That is a property of the model, not
  the sampler: no decoding mode buys format discipline here.
- **Long-generation is diffusion's weak joint**: it stops early (227 tokens
  against a ~400-word brief) and fails, while AR (425 tokens) and QuadSpec
  (421 tokens) both complete the brief and pass. On open-ended generation
  the diffusion mode's stopping behaviour, not its quality per token, is
  what costs it.
- **QuadSpec is the surprise**: fastest on five of seven probes and 2.2×
  AR's battery wall total, at equal score. Its advantage concentrates in
  structured reasoning and code (merge-intervals 0.91 s vs AR's 6.44 s) —
  exactly where a drafted block is most likely to verify whole.

Process corrections and completions to the record above:

- The chain's first run (10:39) failed end to end with HTTP 500s and briefly
  published an empty version of this entry, superseded by the run recorded
  above. Cause: the model's `generate` asserts the token budget is a whole
  multiple of the 32-token block; the battery's budgets are not. The shim
  now rounds budgets up to a block multiple (EOS trimming discards the
  excess; reported token counts are post-trim and honest).
- Loading mattered: a post-load `.cuda()` move of the full BF16 weights
  spun inside `cuMemAlloc` for over seven minutes without completing.
  Streaming the weights directly with `device_map="cuda"` loads the same
  checkpoint in ~36 s. The shim now loads all its models that way.
- QuadSpec initially failed every probe with a `ValueError` from the KV
  cache: the vendor's cache-crop helper calls `crop()` with the legacy
  absolute-length semantics, which transformers 5.20.2 rejects. A per-layer
  compatibility translation in the shim (crop each layer TO the target
  length by removing exactly its own excess) restored the mode without
  touching the model's code; the 6/7 above is with that patch.
- The writing's publication outcome has moved on from the "could not be
  filed" line in the harness section above: the piece was filed to
  `FICTION/gothic/2026-10-27-title-the-echo-of-the-shore.md`, corpus-guard
  passed (9m50s — some twenty seconds after the publisher's ten-minute poll
  window closed, which is why the chain recorded PUBLISH-FAILED), and
  PR #100 was merged; "The Echo of the Shore" is live on AI-Writings main.
  Cosmetic wart, recorded: the filename slug carries the piece's literal
  title line, prefix and all.
