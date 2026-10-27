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

[stderr]
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

## Probe battery — 0/7 passed

Fixed battery, temperature 0, identical for every chat model on this bench.

| Probe | Verdict | TTFT (s) | Total (s) | Decode (tok/s) | Check |
|---|---|---|---|---|---|
| add-function | error | — | — | — | request failed: HTTP Error 500: Internal Server Error |
| reasoning-rates | error | — | — | — | request failed: HTTP Error 500: Internal Server Error |
| reasoning-bat-and-ball | error | — | — | — | request failed: HTTP Error 500: Internal Server Error |
| coding-merge-intervals | error | — | — | — | request failed: HTTP Error 500: Internal Server Error |
| constraint-summary | error | — | — | — | request failed: HTTP Error 500: Internal Server Error |
| knowledge-canberra | error | — | — | — | request failed: HTTP Error 500: Internal Server Error |
| long-generation | error | — | — | — | request failed: HTTP Error 500: Internal Server Error |

### Verbatim outputs

#### add-function — error

```
(empty)
```

#### reasoning-rates — error

```
(empty)
```

#### reasoning-bat-and-ball — error

```
(empty)
```

#### coding-merge-intervals — error

```
(empty)
```

#### constraint-summary — error

```
(empty)
```

#### knowledge-canberra — error

```
(empty)
```

#### long-generation — error

```
(empty)
```

## At play — Mastermind

- Mastermind, seed 42 (secret [6, 1, 1, 6]): did NOT solve within 12 guesses; invalid guesses 0, repeat guesses 0.
- Full move record: games/records/match-nemotron-labs-diffusion-8b-42.json

League table: games/league.md

**How it played:** did not converge on this secret. (Assembled from the match record by the bench harness.)

## Process log

How this entry came to be — decisions, dead ends, and deviations, recorded as they happened:

- 2026-10-27T10:39:33 chain start: Nemotron-Labs Diffusion 8B (nemotron-labs-diffusion-8b) via http://127.0.0.1:8003/v1
- 2026-10-27T10:39:33 bench.py exit=1 in 0s
- 2026-10-27T10:39:33 battery exit=0 in 0s
- 2026-10-27T10:39:33 mastermind exit=0 in 0s
- 2026-10-27T10:39:37 writings exit=0 in 3s

## Casting note

Battery 0/7 passed; Mastermind seed 42: unsolved in 12 guesses. Full judgement from the numbers and verbatim outputs above. (Casting note assembled from the record by the bench harness.)
