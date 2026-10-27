# The games league

Local models get known by playing, not only by benchmarks. The fixture is **Mastermind**: 4 pegs, digits 1-6, repeats allowed, black/white peg feedback, at most 12 guesses, temperature 0. Every model attacks the same seeded secrets, so results are comparable across the table and over time.

Records (every move, verbatim reasoning) live in `records/`. The league table in `league.md` is rebuilt from those records by the bench harness. A model's characterisation in its casting-call entry is read off the record: wasted or repeated guesses, format failures, speed of convergence.
