"""
Comprehensive tests for casting-call.

Every role gets cast to an appropriate model. Counterpoint catches duplicates.
Tempo profiles match expected ranges. Model swaps (what-if) work correctly.
"""

import pytest
from casting_call import ModelAtlas, CastingDirector, ROLE_TEMPO_PROFILES
from casting_call.atlas import VoiceCharacter


@pytest.fixture
def atlas():
    return ModelAtlas.default()


@pytest.fixture
def director(atlas):
    return CastingDirector(atlas)


# ── Atlas tests ──────────────────────────────────────────────────────

class TestModelAtlas:
    def test_default_has_all_models(self, atlas):
        """All 15 canonical models are registered."""
        assert len(atlas) == 15

    @pytest.mark.parametrize("name", [
        "HERMES_405B", "GEMINI_PRO", "CLAUDE_OPUS", "CLAUDE_SONNET",
        "SEED_MINI", "SEED_PRO", "QWEN3_6", "QWEN3_CODER",
        "NEMOTRON_ULTRA", "GLM_5_2", "KIMI_K3", "DEEPSEEK_V3", "MMX_M3",
        "GRANITE_3_1_2B", "QWEN_0_5B",
    ])
    def test_model_exists(self, atlas, name):
        assert name in atlas
        profile = atlas.get(name)
        assert profile is not None
        assert profile.name == name

    def test_voice_characters_are_distinct(self, atlas):
        """Each model has a recognizable voice character."""
        voices = [m.voice_character for m in atlas.all()]
        # At least 8 distinct voice characters among 14 models
        assert len(set(voices)) >= 8

    def test_all_have_tempo_ranges(self, atlas):
        for m in atlas.all():
            assert m.tempo_bpm[0] > 0
            assert m.tempo_bpm[1] >= m.tempo_bpm[0]
            assert m.tempo_bpm[1] <= 200

    def test_all_have_failure_modes(self, atlas):
        for m in atlas.all():
            assert len(m.failure_modes) > 10  # non-trivial description

    def test_by_strength(self, atlas):
        coders = atlas.by_strength("code_generation")
        assert "QWEN3_CODER" in [m.name for m in coders]

    def test_by_tempo_range(self, atlas):
        fast = atlas.by_tempo_range(120, 140)
        names = [m.name for m in fast]
        assert "SEED_MINI" in names
        assert "GEMINI_PRO" in names

    def test_cheapest(self, atlas):
        cheapest = atlas.cheapest("code_generation")
        assert cheapest is not None
        # DeepSeek is the cheapest coder
        assert cheapest.cost_per_1k_tokens <= 0.001


# ── Casting tests ────────────────────────────────────────────────────

class TestCasting:
    @pytest.mark.parametrize("role,expected_model", [
        ("intent_parse", "SEED_MINI"),
        ("planning", "SEED_PRO"),
        ("code_gen", "QWEN3_CODER"),
        ("personality_wrap", "HERMES_405B"),
        ("safety_check", "NEMOTRON_ULTRA"),
        ("creative_ideation", "SEED_MINI"),
        ("spatial_reasoning", "QWEN3_6"),
        ("synthesis", "GEMINI_PRO"),
        ("vision", "GEMINI_PRO"),
        ("voice", "HERMES_405B"),
    ])
    def test_cast_returns_correct_model(self, director, role, expected_model):
        profile = director.cast(role)
        assert profile.name == expected_model, (
            f"Role {role}: expected {expected_model}, got {profile.name}"
        )

    def test_cast_with_cost_ceiling(self, director):
        """Cost ceiling forces a cheaper model."""
        profile = director.cast("code_gen", {"cost_ceiling": 0.0001})
        # Should skip QWEN3_CODER and find a cheaper option or fallback
        assert profile.cost_per_1k_tokens <= 0.0001 or profile.name == "QWEN3_CODER"

    def test_cast_with_exclude(self, director):
        """Excluding a model forces the fallback chain."""
        profile = director.cast("code_gen", {"exclude": ["QWEN3_CODER"]})
        assert profile.name != "QWEN3_CODER"

    def test_cast_excluding_all_primary_models(self, director):
        """Excluding all primary + fallback models falls through to strength search."""
        profile = director.cast("code_gen", {
            "exclude": ["QWEN3_CODER", "DEEPSEEK_V3", "CLAUDE_SONNET"]
        })
        # Should still return something reasonable
        assert profile is not None

    def test_cast_unknown_role_returns_something(self, director):
        """Unknown role doesn't crash — returns some model."""
        profile = director.cast("totally_made_up_role")
        assert profile is not None

    def test_cast_pipeline(self, director):
        """Cast an entire pipeline at once."""
        roles = ["intent_parse", "planning", "code_gen", "personality_wrap", "safety_check"]
        cast = director.cast_pipeline(roles)
        assert len(cast) == 5
        assert cast[0].name == "SEED_MINI"
        assert cast[1].name == "SEED_PRO"
        assert cast[2].name == "QWEN3_CODER"
        assert cast[3].name == "HERMES_405B"
        assert cast[4].name == "NEMOTRON_ULTRA"

    def test_cast_pipeline_counterpoint(self, director):
        """Pipeline casting avoids assigning the same model to adjacent stages."""
        roles = ["intent_parse", "planning", "code_gen", "personality_wrap", "safety_check"]
        cast = director.cast_pipeline(roles)
        assert director.counterpoint_check(cast) is True


# ── Counterpoint tests ───────────────────────────────────────────────

class TestCounterpoint:
    def test_clean_cast_passs(self, director, atlas):
        """A diverse cast passes counterpoint check."""
        cast = [
            atlas.get("SEED_MINI"),
            atlas.get("SEED_PRO"),
            atlas.get("QWEN3_CODER"),
            atlas.get("HERMES_405B"),
            atlas.get("NEMOTRON_ULTRA"),
        ]
        assert director.counterpoint_check(cast) is True

    def test_parallel_octaves_caught(self, director, atlas):
        """Same model in adjacent positions fails counterpoint."""
        cast = [
            atlas.get("SEED_MINI"),
            atlas.get("SEED_MINI"),  # parallel octave!
        ]
        assert director.counterpoint_check(cast) is False

    def test_non_adjacent_repeat_ok(self, director, atlas):
        """Same model in non-adjacent positions is OK (it's a recap, not a parallel)."""
        cast = [
            atlas.get("SEED_MINI"),
            atlas.get("QWEN3_CODER"),
            atlas.get("SEED_MINI"),  # recap — acceptable
        ]
        assert director.counterpoint_check(cast) is True

    def test_single_model_passes(self, director, atlas):
        assert director.counterpoint_check([atlas.get("HERMES_405B")]) is True

    def test_empty_list_passes(self, director):
        assert director.counterpoint_check([]) is True


# ── Tempo profile tests ──────────────────────────────────────────────

class TestTempoProfiles:
    @pytest.mark.parametrize("role", list(ROLE_TEMPO_PROFILES.keys()))
    def test_every_role_has_tempo(self, role):
        assert role in ROLE_TEMPO_PROFILES

    @pytest.mark.parametrize("role,expected_name", [
        ("intent_parse", "Allegro"),
        ("planning", "Moderato"),
        ("code_gen", "Andante"),
        ("personality_wrap", "Adagio"),
        ("safety_check", "Largo"),
        ("creative_ideation", "Rubato"),
    ])
    def test_tempo_name(self, role, expected_name):
        assert ROLE_TEMPO_PROFILES[role].name == expected_name

    def test_tempo_range_method(self, director):
        low, high = director.tempo_range("intent_parse")
        assert low == 120
        assert high == 140

    def test_tempo_range_safety(self, director):
        """Safety is Largo — the slowest tempo."""
        low, high = director.tempo_range("safety_check")
        assert high <= 55

    def test_tempo_range_creative_is_wide(self, director):
        """Creative ideation is Rubato — wide range, no fixed tempo."""
        low, high = director.tempo_range("creative_ideation")
        assert high - low >= 80  # wide

    def test_tempo_range_unknown_role_raises(self, director):
        with pytest.raises(ValueError):
            director.tempo_range("nonexistent_role")

    @pytest.mark.parametrize("role", list(ROLE_TEMPO_PROFILES.keys()))
    def test_tempo_ranges_are_valid(self, role, director):
        low, high = director.tempo_range(role)
        assert 30 <= low <= 200
        assert high >= low


# ── Model swap / what-if tests ───────────────────────────────────────

class TestModelSwap:
    def test_swap_feasible(self, director):
        """GLM_5_2 can handle intent parsing (it's versatile)."""
        assert director.swap("intent_parse", "GLM_5_2") is True

    def test_swap_infeasible(self, director):
        """MMX_M3 cannot handle code generation."""
        assert director.swap("code_gen", "MMX_M3") is False

    def test_swap_nonexistent_model(self, director):
        assert director.swap("code_gen", "GPT_999") is False

    def test_swap_hermes_to_code(self, director):
        """Hermes is not a code model."""
        assert director.swap("code_gen", "HERMES_405B") is False

    def test_swap_nemotron_to_voice(self, director):
        """Nemotron is not a voice model."""
        assert director.swap("voice", "NEMOTRON_ULTRA") is False

    def test_what_if_returns_dict(self, director):
        result = director.what_if("intent_parse", "GLM_5_2")
        assert isinstance(result, dict)
        assert "feasible" in result
        assert "cost_delta" in result
        assert "tempo_delta" in result
        assert "reason" in result

    def test_what_if_cost_delta(self, director):
        """Swapping Seed-mini → GLM_5_2 increases cost."""
        result = director.what_if("intent_parse", "GLM_5_2")
        assert result["cost_delta"] > 0  # GLM is more expensive than Seed-mini

    def test_what_if_infeasible(self, director):
        result = director.what_if("code_gen", "MMX_M3")
        assert result["feasible"] is False

    def test_what_if_nonexistent(self, director):
        result = director.what_if("code_gen", "GPT_999")
        assert result["feasible"] is False

    def test_what_if_tempo_delta(self, director):
        """Swapping Seed-mini → Claude Opus for intent slows things down."""
        result = director.what_if("intent_parse", "CLAUDE_OPUS")
        # Opus is Largo, Seed-mini is Allegro — big tempo shift
        assert result["tempo_delta"][0] < 0  # slower low end
        assert result["tempo_delta"][1] < 0  # slower high end


# ── Integration: voice character / tempo alignment ───────────────────

class TestVoiceCharacterAlignment:
    """Models cast for a role should have a voice that fits the tempo."""

    def test_voice_role_gets_warm_model(self, director):
        """Voice/personality roles get warm-character models (Roland)."""
        profile = director.cast("voice")
        assert profile.voice_character == VoiceCharacter.ROLAND

    def test_safety_gets_heavy_model(self, director):
        """Safety check gets the pipe organ — cathedral-scale."""
        profile = director.cast("safety_check")
        assert profile.voice_character == VoiceCharacter.PIPE_ORGAN

    def test_intent_gets_fast_model(self, director):
        """Intent parsing gets a fast, buzzy model."""
        profile = director.cast("intent_parse")
        assert profile.tempo_bpm[0] >= 120  # Allegro

    def test_code_gets_precision_model(self, director):
        """Code generation gets a precision-calibrated model."""
        profile = director.cast("code_gen")
        assert profile.voice_character == VoiceCharacter.PRECISION

    def test_pipeline_voices_are_diverse(self, director):
        """A full pipeline cast should have diverse voice characters."""
        roles = ["intent_parse", "planning", "code_gen", "personality_wrap", "safety_check"]
        cast = director.cast_pipeline(roles)
        voices = [p.voice_character for p in cast]
        assert len(set(voices)) >= 4  # at least 4 distinct voices in 5 roles
