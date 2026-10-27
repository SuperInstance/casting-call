# Nemotron-3.5-Lightning (Ollama) — Thor bench entry

**Date:** 2026-10-26 · **Box:** Jetson AGX Thor (sm_110, 122 GiB unified) · **Lane:** Ollama (fleet service :11434) · **Residency call:** MEDIUM (loadable on demand; evicted when RAM is needed)

## The numbers

| Measure | Value |
|---|---|
| Footprint on disk | see inventory |
| Context setting | Ollama server default context |

Harness (`~/coder-stack/bench.py`) raw output:

```
== LANE Nemotron-3.5-Lightning (Ollama) model=nemotron-3.5-lightning:latest base=http://127.0.0.1:11434/v1
[A] short-gen: total=10.12s ttft=9.938729763031006 prompt_tok=32 completion_tok=190
[A] decode tok/s (excl TTFT): 1054.4
[A] output: '```python\ndef add(a, b):\n    return a + b\n```'
[B] repeat 1: total=11.22s ttft=None prompt_tok=12261 completion_tok=120 decode_tok/s=10.690472299499461
[B] output: ''
[B] repeat 2: total=1.47s ttft=None prompt_tok=12261 completion_tok=120 decode_tok/s=81.5369726392717
[B] repeat 3: total=1.54s ttft=None prompt_tok=12261 completion_tok=120 decode_tok/s=78.06032114264285
== DONE Nemotron-3.5-Lightning (Ollama)
```

## Probe battery — 2/7 passed

Fixed battery, temperature 0, identical for every chat model on this bench.

| Probe | Verdict | TTFT (s) | Total (s) | Decode (tok/s) | Check |
|---|---|---|---|---|---|
| add-function | pass | 2.41 | 2.58 | 1125.5 | contains def add with a return |
| reasoning-rates | fail | — | 8.04 | — | expected 6 days; found day-figures [] |
| reasoning-bat-and-ball | pass | 6.03 | 7.75 | 343.5 | expected ball = GBP 0.05 (5p) |
| coding-merge-intervals | fail | — | 6.61 | — | executed: FAILED (NameError: name 'merge_intervals' is not defined) |
| constraint-summary | fail | — | 4.14 | — | bullets=0, words per bullet=[] (need exactly 3 bullets, each <12 words) |
| knowledge-canberra | fail | — | 2.64 | — | does not name Canberra |
| long-generation | fail | — | 10.43 | — | words=0 (target ~400, accept 250-600); banned word 'very' absent |

### Verbatim outputs

#### add-function — pass

```
```python
def add(a, b):
    return a + b
```
```

#### reasoning-rates — fail

```
(empty)
```

#### reasoning-bat-and-ball — pass

```
Let the ball cost **x** GBP.  
Then the bat costs **x + 1.00** GBP.

Together:  
x + (x + 1.00) = 1.10  
2x + 1.00 = 1.10  
2x = 0.10  
x = 0.05

The ball costs **GBP 0.05** (5p).  
Check: Ball 5p + Bat £1.05 = £1.10, and the bat is exactly £1.00 more than the ball.
```

#### coding-merge-intervals — fail

```
(empty)
```

#### constraint-summary — fail

```
(empty)
```

#### knowledge-canberra — fail

```
(empty)
```

#### long-generation — fail

```
(empty)
```

## At play — Mastermind

- Mastermind, seed 42 (secret [6, 1, 1, 6]): did NOT solve within 12 guesses; invalid guesses 12, repeat guesses 0.
- Full move record: games/records/match-nemotron-35-lightning-42.json

League table: games/league.md

**How it played:** format-brittle (guesses that did not parse); did not converge on this secret. (Assembled from the match record by the bench harness.)

## Process log

How this entry came to be — decisions, dead ends, and deviations, recorded as they happened:

- 2026-10-26T17:47:52 chain start: Nemotron-3.5-Lightning (Ollama) (nemotron-3.5-lightning:latest) via http://127.0.0.1:11434/v1
- 2026-10-26T17:48:17 bench.py exit=0 in 24s
- 2026-10-26T17:48:59 battery exit=0 in 42s
- 2026-10-26T17:51:38 mastermind exit=0 in 159s
- 2026-10-26T17:52:09 writings exit=0 in 31s

## Casting note

Battery 2/7 passed; mean decode 734.5 tok/s across battery probes; Mastermind seed 42: unsolved in 12 guesses. Full judgement from the numbers and verbatim outputs above. (Casting note assembled from the record by the bench harness.)
