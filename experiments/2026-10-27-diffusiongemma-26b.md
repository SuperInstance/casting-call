# DiffusionGemma-26B-A4B-it (GGUF Q4_K_M) — Thor bench entry

**Date:** 2026-10-27 · **Box:** Jetson AGX Thor (sm_110, 122 GiB unified) · **Lane:** llama.cpp PR #24427 `llama-server` (the diffusion-gemma fork build kept in `~/diffusion-lab/llama-dg/`), run as a temporary bench instance on :8003 and stopped after the run · **Residency call:** LOW as a resident for now — the only runtime on this box that serves the architecture is an unmerged research PR — but it genuinely serves, and the built server stays in the lab for a one-command revival.

## The numbers

| Measure | Value |
|---|---|
| Footprint on disk | 16.81 GB — a single GGUF Q4_K_M (16,806,810,208 B, unsloth/diffusiongemma-26B-A4B-it-GGUF); sha256 verified on arrival 2026-10-24 (`24523b6c…028bc5`) |
| Cold time to ready | ~12 s from launch to `/health` ok (weights NVMe-resident; the load is inside that figure) |
| Resident memory while loaded | ~17 GB (16.8 GB of weights fully offloaded, `-ngl 99`, plus KV cache at `-c 4096`) |
| Context setting | `-c 4096` requested (trained context 262,144); generation itself proceeds in fixed 512-token canvases whatever the context — see the decode note |
| Decode rate | 42.1–42.9 tok/s on every probe — canvas throughput, not autoregressive decode (note below) |
| TTFT | 0.18–0.35 s (first streamed chunk) |

## Why this model needed a different runtime — the "can't work", itemised

The bench's first attempt died at load with `unknown model architecture: 'diffusion-gemma'`, and that verdict is permanent for mainline llama.cpp: DiffusionGemma is a **block-diffusion** decoder — it fills a 512-token canvas of masked tokens and denoises it over repeated passes — not an autoregressive causal LM, and mainline has no implementation of the architecture. The routes surveyed on 2026-10-27:

1. **Hugging Face transformers (the brief's first route) — no route with the weights on this box.** transformers 5.20.2 in `~/ml/.venv` does carry a `diffusion_gemma` model package, but the box holds GGUF weights only, and transformers cannot consume a bare GGUF file. Pointed at the GGUF it fails immediately:
   ```
   OSError: It looks like the config file at '/home/caseydigennaro/diffusion-lab/models/diffusiongemma-26B-A4B-it-Q4_K_M.gguf' is not a valid JSON file.
   ```
   The official BF16 checkpoint (50.5 GB) was never downloaded, so this route would need a new download before it could even be tested. Not started.
2. **vLLM (the brief's second route) — no route.** There is no NGC vLLM container on the box, and the on-box weights are GGUF, which vLLM does not serve. The documented vLLM+NVFP4 stall pattern (Omni, Nanbeige) does not apply here — this is a different failure class entirely: no checkpoint in a format vLLM can read.
3. **The box's own purpose-built stack — the route that worked.** `~/diffusion-lab/` already held llama.cpp **PR #24427** ("Add diffusion-gemma block-diffusion support", still open upstream; tree at its current head `dd0cf04`), fetched and built for sm_110 on 2026-10-23. Two findings from this morning's audit qualify the lab's own record:
   - **The model had never actually generated on this box.** The PR's CLI asserts unless exactly one denoising schedule is set (`GGML_ASSERT((params.diffusion.eps == 0) ^ (params.diffusion.block_length == 0))`), and both invocations the lab shipped — the arrival smoke test and `lab_server.py` — omit both flags. The arrival log's "smoke exit=0" was a bookkeeping error: the smoke log itself shows the assert and a core dump.
   - **With a schedule set, the CLI still cannot generate.** Its host-side generate loop (in `examples/diffusion/diffusion.cpp`) re-submits the whole canvas each step with positions restarting at 0, and this llama.cpp's batch allocator rejects any batch that does not continue the stored KV positions (`it is required that the sequence positions remain consecutive: Y = X + 1` — last stored position 511, batch starting at 0). Every schedule and fallback combination tried (block-length 32; eps 0.001; larger ubatch; device fast paths off; `--run-max-denoising-step`) failed on that check, at step 1 or at block boundaries, with zero tokens generated. The PR's **server** path manages the canvas on-device and never passes through that validation — but the server target had never built, because its webui asset step failed (a Hugging Face bucket download, and then an embed tool demanding a `loading.html` that the b50 asset tar does not contain). Fixed on 2026-10-27: reconfigure with `-DLLAMA_BUILD_UI=OFF -DLLAMA_USE_PREBUILT_UI=OFF`, let the asset provisioning fall back to the downloaded dist (splash PNGs set aside), supply a minimal `loading.html` — `llama-server` then builds clean.
   - Served as: `llama-server -m diffusiongemma-26B-A4B-it-Q4_K_M.gguf --port 8003 --host 127.0.0.1 -ngl 99 -c 4096 --reasoning-format none`. The last flag matters for bench comparability: without it, the server routes the model's entire output into `reasoning_content` and leaves `content` empty; with it, the raw stream — including the model's native `<|channel>thought … <channel|>` segment — arrives in `content`, the surface every other bench entry is graded on.

## Probe battery — 5/7 passed

Fixed battery, temperature 0, identical for every chat model on this bench. Full outputs in `~/thor-bench/results/diffusiongemma-26b/battery-r3.json`.

| Probe | Verdict | TTFT (s) | Total (s) | Decode (tok/s) | Check |
|---|---|---|---|---|---|
| add-function | pass | 0.24 | 3.57 | 42.1 | contains def add with a return |
| reasoning-rates | fail | 0.22 | 14.40 | 42.3 | expected 6 days; found day-figures ['4', '4'] |
| reasoning-bat-and-ball | pass | 0.21 | 9.55 | 42.4 | expected ball = GBP 0.05 (5p) |
| coding-merge-intervals | pass | 0.20 | 10.03 | 42.5 | executed: 4/4 assertions passed |
| constraint-summary | fail | 0.35 | 7.40 | 42.5 | bullets=13, words per bullet=[5, 6, 10, 16, 9, 10, 8, 7, 9, 20, 21, 19, 15] (need exactly 3 bullets, each <12 words) |
| knowledge-canberra | pass | 0.18 | 4.84 | 42.9 | names Canberra |
| long-generation | pass | 0.21 | 15.53 | 42.4 | words=421 (target ~400, accept 250-600); banned word 'very' absent |

**A note on the decode figures.** The near-identical ~42 tok/s on every probe is the honest signature of block diffusion: the server fills a fixed 512-token canvas in a fixed number of denoising steps, so "tokens per second" is canvas throughput. It does not speed up on easy prompts or slow down on hard ones, and the reported completion-token counts are canvas positions, not autoregressive steps. TTFT is likewise the first streamed canvas state. Comparisons with autoregressive entries should be made on wall-clock totals, which are competitive throughout (3.6–15.5 s per probe).

**The two failures are budget-and-format failures, not knowledge failures** — the same disease family as Nemotron-3-Nano's invisible-chain-of-thought losses, by the opposite mechanism: this model's thought channel is fully visible, and expensive.

- *reasoning-rates* derived the correct answer twice inside its thought channel (`$D_2 = 6$`; "Days for 15 rooms = $15 / 2.5 = 6$ days"), but the 600-token budget ran out inside the post-thought answer segment — it begins ("To find the number of days, we can calculate the rate of work: 1. **") and is cut before restating the figure, so the checker's extraction found only the givens.
- *constraint-summary* planned correctly ("Exactly three bullet points… Each bullet point must be under 12 words") and then produced thirteen bullets across thought and answer segments, several over the word limit.

Verbatim, add-function (the whole shape of every response: thought channel, then the answer):

```
<|channel>thought
*   Goal: Write a Python function `add(a, b)`.
    *   Functionality: Return the sum of `a` and `b`.
    *   Constraint: "Code only."

    ```python
    def add(a, b):
        return a + b
    ```

    *   Is it Python? Yes.
    *   Is it the function `add(a, b)`? Yes.
    *   Does it return the sum? Yes.
    *   Is it code only? Yes.<channel|>```python
def add(a, b):
    return a + b
```
```

And the bat-and-ball answer segment, for the record: "The ball costs **GBP 0.05** (or 5p)." — with the simultaneous-equation working shown in full.

## At play — Mastermind

Fixture: seed 42, secret [6, 1, 1, 6], at most 12 guesses, temperature 0. Record: `games/records/match-diffusiongemma-26b-42.json`.

- **Turn 1:** a clean, parseable opener, `GUESS: 1 2 3 4` → black 0, white 1. Textbook.
- **Turns 2–12:** no valid guess at all (invalid 11, repeats 0, solved_turn none). The failure is visible in the record: on turn 2 the thought channel degenerates into a repetition loop ("first first first first…" to the end of the raw output) and the 900-token budget dies inside the thought segment before any GUESS line is emitted; the later turns repeat the pattern of thought-first, budget-out. The model never gets to use the feedback it was given.

Against the table: Nemotron-3-Nano also failed this secret (textbook opener, then eleven empty turns); Qwen3-Coder-30B managed five parseable guesses. DiffusionGemma sits with the former — one good move, then drowned by its own reasoning format.

## Process log

- Recon: weights are GGUF only (16,806,810,208 B, arrival hash on record); no safetensors anywhere on the box. Thor at 122 GiB unified, ~74 GiB available, GPU idle; residents (Coder-30B llama-server, NemoClaw sandbox, governor) untouched throughout.
- Route 1, transformers: package present in transformers 5.20.2; GGUF load fails with the OSError above. Closed without a download.
- Route 2, vLLM: no container on the box and no servable checkpoint format. Closed as no-route; the ≤25-minute attempt was never needed.
- Route 3, the lab's PR #24427 build: read the lab's own README route survey, then tested the CLI. Found the schedule assert, then the KV-position validation failure; read both in source (`diffusion-cli.cpp`, `examples/diffusion/diffusion.cpp`, `src/llama-batch.cpp`) rather than guessing flags. Checked upstream — the local tree is already the PR's current head, so no fix was coming from there.
- Built the PR's `llama-server` (the step two previous crews had failed on): the webui asset provisioning was the whole problem; with the UI build and prebuilt-download paths off, the downloaded dist embedded once a minimal `loading.html` was supplied. Splash PNGs set aside in the build tree only; nothing in the lab's sources was modified.
- Served on :8003 with `--reasoning-format none` after the first smoke test showed the default parsing hiding all output in `reasoning_content`. Smoke paragraph correct and coherent in 6.4 s end to end; battery and Mastermind then ran unchanged, on the standard harness. Server stopped afterwards; the box was left as found.

## Casting note

DiffusionGemma works here — that is the headline, after a week of "unknown model architecture". On the standard battery it scores **5/7, level with Nemotron-3-Nano-30B**, with faster wall-clock totals than that entry on most probes, fully visible reasoning (a genuine interpretability plus beside Nemotron's invisible chain-of-thought), and correct reasoning even in one of its two failures. Its weaknesses are structural: a thought channel that spends the token budget before the answer lands, format discipline that collapses under tight constraints, and a Mastermind game lost to a repetition loop. As a casting candidate it is a characterful oddity rather than a workhorse — the only block-diffusion model on the bench, worth keeping revivable in the lab and worth re-testing if PR #24427 merges and the serving path hardens.
