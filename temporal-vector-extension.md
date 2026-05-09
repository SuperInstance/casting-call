# Temporal Dimensions for PLATO Vector Persistence

**FM's suggestion #3 — Add time as an explicit embedding dimension.**

## Problem
Current embeddings encode: (domain, question, answer, confidence, trust_score). They do NOT encode: when the knowledge was relevant, when it was last validated, when it's expected to expire.

## Solution
Add 3 temporal dimensions to the embedding vector, making it 387d instead of 384d:

- **t_created** (dim 384) — normalized timestamp of tile creation (0 = epoch, 1 = now)
- **t_last_validated** (dim 385) — normalized timestamp of last validation by another agent
- **t_horizon** (dim 386) — expected relevance horizon (0 = ephemeral, 1 = permanent)

## Why This Matters
Without temporal dimensions, a tile from 2025 about "best LLM practices" is equally similar to a tile from 2026 about the same topic. With temporal dimensions, the distance increases as the knowledge ages. Agents can filter by temporal proximity — "find me tiles that were relevant within the last N days."

## Implementation
The embedding pipeline (plato-vector-persistence.md) already stores metadata alongside vectors. The temporal dimensions are computed at embedding time from the tile's timestamp and agent trust model.

```
# Before: [e0, e1, ..., e383] — 384d semantic embedding
# After: [e0, e1, ..., e383, t_created, t_last_validated, t_horizon] — 387d with temporal
```

The GPU similarity kernel already parameterizes DIM at launch time. Changing from 384 to 387 requires only changing the DIM constant.

## Stitching Parameter Database

**Bridge to FM's fleet-stitch.**

The stitching parameter database stores, for each (source_model, target_model) pair, the affine mapping Wx + b that translates between their residual streams. This is the metadata that the casting-call MCP serves when an agent asks "can I stitch model A onto model B?"

Schema:
```json
{
  "stitch_pairs": [
    {
      "source": "deepseek/deepseek-v4-flash",
      "target": "zai/glm-5.1",
      "layer": 12,
      "W_shape": [4096, 4096],
      "W_available": false,    // true when FM has computed it
      "accuracy": null,        // placeholder for validation score
      "notes": "FM building fleet-stitch for this pair"
    }
  ]
}
```

When FM's fleet-stitch computes a mapping, it pushes the parameters here. The casting-call then knows: (1) this stitch exists, (2) what its accuracy is, (3) which layers are mapped. The MCP server serves this data to any agent that asks.
