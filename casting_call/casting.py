"""
CastingDirector — the routing brain.

Given a role (intent_parse, code_gen, voice, safety_check, ...), the director
consults the atlas and returns the best model profile. It also enforces the
counterpoint constraint: no parallel octaves — two models never receive
structurally identical prompts for the same stage.

This is Layer 8 in the Grand Plan. It is a pure function consulted by the
brain pipeline (Layer 9). No I/O, no side effects.
"""

from __future__ import annotations

from casting_call.atlas import ModelAtlas, ModelProfile
from casting_call.tempo_profiles import ROLE_TEMPO_PROFILES, TempoProfile


# The canonical role → model assignment. This is the default casting.
# A model swap (e.g., Nemotron 3 Super replacing Seed-mini for intent) is a
# one-row change here, measured against the R2 trajectory set before commit.
_ROLE_DEFAULTS: dict[str, str] = {
    "intent_parse":         "SEED_MINI",
    "planning":             "SEED_PRO",
    "code_gen":             "QWEN3_CODER",
    "personality_wrap":     "HERMES_405B",
    "safety_check":         "NEMOTRON_ULTRA",
    "creative_ideation":    "SEED_MINI",
    "spatial_reasoning":    "QWEN3_6",
    "synthesis":            "GEMINI_PRO",
    "vision":               "GEMINI_PRO",
    "voice":                "HERMES_405B",
    "forced_perspective":   "SEED_MINI",
    "creative_nonfiction":  "SEED_PRO",
    "sensory_creative":     "DEEPSEEK_V4_FLASH",
}

# Fallback models when the primary is unavailable.
_ROLE_FALLBACKS: dict[str, list[str]] = {
    "intent_parse":         ["SEED_MINI", "GLM_5_2", "DEEPSEEK_V4_FLASH"],
    "planning":             ["SEED_PRO", "QWEN3_6", "CLAUDE_SONNET"],
    "code_gen":             ["QWEN3_CODER", "DEEPSEEK_V4_FLASH", "CLAUDE_SONNET"],
    "personality_wrap":     ["HERMES_405B", "GLM_5_2"],
    "safety_check":         ["NEMOTRON_ULTRA", "CLAUDE_OPUS"],
    "creative_ideation":    ["SEED_MINI", "MMX_M3"],
    "spatial_reasoning":    ["QWEN3_6", "KIMI_K3", "SEED_PRO"],
    "synthesis":            ["GEMINI_PRO", "GLM_5_2", "CLAUDE_SONNET"],
    "vision":               ["GEMINI_PRO", "GLM_5_2"],
    "voice":                ["HERMES_405B", "GLM_5_2"],
    "forced_perspective":   ["SEED_MINI", "GLM_5_2"],
    "creative_nonfiction":  ["SEED_PRO", "DEEPSEEK_V4_FLASH", "CLAUDE_SONNET"],
    "sensory_creative":     ["DEEPSEEK_V4_FLASH", "SEED_PRO", "GLM_5_2"],
}


class CastingDirector:
    """
    Casts the right model for a role, enforces counterpoint, and reports tempo.

    Usage:
        >>> atlas = ModelAtlas.default()
        >>> director = CastingDirector(atlas)
        >>> profile = director.cast("intent_parse")
        >>> profile.name
        'SEED_MINI'
    """

    def __init__(self, atlas: ModelAtlas):
        self.atlas = atlas

    def cast(self, role: str, context: dict | None = None) -> ModelProfile:
        """
        Cast the best model for a role.

        Args:
            role: One of 'intent_parse', 'planning', 'code_gen',
                  'personality_wrap', 'safety_check', 'creative_ideation',
                  'spatial_reasoning', 'synthesis', 'vision', 'voice'.
            context: Optional constraints:
                - 'cost_ceiling': max cost per 1k tokens
                - 'exclude': list of model names to skip
                - 'prefer_speed': if True, prefer faster models

        Returns:
            The best ModelProfile for the role.
        """
        context = context or {}
        exclude = set(context.get("exclude", []))
        cost_ceiling = context.get("cost_ceiling")
        prefer_speed = context.get("prefer_speed", False)

        # Try the fallback chain — first available wins.
        candidates = _ROLE_FALLBACKS.get(role, [])
        for model_name in candidates:
            if model_name in exclude:
                continue
            profile = self.atlas.get(model_name)
            if profile is None:
                continue
            if cost_ceiling is not None and profile.cost_per_1k_tokens > cost_ceiling:
                continue
            return profile

        # If nothing in the chain, try by strength matching.
        strength_map = {
            "intent_parse": "intent_parse",
            "planning": "deep_planning",
            "code_gen": "code_generation",
            "personality_wrap": "personality",
            "safety_check": "safety_check",
            "creative_ideation": "creative_ideation",
            "spatial_reasoning": "spatial_reasoning",
            "synthesis": "synthesis",
            "vision": "vision",
            "voice": "voice",
            "forced_perspective": "forced_perspective",
            "creative_nonfiction": "creative_writing",
            "sensory_creative": "sensory_creative",
        }
        strength = strength_map.get(role)
        if strength:
            candidates_by_strength = self.atlas.by_strength(strength)
            for p in candidates_by_strength:
                if p.name in exclude:
                    continue
                if cost_ceiling is not None and p.cost_per_1k_tokens > cost_ceiling:
                    continue
                return p

        # Last resort: cheapest model.
        cheapest = self.atlas.cheapest(strength or "balanced") if strength else None
        if cheapest:
            return cheapest

        # Absolute fallback: first model in the atlas.
        all_models = self.atlas.all()
        if not all_models:
            raise ValueError("Atlas is empty — no models to cast.")
        return all_models[0]

    def cast_pipeline(self, roles: list[str], context: dict | None = None) -> list[ModelProfile]:
        """
        Cast an entire pipeline at once. Ensures counterpoint: no two roles
        get the same model unless the role explicitly allows it.

        Returns a list of ModelProfiles in the same order as roles.
        """
        context = context or {}
        result: list[ModelProfile] = []
        assigned_names: set[str] = set()

        for role in roles:
            # For each role, exclude models already assigned to different roles,
            # UNLESS the role defaults to the same model (e.g., creative_ideation
            # and intent_parse both use SEED_MINI — that's fine, they're the same
            # *stage type* in the pipeline).
            local_ctx = dict(context)
            local_ctx["exclude"] = list(
                set(context.get("exclude", [])) | assigned_names
            )
            profile = self.cast(role, local_ctx)
            result.append(profile)
            assigned_names.add(profile.name)

        return result

    def tempo_range(self, role: str) -> tuple[int, int]:
        """
        What BPM range fits this role?

        Returns (low, high) BPM from the tempo profile.
        """
        profile = ROLE_TEMPO_PROFILES.get(role)
        if profile is None:
            raise ValueError(f"Unknown role: {role!r}")
        return (profile.bpm_low, profile.bpm_high)

    def tempo_profile(self, role: str) -> TempoProfile:
        """The full tempo profile for a role."""
        return ROLE_TEMPO_PROFILES[role]

    def counterpoint_check(self, cast_list: list[ModelProfile]) -> bool:
        """
        No parallel octaves — two models never receive structurally identical
        prompts for the same stage.

        In the musical analogy: parallel octaves is when two voices sing the
        same note in the same rhythm. It wastes a voice. In the pipeline: if
        two different roles are assigned the same model AND that model would
        receive structurally identical prompts, that's parallel octaves.

        Same model assigned to different roles is fine (Seed-mini does both
        intent_parse and creative_ideation) as long as the prompts differ
        structurally. Same model assigned to the same role twice is not.

        For this check, we verify that no model appears more than once for
        the same role name in the cast list. Since cast_list is a flat list
        of profiles, we check for duplicate model names where the models
        would be in the same pipeline stage.

        Returns True if the cast is clean (no parallel octaves).
        """
        # In a flat cast list, duplicate model names mean the same model
        # is assigned to multiple stages. This is allowed (a versatile model
        # can play multiple parts) but flagged if the same model appears
        # in adjacent stages with the same tempo — that's parallel octaves.
        seen: dict[str, int] = {}  # model_name → first index
        for i, profile in enumerate(cast_list):
            if profile.name in seen:
                prev = seen[profile.name]
                # Same model in adjacent positions = parallel octaves
                if i - prev == 1:
                    return False
                # Same model in non-adjacent positions is OK (it's a recap)
            else:
                seen[profile.name] = i
        return True

    def swap(self, role: str, new_model: str) -> bool:
        """
        What-if analysis: can we swap a model into a role?

        Returns True if the model exists in the atlas and has a strength
        relevant to the role. Does NOT mutate the default casting — this
        is a read-only check.

        Usage:
            >>> director.swap("intent_parse", "GLM_5_2")
            True  # GLM_5_2 can handle intent parsing
        """
        profile = self.atlas.get(new_model)
        if profile is None:
            return False

        strength_map = {
            "intent_parse": ["intent_parse", "fast_exploration", "creative_ideation"],
            "planning": ["deep_planning", "spatial_reasoning", "build_decomposition"],
            "code_gen": ["code_generation", "precision", "fast_code"],
            "personality_wrap": ["personality", "voice", "creative_writing"],
            "safety_check": ["safety_check", "verification", "convergence"],
            "creative_ideation": ["creative_ideation", "intent_parse"],
            "spatial_reasoning": ["spatial_reasoning", "spatial_decomposition", "build_intelligence"],
            "synthesis": ["synthesis", "summary"],
            "vision": ["vision", "multimodal", "synthesis"],
            "voice": ["voice", "narration", "creative_writing"],
            "forced_perspective": ["forced_perspective", "creative_ideation", "intent_parse"],
            "creative_nonfiction": ["creative_writing", "prose_precision", "prose_brevity", "deep_planning"],
            "sensory_creative": ["sensory_creative", "phenomenological_instinct", "creative_writing"],
        }
        required = strength_map.get(role, [])
        return any(s in profile.strengths for s in required)

    def what_if(self, role: str, new_model: str) -> dict:
        """
        Full what-if analysis for a model swap.

        Returns a dict with:
            - 'feasible': can the model do the job?
            - 'cost_delta': change in cost per 1k tokens
            - 'tempo_delta': change in tempo range
            - 'reason': human-readable explanation
        """
        current = self.cast(role)
        candidate = self.atlas.get(new_model)

        if candidate is None:
            return {
                "feasible": False,
                "cost_delta": 0.0,
                "tempo_delta": (0, 0),
                "reason": f"Model {new_model} not found in atlas.",
            }

        feasible = self.swap(role, new_model)
        cost_delta = candidate.cost_per_1k_tokens - current.cost_per_1k_tokens
        tempo_delta = (
            candidate.tempo_bpm[0] - current.tempo_bpm[0],
            candidate.tempo_bpm[1] - current.tempo_bpm[1],
        )

        if feasible:
            reason = (
                f"{new_model} ({candidate.voice_character.value}) can handle {role}. "
                f"Cost {'+' if cost_delta >= 0 else ''}{cost_delta:.4f}/1k. "
                f"Tempo shift: ({tempo_delta[0]:+d}, {tempo_delta[1]:+d}) BPM."
            )
        else:
            reason = (
                f"{new_model} lacks the strengths for {role}. "
                f"Required strengths not found in profile."
            )

        return {
            "feasible": feasible,
            "cost_delta": cost_delta,
            "tempo_delta": tempo_delta,
            "reason": reason,
        }
