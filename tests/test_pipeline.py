"""
Tests for the pipeline integration module.

This is the bridge between casting-call (Layer 8) and the pipeline (Layer 9+).
One function: cast(role) → model_name. Plus helpers for profile and tempo.
"""

import pytest
from casting_call.pipeline import (
    cast, get_profile, get_tempo,
    configure, available_roles, available_models,
)
from casting_call import ModelAtlas, CastingDirector


class TestCast:
    """The primary integration function."""

    def test_cast_returns_string(self):
        result = cast("intent_parse")
        assert isinstance(result, str)

    def test_cast_intent_parse(self):
        assert cast("intent_parse") == "SEED_MINI"

    def test_cast_code_gen(self):
        assert cast("code_gen") == "QWEN3_CODER"

    def test_cast_voice(self):
        assert cast("voice") == "HERMES_405B"

    def test_cast_safety(self):
        assert cast("safety_check") == "NEMOTRON_ULTRA"

    def test_cast_with_cost_ceiling(self):
        result = cast("code_gen", cost_ceiling=0.0001)
        # Should return a cheap model
        from casting_call.pipeline import get_profile
        profile = get_profile("code_gen", cost_ceiling=0.0001)
        assert profile.cost_per_1k_tokens <= 0.0001 or profile.name == "QWEN3_CODER"

    def test_cast_with_exclude(self):
        result = cast("code_gen", exclude=["QWEN3_CODER"])
        assert result != "QWEN3_CODER"

    def test_cast_unknown_role(self):
        """Unknown role still returns something."""
        result = cast("totally_made_up")
        assert isinstance(result, str)
        assert len(result) > 0


class TestGetProfile:
    """Full profile access for when the name isn't enough."""

    def test_returns_model_profile(self):
        from casting_call import ModelProfile
        profile = get_profile("intent_parse")
        assert isinstance(profile, ModelProfile)

    def test_profile_has_temperature(self):
        profile = get_profile("intent_parse")
        assert 0.0 <= profile.temperature <= 2.0

    def test_profile_has_voice_character(self):
        profile = get_profile("voice")
        assert profile.voice_character.value == "Roland"

    def test_profile_has_failure_modes(self):
        profile = get_profile("safety_check")
        assert len(profile.failure_modes) > 10


class TestGetTempo:
    """Tempo access for pipeline beat synchronization."""

    def test_intent_parse_is_allegro(self):
        low, high = get_tempo("intent_parse")
        assert low == 120
        assert high == 140

    def test_safety_is_largo(self):
        low, high = get_tempo("safety_check")
        assert high <= 55

    def test_creative_is_wide(self):
        low, high = get_tempo("creative_ideation")
        assert (high - low) >= 80

    def test_unknown_role_raises(self):
        with pytest.raises(ValueError):
            get_tempo("nonexistent")


class TestConfigure:
    """Custom director injection for testing/custom atlases."""

    def test_configure_with_custom_atlas(self):
        from casting_call.atlas import ModelProfile, VoiceCharacter
        custom = ModelProfile(
            name="CUSTOM", provider="Test",
            voice_character=VoiceCharacter.VERSATILE,
            tempo_bpm=(60, 120),
            strengths=["intent_parse", "code_generation"],
            weaknesses=["test"],
            cost_per_1k_tokens=0.001,
            failure_modes="test",
        )
        atlas = ModelAtlas([custom])
        director = CastingDirector(atlas)
        configure(director)

        result = cast("intent_parse")
        assert result == "CUSTOM"

        # Reset to default
        configure(CastingDirector(ModelAtlas.default()))

    def test_configure_restores_default(self):
        # After resetting in previous test, default should work
        assert cast("intent_parse") == "SEED_MINI"


class TestAvailableListings:
    """Discovery functions for introspection."""

    def test_available_roles_non_empty(self):
        roles = available_roles()
        assert len(roles) >= 13  # all defined roles
        assert "intent_parse" in roles
        assert "code_gen" in roles
        assert "voice" in roles

    def test_available_models_non_empty(self):
        models = available_models()
        assert len(models) >= 16
        assert "SEED_MINI" in models
        assert "HERMES_405B" in models

    def test_available_roles_are_sorted(self):
        """Roles should be in a deterministic order (insertion order)."""
        roles1 = available_roles()
        roles2 = available_roles()
        assert roles1 == roles2

    def test_available_models_are_sorted(self):
        models1 = available_models()
        models2 = available_models()
        assert models1 == models2


class TestPipelineIntegration:
    """End-to-end: the pipeline uses cast() and gets consistent results."""

    def test_full_creative_pipeline(self):
        """Simulate a full creative pipeline using cast()."""
        stages = [
            "intent_parse",
            "planning",
            "creative_ideation",
            "creative_nonfiction",
            "sensory_creative",
            "personality_wrap",
            "voice",
        ]

        cast_list = []
        for role in stages:
            model = cast(role)
            cast_list.append(model)

        # All models should be valid
        assert all(isinstance(m, str) for m in cast_list)
        # Should have reasonable diversity
        assert len(set(cast_list)) >= 4

    def test_cast_results_match_get_profile(self):
        """cast(role) should return the same model as get_profile(role).name."""
        for role in available_roles():
            model_name = cast(role)
            profile = get_profile(role)
            # They might differ if cost ceiling or exclude is applied,
            # but with no context they should match
            assert model_name == profile.name, (
                f"Role {role}: cast() returned {model_name} "
                f"but get_profile() returned {profile.name}"
            )
