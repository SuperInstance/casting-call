# Nemotron-3-Nano-Omni-30B-A3B-Reasoning (NVFP4) — Thor bench entry

**Date:** 2026-10-26 · **Box:** Jetson AGX Thor (sm_110, 122 GiB unified) · **Lane:** vLLM (NGC 26.03 container) · **Residency call:** COLD until a serving lane works

> **Outcome: FAILED TO SERVE.** vLLM endpoint never became ready within 9 minutes; engine stalled during weight load (same signature as the Nanbeige attempts).

## The numbers

| Measure | Value |
|---|---|

## Process log

How this entry came to be — decisions, dead ends, and deviations, recorded as they happened:

- vLLM container started with fleet-corrected flags (VLLM_NVFP4_GEMM_BACKEND=cutlass, VLLM_USE_FLASHINFER_MOE_FP4=0, gpu-memory-utilization 0.30, enforce-eager, no prefix caching).
- Readiness poll exhausted at 9 minutes with no /v1/models answer.
- Engine log tail:
- Server pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/engine/arg_utils.py", line 1477, in create_engine_config
(APIServer pid=1)     model_config = self.create_model_config()
(APIServer pid=1)                    ^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/vllm/engine/arg_utils.py", line 1329, in create_model_config
(APIServer pid=1)     return ModelConfig(
(APIServer pid=1)            ^^^^^^^^^^^^
(APIServer pid=1)   File "/usr/local/lib/python3.12/dist-packages/pydantic/_internal/_dataclasses.py", line 121, in __init__
(APIServer pid=1)     s.__pydantic_validator__.validate_python(ArgsKwargs(args, kwargs), self_instance=s)
(APIServer pid=1) pydantic_core._pydantic_core.ValidationError: 1 validation error for ModelConfig
(APIServer pid=1)   Value error, The repository /models/Nemotron-3-Nano-Omni-30B-A3B-Reasoning-NVFP4 contains custom code which must be executed to correctly load the model. You can inspect the repository content at /models/Nemotron-3-Nano-Omni-30B-A3B-Reasoning-NVFP4 .
(APIServer pid=1)  You can inspect the repository content at https://hf.co//models/Nemotron-3-Nano-Omni-30B-A3B-Reasoning-NVFP4.
(APIServer pid=1) Please pass the argument `trust_remote_code=True` to allow custom code to be run. [type=value_error, input_value=ArgsKwargs((), {'model': ...rocessor_plugin': None}), input_type=ArgsKwargs]
(APIServer pid=1)     For further information visit https://errors.pydantic.dev/2.12/v/value_error


## Casting note

Not yet castable: no working local serving lane at entry time. Record stands as the failure evidence.
