"""
casting-call — the musician's ear that knows which keyboard sounds right for which song.

Layer 8 of the Slackwater stack. Pure functions that map a pipeline role to the
right model, tempo, and prompt strategy. No I/O, no side effects — just the atlas
and the casting logic.

    >>> from casting_call import ModelAtlas, CastingDirector
    >>> atlas = ModelAtlas.default()
    >>> director = CastingDirector(atlas)
    >>> profile = director.cast("intent_parse")
    >>> profile.name
    'SEED_MINI'
"""

from casting_call.atlas import ModelAtlas, ModelProfile, VoiceCharacter
from casting_call.casting import CastingDirector
from casting_call.tempo_profiles import TempoProfile, ROLE_TEMPO_PROFILES
from casting_call.pipeline import cast, get_profile, get_tempo, configure, available_roles, available_models

__all__ = [
    "ModelAtlas",
    "ModelProfile",
    "VoiceCharacter",
    "CastingDirector",
    "TempoProfile",
    "ROLE_TEMPO_PROFILES",
    # Pipeline integration
    "cast",
    "get_profile",
    "get_tempo",
    "configure",
    "available_roles",
    "available_models",
]

__version__ = "0.1.0"
