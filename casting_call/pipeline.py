"""
Pipeline integration for casting-call.

One-function integration: the pipeline imports `cast(role)` and gets back
a model name. This is the bridge between Layer 8 (casting) and Layers 9+
(pipeline execution).

Usage:
    from casting_call.pipeline import cast, get_profile, get_tempo

    model_name = cast("intent_parse")        # → "SEED_MINI"
    profile = get_profile("intent_parse")    # → ModelProfile(...)
    tempo = get_tempo("intent_parse")        # → (120, 140)

The atlas and director are module-level singletons — created once on import.
For testing, inject a custom director via `configure()`.
"""

from __future__ import annotations
from typing import Optional

from casting_call.atlas import ModelAtlas, ModelProfile
from casting_call.casting import CastingDirector
from casting_call.tempo_profiles import ROLE_TEMPO_PROFILES


# Module-level singletons — created once, used by all pipeline stages.
_atlas: ModelAtlas = ModelAtlas.default()
_director: CastingDirector = CastingDirector(_atlas)


def cast(role: str, **context) -> str:
    """
    Cast a role to a model name.

    This is the primary integration point. The pipeline calls this before
    each stage to determine which model to invoke.

    Args:
        role: Pipeline role (e.g., 'intent_parse', 'code_gen', 'voice').
        **context: Optional constraints:
            - cost_ceiling: max cost per 1k tokens
            - exclude: list of model names to skip
            - prefer_speed: prefer faster models

    Returns:
        Model name string (e.g., 'SEED_MINI').

    Example:
        >>> from casting_call.pipeline import cast
        >>> cast("intent_parse")
        'SEED_MINI'
        >>> cast("code_gen", cost_ceiling=0.0001)
        'DEEPSEEK_V4_FLASH'
    """
    return _director.cast(role, context or {}).name


def get_profile(role: str, **context) -> ModelProfile:
    """
    Cast a role and return the full ModelProfile.

    Use this when you need more than just the name — e.g., temperature,
    voice character, failure modes.
    """
    return _director.cast(role, context or {})


def get_tempo(role: str) -> tuple[int, int]:
    """
    Get the BPM tempo range for a role.

    Returns:
        (low_bpm, high_bpm) tuple.
    """
    profile = ROLE_TEMPO_PROFILES.get(role)
    if profile is None:
        raise ValueError(f"Unknown role: {role!r}")
    return (profile.bpm_low, profile.bpm_high)


def configure(director: CastingDirector) -> None:
    """
    Inject a custom CastingDirector (for testing or custom atlases).

    Usage:
        atlas = ModelAtlas(my_custom_models)
        director = CastingDirector(atlas)
        configure(director)
    """
    global _director, _atlas
    _director = director
    _atlas = director.atlas


def available_roles() -> list[str]:
    """All roles the casting director knows about."""
    from casting_call.casting import _ROLE_DEFAULTS
    return list(_ROLE_DEFAULTS.keys())


def available_models() -> list[str]:
    """All model names in the atlas."""
    return [m.name for m in _atlas.all()]
