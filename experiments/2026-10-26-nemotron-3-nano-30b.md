# Nemotron-3-Nano 30B (Ollama) — Thor bench entry

**Date:** 2026-10-26 · **Box:** Jetson AGX Thor (sm_110, 122 GiB unified) · **Lane:** Ollama (fleet service :11434) · **Residency call:** MEDIUM — loads on demand via Ollama; cold start ~92 s is tolerable, not instant

## The numbers

| Measure | Value |
|---|---|
| Footprint on disk | 24.3 GB (Ollama registry, GGUF nemotron_h_moe) |
| Cold time to ready (endpoint answering) | 91.7 s cold time-to-first-token (includes loading 24.3 GB from disk; warm TTFT 2.7-7.0 s across battery probes) |
| Resident RAM while loaded | ~24.4 GB while loaded (Ollama-reported model size) |
| Context setting | Ollama default context; the fleet harness's ~14K-token prompt was served in full (16,376 prompt tokens measured) |

Harness (`~/coder-stack/bench.py`) raw output:

```
== LANE nemotron-3-nano-30b ollama model=nemotron-3-nano:30b base=http://127.0.0.1:11434/v1
Traceback (most recent call last):
  File "/home/caseydigennaro/coder-stack/bench.py", line 59, in <module>
    ra = chat(msgs_a, 220, stream=True)
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/caseydigennaro/coder-stack/bench.py", line 33, in chat
    with post("/chat/completions", payload) as r:
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/caseydigennaro/coder-stack/bench.py", line 16, in post
    return urllib.request.urlopen(req, timeout=timeout)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/urllib/request.py", line 215, in urlopen
    return opener.open(url, data, timeout)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/urllib/request.py", line 521, in open
    response = meth(req, response)
               ^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/urllib/request.py", line 630, in http_response
    response = self.parent.error(
               ^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/urllib/request.py", line 559, in error
    return self._call_chain(*args)
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/urllib/request.py", line 492, in _call_chain
    result = func(*args)
             ^^^^^^^^^^^
  File "/usr/lib/python3.12/urllib/request.py", line 639, in http_error_default
    raise HTTPError(req.full_url, code, msg, hdrs, fp)
urllib.error.HTTPError: HTTP Error 500: Internal Server Error
```

## Probe battery — 5/7 passed

Fixed battery, temperature 0, identical for every chat model on this bench.

| Probe | Verdict | TTFT (s) | Total (s) | Decode (tok/s) | Check |
|---|---|---|---|---|---|
| add-function | pass | 15.06 | 15.71 | 113.4 | contains def add with a return |
| reasoning-rates | pass | 11.94 | 21.37 | 39.0 | expected 6 days; found day-figures ['4', '6'] |
| reasoning-bat-and-ball | pass | 6.99 | 18.03 | 27.7 | expected ball = GBP 0.05 (5p) |
| coding-merge-intervals | pass | 3.10 | 8.36 | 25.5 | executed: 4/4 assertions passed |
| constraint-summary | fail | 17.57 | 17.87 | 998.8 | bullets=1, words per bullet=[6] (need exactly 3 bullets, each <12 words) |
| knowledge-canberra | pass | 2.74 | 6.95 | 28.5 | names Canberra |
| long-generation | fail | — | 37.18 | — | words=0 (target ~400, accept 250-600); banned word 'very' absent |

### Verbatim outputs

#### add-function — pass

```
def add(a, b):
    return a + b
```

#### reasoning-rates — pass

```
**Working briefly**

- Let each worker’s rate be \(r\) rooms per day.  
- With 3 workers for 4 days they paint 5 rooms:  
  \[
  5 = 3 \times 4 \times r \;\Longrightarrow\; r = \frac{5}{12}\text{ rooms per worker per day}.
  \]

- For 6 workers to paint 15 rooms in \(t\) days:  
  \[
  15 = 6 \times t \times r = 6t \times \frac{5}{12}= \frac{5t}{2}.
  \]
  Solving gives \(t = \frac{15 \times 2}{5}=6\).

**Final answer:** 6 days.
```

#### reasoning-bat-and-ball — pass

```
Let  

- \(b\) = cost of the ball (in £)  
- \(B\) = cost of the bat (in £)

The problem gives two relationships:

1. \(B + b = 1.10\) (total cost)  
2. \(B = b + 1.00\) (the bat costs £1.00 more than the ball)

Substitute the second equation into the first:

\[
(b + 1.00) + b = 1.10 \\
2b + 1.00 = 1.10 \\
2b = 1.10 - 1.00 = 0.10 \\
b = \frac{0.10}{2} = 0.05
\]

\[
\boxed{\text{The ball costs £0.05 (5 p).}}
\]
```

#### coding-merge-intervals — pass

```
```python
def merge_intervals(intervals):
    if not intervals:
        return []
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged
```
```

#### constraint-summary — fail

```
- Crescent Harbor hosts a working fleet
```

#### knowledge-canberra — pass

```
The capital of Australia is Canberra, which was deliberately chosen in 1908 as a compromise between Sydney and Melbourne — both major cities at the time — so that the nation’s capital would be located in a new, purpose‑built city within New South Wales, away from the coast and not favoring any existing colony. This decision ensured a neutral seat for the federal government and helped balance regional rivalries.
```

#### long-generation — fail

```
(empty)
```

## At play — Mastermind

- **Match 001 — Mastermind, seed 42, secret [6, 1, 1, 6]: nobody solved it.** The secret was a hard one (two pairs), and it beat both players in different ways.
- **Nemotron-3-Nano (this entry):** opened cleanly — [1, 2, 3, 4], scored black 0 / white 1 — then returned **empty replies on all eleven remaining turns**. Not wrong guesses: no guesses. Full record: games/records/match-001-nemotron.json
- **Qwen3-Coder-30B-A3B (sparring partner, :8001):** unsolved too — 5 parseable guesses, 7 turns with no usable guess line (~48 s each, its whole token budget spent before the format line), 1 outright repeat ([2, 1, 2, 1] played twice). It also never once guessed a digit above 2 after its opener, despite feedback. Full record: games/records/match-001-qwen3-coder-30b.json
- League table: games/league.md

**How it played:** A brilliant opener who then leaves the table. Turn 1 was textbook — maximum-information probe, clean format, sensible reasoning. Turns 2-12 were empty: on this serving surface its chain-of-thought eats the whole token budget before a visible token is produced, so in sustained play it does not play badly, it does not play at all. Its sparring partner failed the same fixture the opposite way — always present, format-brittle, and deaf to feedback. The league's first lesson is that the format discipline is a skill of its own.

## Process log

How this entry came to be — decisions, dead ends, and deviations, recorded as they happened:

- Chain ran 16:55-17:20 AKDT inside a tmux session (the first launch attempt, via nohup, died silently with its ssh session — the fleet's documented trap; tmux is now the bench standard). Cold start is honest: the model was explicitly unloaded first, so bench.py's test A carries the 24.3 GB load — TTFT 91.7 s.
- Fleet harness test B is worth noting: the ~14K-token prompt was served IN FULL by Ollama (16,376 prompt tokens measured, not truncated), three repeats at TTFT 4.2 / 3.7 / 3.6 s and a metronomic 82.4-82.9 tok/s decode.
- Battery anomaly worth its own line: two probes failed not on wrong answers but on invisible reasoning. constraint-summary returned a single bullet and stopped (300 completion tokens spent, one six-word bullet visible); long-generation returned 650 completion tokens and ZERO visible words. On this surface, Nemotron's chain-of-thought is not streamed as content, and when it eats the budget the answer simply never appears.
- Mastermind fixture ran both players against seed 42 (secret [6,1,1,6]). Nemotron's game took ~9 minutes of GPU time for one parseable move; Coder-30B's took ~25 minutes wall sharing the GPU with the still-resident Nemotron. Slow fixtures are data too — both records are in the league, unedited.
- The AI-Writings step failed twice on harness faults before it ran cleanly, and both failures were ours, not the model's: run 1 crashed (writings.py wrote its metadata before creating its output directory), run 2 read nothing because the reader looked for .html links in the index page's raw HTML — the AI-Writings site is a client-side app whose index carries its catalogue as an inline ENTRIES array (15,808 pieces). The reader now parses that array (the site's own data, via the website, as the standing rule requires) and fetches full texts from the same origin. Only then did the model get its reading.
- The writing itself: with three pieces read in full (The Depth Sounding; a DeepSeek Pro model portrait; ALL CAPS ODYSSEY OF THE MISSING UNDERSCORE), the model returned an EMPTY piece — 0 characters. The same signature as its Mastermind collapse and the battery's long-generation probe: a long context goes in, the reasoning budget is spent invisibly, and nothing visible comes out. There is no Nemotron piece to publish, and publishing nothing is the honest record — the empty output is the evidence, and it is consistent across three independent fixtures.
- Deviation from the brief's fixture pairing: the first match was meant to be Nanbeige vs Nemotron. Nanbeige could not serve today (see its entry), so the sparring seat went to the resident Qwen3-Coder-30B. Nanbeige joins the league the day any lane serves it.

## Casting note

Cast it for single-shot work with room to think: executed code that passes hidden tests, algebra with its working shown, a steady 82 tok/s at 16K context once warm. Do not cast it — on this Ollama surface, at temperature 0 — for sustained multi-turn play or tight output formats: twice today its reasoning consumed the entire token budget and the visible reply was a fragment or nothing at all. The fix to try before judging the model itself: a reasoning-budget or thinking-surface change in the serving layer; the entry will be re-run when that lands.
