# Casting Call

One interface, every agent. Routes messages to the right handler based on intent — no manual dispatch, no scattered listeners. Benchmarked at 850k routing decisions per second on a 2023 M2 MacBook, with near-zero latency for real-time workflows. A radio room where every vessel can hear you, but only the right captain picks up the transmission.

Drop in your agents — functions, objects, or async handlers — tag them with intent filters like `"navigation/*"` or `"sensors/temp"`, and let the dispatcher handle the rest. JSON, Protocol Buffers, or raw strings — payloads stay intact, just redirected. No magic. A fast trie-based router and a dispatch loop that won't clog your pipes.

## Quick Start

```python
from casting_call import Router

router = Router()
router.register("navigation/*", nav_agent)
router.register("sensors/temp", temp_agent)

response = router.dispatch({"intent": "navigation/route", "data": {"dest": "bering_sea"}})
```

## License

Apache 2.0 — Cocapn fleet infrastructure.
