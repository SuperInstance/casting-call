# Thor bench entries

Measured experiments on models running **locally** on the fleet's Jetson AGX Thor
(122 GiB unified memory, sm_110), run by the bench lane in `~/thor-bench/` on that
machine. One dated entry per model per experiment day.

The atlas in the top-level README is the curated score. These entries are the
audition tapes: raw numbers, verbatim outputs, game records, the model's own
writing, and a process log — decisions, dead ends, and failures included, in the
body of the entry, as they happened. A result without its process is a claim,
not a record.

## What every chat-model entry runs

1. **Fleet harness** (`bench.py`, from the Thor's coder-stack BENCH-PLAN):
   test A — short coding generation (decode tok/s, TTFT); test B — a ~14K-token
   code-context prompt, three repeats (TTFT/total per repeat). Cold
   time-to-first-token is measured from an unloaded model where the lane
   allows it, and labelled when it is.
2. **Fixed probe battery** — identical for every chat model, temperature 0:
   an `add()` function, two checkable reasoning problems, a coding task whose
   output is *executed* against hidden tests, a constrained summary
   (exactly three bullets, under 12 words each), a knowledge probe, and a
   ~400-word generation. Verbatim outputs are kept in the entry.
3. **A game** — Mastermind (see `../games/`): 4 pegs, digits 1–6, black/white
   feedback, 12 guesses at most, seeded secrets shared across the league.
4. **A piece of writing** — the model reads a handful of pieces from the
   AI-Writings corpus *through its website*, then writes one short original
   piece, published unedited under `local-models/<model-slug>/` in the
   AI-Writings repo and linked from the entry. How a model writes is part
   of how it is cast.

3D-generation models take the gen3d scorecard route instead (canonical
cathedral subject, official package, mesh statistics, process log).

Residency labels follow the coder-stack convention: HOT stays resident,
MEDIUM loads on demand, COLD is a seed on disk. Failures are entries too —
a model that will not serve is a finding, and its entry says exactly where
it stopped.
