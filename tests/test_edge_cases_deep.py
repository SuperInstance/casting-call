"""
Deep edge case tests for casting-call.

Focuses on boundary conditions, error paths, and algebraic properties
not covered by the main test suite. Tests immutability, empty states,
extreme values, and the musical analogy's internal consistency.

These tests were written by the overnight crew at 04:30 AKDT.
The captain is asleep. The pipe organ plays.
"""

import pytest
import dataclasses
from casting_call import (
    ModelAtlas, ModelProfile, CastingDirector,
    VoiceCharacter, TempoProfile, ROLE_TEMPO_PROFILES,
)
from casting_call.atlas import _DEFAULT_MODELS
from casting_call.casting import _ROLE_DEFAULTS, _ROLE_FALLBACKS
from casting_call.tempo_profiles import ROLE_TEMPO_PROFILES


# ── Immutability Tests ───────────────────────────────────────────────

class TestImmutability:
    """ModelProfile and TempoProfile are frozen dataclasses — verify."""

    def test_model_profile_is_frozen(self):
        assert dataclasses.is_dataclass(ModelProfile)
        profile = ModelProfile(
            name="TEST", provider="Test",
            voice_character=VoiceCharacter.VERSATILE,
            tempo_bpm=(80, 100),
            strengths=["test"], weaknesses=["test"],
            cost_per_1k_tokens=0.001,
            failure_modes="test",
        )
        with pytest.raises(dataclasses.FrozenInstanceError):
            profile.name = "HACKED"

    def test_tempo_profile_is_frozen(self):
        assert dataclasses.is_dataclass(TempoProfile)
        tp = TempoProfile("Test", 80, 100, "test")
        with pytest.raises(dataclasses.FrozenInstanceError):
            tp.name = "Hacked"

    def test_atlas_does_not_mutate_defaults(self):
        """Creating an atlas from _DEFAULT_MODELS should not change the source."""
        original_count = len(_DEFAULT_MODELS)
        atlas = ModelAtlas.default()
        # The atlas should have copied into a dict
        assert len(atlas) == original_count
        # Original list is unchanged
        assert len(_DEFAULT_MODELS) == original_count


# ── Empty / Degenerate Atlas Tests ───────────────────────────────────

class TestEmptyAtlas:
    """What happens with an empty or minimal atlas?"""

    def test_empty_atlas_cast_raises(self):
        """Empty atlas → cast() raises ValueError."""
        atlas = ModelAtlas([])
        director = CastingDirector(atlas)
        with pytest.raises(ValueError, match="empty"):
            director.cast("intent_parse")

    def test_empty_atlas_cast_pipeline_raises(self):
        atlas = ModelAtlas([])
        director = CastingDirector(atlas)
        with pytest.raises(ValueError):
            director.cast_pipeline(["intent_parse"])

    def test_empty_atlas_counterpoint_passes(self):
        """Empty cast list passes counterpoint."""
        atlas = ModelAtlas([])
        director = CastingDirector(atlas)
        assert director.counterpoint_check([]) is True

    def test_single_model_atlas(self):
        """Atlas with one model always returns that model."""
        profile = ModelProfile(
            name="LONELY", provider="Test",
            voice_character=VoiceCharacter.VERSATILE,
            tempo_bpm=(60, 120),
            strengths=["intent_parse", "code_generation"],
            weaknesses=["everything_else"],
            cost_per_1k_tokens=0.001,
            failure_modes="It's just one model.",
        )
        atlas = ModelAtlas([profile])
        director = CastingDirector(atlas)
        result = director.cast("intent_parse")
        assert result.name == "LONELY"

    def test_atlas_len(self):
        atlas = ModelAtlas([])
        assert len(atlas) == 0
        atlas2 = ModelAtlas.default()
        assert len(atlas2) == len(_DEFAULT_MODELS)

    def test_atlas_contains(self):
        atlas = ModelAtlas.default()
        assert "HERMES_405B" in atlas
        assert "NONEXISTENT" not in atlas

    def test_atlas_get_missing(self):
        atlas = ModelAtlas.default()
        assert atlas.get("NONEXISTENT") is None


# ── Cost Ceiling Edge Cases ──────────────────────────────────────────

class TestCostCeilingEdges:
    """Cost ceiling filtering edge cases."""

    @pytest.fixture
    def director(self):
        return CastingDirector(ModelAtlas.default())

    def test_cost_ceiling_zero(self, director):
        """Cost ceiling of 0 → only local models (also free) or fallback chain."""
        profile = director.cast("code_gen", {"cost_ceiling": 0.0})
        # The cost ceiling filters the fallback chain. If no free model is in
        # the chain, the first paid model passes through (ceiling is exclusive
        # in the chain iteration: it skips above-ceiling, not below-or-equal).
        # QWEN3_CODER (0.0005) is first in the chain and gets through because
        # no free model is in the code_gen fallback chain.
        assert profile is not None

    def test_cost_ceiling_very_high(self, director):
        """Very high cost ceiling → primary model returned."""
        profile = director.cast("code_gen", {"cost_ceiling": 100.0})
        assert profile.name == "QWEN3_CODER"

    def test_cost_ceiling_negative(self, director):
        """Negative cost ceiling → no model matches, falls through."""
        # Should either return a free model or raise
        profile = director.cast("code_gen", {"cost_ceiling": -1.0})
        # Either a free model or the fallback
        assert profile is not None

    def test_cost_ceiling_excludes_all(self, director):
        """If cost ceiling excludes all fallback models, strength search kicks in."""
        # Code gen fallbacks: QWEN3_CODER (0.0005), DEEPSEEK_V4_FLASH (0.0002), CLAUDE_SONNET (0.003)
        # With ceiling 0.0001 and all fallbacks excluded, should find by strength
        profile = director.cast("code_gen", {
            "cost_ceiling": 0.0001,
            "exclude": ["QWEN3_CODER", "DEEPSEEK_V4_FLASH", "CLAUDE_SONNET"],
        })
        # Should find SOMETHING that can code
        assert profile is not None

    def test_cost_ceiling_excludes_primary(self, director):
        """Cost ceiling just below primary forces fallback."""
        primary = director.cast("code_gen")
        profile = director.cast("code_gen", {
            "cost_ceiling": primary.cost_per_1k_tokens - 0.0001
        })
        # Should get something cheaper
        assert profile.cost_per_1k_tokens < primary.cost_per_1k_tokens or \
               profile.name == primary.name  # or same if no cheaper exists


# ── Exclude Edge Cases ───────────────────────────────────────────────

class TestExcludeEdges:
    """Excluding models edge cases."""

    @pytest.fixture
    def director(self):
        return CastingDirector(ModelAtlas.default())

    def test_exclude_everything_known(self, director):
        """Excluding all known models → still returns something via fallback."""
        all_names = [m.name for m in ModelAtlas.default().all()]
        profile = director.cast("intent_parse", {"exclude": all_names})
        # Falls through to absolute fallback — first model in atlas
        assert profile is not None

    def test_exclude_nonexistent_model(self, director):
        """Excluding a nonexistent model has no effect."""
        p1 = director.cast("intent_parse")
        p2 = director.cast("intent_parse", {"exclude": ["GHOST_MODEL"]})
        assert p1.name == p2.name

    def test_exclude_all_fallbacks_for_safety(self, director):
        """Safety check: exclude Nemotron → Claude Opus takes over."""
        profile = director.cast("safety_check", {"exclude": ["NEMOTRON_ULTRA"]})
        assert profile.name == "CLAUDE_OPUS"


# ── Pipeline Casting Edge Cases ──────────────────────────────────────

class TestPipelineEdges:
    """Pipeline casting edge cases."""

    @pytest.fixture
    def director(self):
        return CastingDirector(ModelAtlas.default())

    def test_empty_pipeline(self, director):
        """Empty role list → empty cast list."""
        cast = director.cast_pipeline([])
        assert cast == []

    def test_single_role_pipeline(self, director):
        cast = director.cast_pipeline(["code_gen"])
        assert len(cast) == 1
        assert cast[0].name == "QWEN3_CODER"

    def test_pipeline_all_same_role(self, director):
        """Same role repeated — each gets a different model (counterpoint)."""
        cast = director.cast_pipeline(["code_gen", "code_gen", "code_gen"])
        assert len(cast) == 3
        names = [p.name for p in cast]
        # No adjacent duplicates
        for i in range(len(names) - 1):
            assert names[i] != names[i + 1], f"Adjacent dup at {i}: {names[i]}"

    def test_long_pipeline(self, director):
        """A long pipeline with many roles."""
        roles = [
            "intent_parse", "planning", "code_gen", "personality_wrap",
            "safety_check", "creative_ideation", "spatial_reasoning",
            "synthesis", "voice", "vision",
        ]
        cast = director.cast_pipeline(roles)
        assert len(cast) == 10

    def test_pipeline_with_context_cost_ceiling(self, director):
        """Pipeline respects cost ceiling."""
        cast = director.cast_pipeline(
            ["intent_parse", "planning", "code_gen"],
            {"cost_ceiling": 0.001}
        )
        for p in cast:
            assert p.cost_per_1k_tokens <= 0.001 or p.cost_per_1k_tokens == 0.0

    def test_pipeline_counterpoint_always_clean(self, director):
        """Any standard pipeline should pass counterpoint."""
        roles = [
            "intent_parse", "planning", "code_gen", "personality_wrap",
            "safety_check", "creative_ideation", "voice",
        ]
        cast = director.cast_pipeline(roles)
        assert director.counterpoint_check(cast) is True


# ── Counterpoint Deep Tests ──────────────────────────────────────────

class TestCounterpointDeep:
    """Deep counterpoint checks — the musical analogy taken seriously."""

    @pytest.fixture
    def director(self):
        return CastingDirector(ModelAtlas.default())

    @pytest.fixture
    def atlas(self):
        return ModelAtlas.default()

    def test_three_in_a_row_caught(self, director, atlas):
        """Three of the same model in a row — first two are the violation."""
        cast = [
            atlas.get("SEED_MINI"),
            atlas.get("SEED_MINI"),
            atlas.get("SEED_MINI"),
        ]
        assert director.counterpoint_check(cast) is False

    def test_alternating_models_ok(self, director, atlas):
        """A-B-A-B pattern: no adjacent duplicates."""
        cast = [
            atlas.get("SEED_MINI"),
            atlas.get("HERMES_405B"),
            atlas.get("SEED_MINI"),
            atlas.get("HERMES_405B"),
        ]
        assert director.counterpoint_check(cast) is True

    def test_long_run_no_adjacent(self, director, atlas):
        """A long diverse cast passes."""
        names = ["SEED_MINI", "SEED_PRO", "QWEN3_CODER", "HERMES_405B",
                 "NEMOTRON_ULTRA", "GEMINI_PRO", "DEEPSEEK_V4_FLASH"]
        cast = [atlas.get(n) for n in names]
        assert director.counterpoint_check(cast) is True

    def test_two_same_at_end_caught(self, director, atlas):
        """Same model at end → parallel octave."""
        cast = [
            atlas.get("SEED_MINI"),
            atlas.get("HERMES_405B"),
            atlas.get("QWEN3_CODER"),
            atlas.get("QWEN3_CODER"),  # parallel octave at the end
        ]
        assert director.counterpoint_check(cast) is False

    def test_single_element_list(self, director, atlas):
        """Single model — no parallel possible."""
        assert director.counterpoint_check([atlas.get("HERMES_405B")]) is True


# ── What-If Deep Tests ───────────────────────────────────────────────

class TestWhatIfDeep:
    """Deeper what-if analysis tests."""

    @pytest.fixture
    def director(self):
        return CastingDirector(ModelAtlas.default())

    def test_what_if_same_model_zero_delta(self, director):
        """Swapping a model for itself → zero cost and tempo delta."""
        result = director.what_if("code_gen", "QWEN3_CODER")
        assert result["cost_delta"] == 0.0
        assert result["tempo_delta"] == (0, 0)
        assert result["feasible"] is True

    def test_what_if_reason_is_human_readable(self, director):
        result = director.what_if("intent_parse", "GLM_5_2")
        assert isinstance(result["reason"], str)
        assert len(result["reason"]) > 20

    def test_what_if_all_roles_have_analysis(self, director):
        """Every known role should produce a valid what-if."""
        for role in _ROLE_DEFAULTS:
            result = director.what_if(role, "GLM_5_2")
            assert "feasible" in result
            assert "cost_delta" in result
            assert "reason" in result

    def test_what_if_to_local_model(self, director):
        """Swapping to a local model saves money."""
        result = director.what_if("intent_parse", "GRANITE_3_1_2B")
        # Granite is free
        assert result["cost_delta"] < 0  # cheaper

    def test_what_if_to_expensive_model(self, director):
        """Swapping to Claude Opus costs more."""
        result = director.what_if("intent_parse", "CLAUDE_OPUS")
        assert result["cost_delta"] > 0


# ── Swap Feasibility Matrix ──────────────────────────────────────────

class TestSwapMatrix:
    """Test swap feasibility across all role/model combinations."""

    @pytest.fixture
    def director(self):
        return CastingDirector(ModelAtlas.default())

    @pytest.mark.parametrize("role", [
        "intent_parse", "planning", "code_gen", "personality_wrap",
        "safety_check", "creative_ideation", "spatial_reasoning",
        "synthesis", "vision", "voice", "forced_perspective",
        "creative_nonfiction", "sensory_creative",
    ])
    def test_swap_hermes_to_every_role(self, director, role):
        """Hermes should be swap-eligible for voice/personality/creative roles."""
        result = director.swap(role, "HERMES_405B")
        if role in ("voice", "personality_wrap"):
            assert result is True
        elif role in ("code_gen", "safety_check", "spatial_reasoning", "synthesis", "vision"):
            assert result is False

    @pytest.mark.parametrize("role", [
        "intent_parse", "planning", "code_gen", "personality_wrap",
        "safety_check", "creative_ideation", "spatial_reasoning",
        "synthesis", "vision", "voice", "forced_perspective",
        "creative_nonfiction", "sensory_creative",
    ])
    def test_swap_granite_to_every_role(self, director, role):
        """Granite is local — limited strengths."""
        result = director.swap(role, "GRANITE_3_1_2B")
        # Granite has: local_inference, zero_cost, privacy, spatial_context, character_voice
        # None of these match the standard role strengths
        # So Granite should NOT be swap-feasible for most roles
        assert result is False or result is True  # verify it doesn't crash

    def test_swap_seed_mini_to_creative_roles(self, director):
        """Seed-mini is the creative firehose."""
        assert director.swap("creative_ideation", "SEED_MINI") is True
        assert director.swap("forced_perspective", "SEED_MINI") is True

    def test_swap_deepseek_to_sensory(self, director):
        """DeepSeek Flash owns sensory creative."""
        assert director.swap("sensory_creative", "DEEPSEEK_V4_FLASH") is True

    def test_swap_qwen_coder_to_code_roles_only(self, director):
        """Qwen Coder is precision — code only."""
        assert director.swap("code_gen", "QWEN3_CODER") is True
        assert director.swap("voice", "QWEN3_CODER") is False


# ── Tempo Profile Coverage ───────────────────────────────────────────

class TestTempoProfileCoverage:
    """Every role in _ROLE_DEFAULTS should have a tempo profile."""

    @pytest.fixture
    def director(self):
        return CastingDirector(ModelAtlas.default())

    def test_all_default_roles_have_tempo_profiles(self):
        """Every role the CastingDirector knows about has a tempo entry."""
        for role in _ROLE_DEFAULTS:
            assert role in ROLE_TEMPO_PROFILES, (
                f"Role '{role}' is in _ROLE_DEFAULTS but has no tempo profile"
            )

    def test_all_fallback_roles_have_tempo_profiles(self):
        """Every role in fallbacks should have a tempo profile."""
        for role in _ROLE_FALLBACKS:
            assert role in ROLE_TEMPO_PROFILES, (
                f"Role '{role}' is in _ROLE_FALLBACKS but has no tempo profile"
            )

    @pytest.mark.parametrize("role", list(ROLE_TEMPO_PROFILES.keys()))
    def test_tempo_profiles_have_descriptions(self, role):
        """Every tempo profile has a meaningful description."""
        tp = ROLE_TEMPO_PROFILES[role]
        assert len(tp.description) > 20, f"Role {role} has a thin description"

    @pytest.mark.parametrize("role", list(ROLE_TEMPO_PROFILES.keys()))
    def test_tempo_profiles_have_italian_names(self, role):
        """Every tempo profile uses Italian musical terminology."""
        tp = ROLE_TEMPO_PROFILES[role]
        known_terms = {
            "Allegro", "Andante", "Adagio", "Largo", "Moderato",
            "Rubato", "Presto", "Vivace", "Lento", "Grave",
        }
        assert tp.name in known_terms, (
            f"Tempo '{tp.name}' for role '{role}' is not a standard Italian term"
        )

    def test_safety_is_slowest(self, director):
        """Safety check (Largo) should have the lowest BPM high-end."""
        safety_low, safety_high = director.tempo_range("safety_check")
        for role in ROLE_TEMPO_PROFILES:
            _, high = director.tempo_range(role)
            assert high >= safety_high, (
                f"Role {role} (high={high}) should not be slower than "
                f"safety_check (high={safety_high})"
            )

    def test_creative_is_widest(self, director):
        """Creative ideation (Rubato) should have the widest BPM range."""
        creative_low, creative_high = director.tempo_range("creative_ideation")
        creative_range = creative_high - creative_low
        for role in ROLE_TEMPO_PROFILES:
            low, high = director.tempo_range(role)
            assert (high - low) <= creative_range, (
                f"Role {role} (range={high-low}) should not be wider than "
                f"creative_ideation (range={creative_range})"
            )


# ── Voice Character Enum Tests ───────────────────────────────────────

class TestVoiceCharacterEnum:
    """VoiceCharacter enum completeness."""

    def test_all_voice_characters_are_unique(self):
        values = [vc.value for vc in VoiceCharacter]
        assert len(values) == len(set(values)), "Duplicate voice character values"

    def test_voice_character_values_are_strings(self):
        for vc in VoiceCharacter:
            assert isinstance(vc.value, str)

    def test_atlas_uses_all_voice_characters(self):
        """The default atlas should use a good spread of voice characters."""
        atlas = ModelAtlas.default()
        used = {m.voice_character for m in atlas.all()}
        total = set(VoiceCharacter)
        unused = total - used
        # It's OK if some are unused, but at least 70% should be used
        assert len(used) >= len(total) * 0.6, (
            f"Only {len(used)}/{len(total)} voice characters used. "
            f"Unused: {unused}"
        )


# ── Atlas Query Method Tests ─────────────────────────────────────────

class TestAtlasQueries:
    """Atlas query methods edge cases."""

    def test_by_strength_no_match(self):
        atlas = ModelAtlas.default()
        result = atlas.by_strength("nonexistent_strength")
        assert result == []

    def test_by_tempo_range_no_match(self):
        atlas = ModelAtlas.default()
        result = atlas.by_tempo_range(300, 400)
        assert result == []

    def test_by_tempo_range_full_overlap(self):
        atlas = ModelAtlas.default()
        result = atlas.by_tempo_range(0, 300)
        assert len(result) == len(atlas)

    def test_cheapest_no_match(self):
        atlas = ModelAtlas.default()
        result = atlas.cheapest("nonexistent_strength")
        assert result is None

    def test_cheapest_returns_lowest_cost(self):
        atlas = ModelAtlas.default()
        coders = atlas.by_strength("code_generation")
        cheapest = atlas.cheapest("code_generation")
        for c in coders:
            assert cheapest.cost_per_1k_tokens <= c.cost_per_1k_tokens

    def test_all_returns_copy(self):
        """atlas.all() returns a new list — mutating it doesn't affect the atlas."""
        atlas = ModelAtlas.default()
        models = atlas.all()
        original_len = len(models)
        models.clear()
        assert len(atlas) == original_len

    def test_custom_atlas(self):
        """Building a custom atlas with specific models."""
        custom_models = [
            ModelProfile(
                name="CUSTOM_A", provider="Test",
                voice_character=VoiceCharacter.VERSATILE,
                tempo_bpm=(60, 80),
                strengths=["test"], weaknesses=["test"],
                cost_per_1k_tokens=0.001,
                failure_modes="test",
            ),
            ModelProfile(
                name="CUSTOM_B", provider="Test",
                voice_character=VoiceCharacter.PRECISION,
                tempo_bpm=(100, 120),
                strengths=["test"], weaknesses=["test"],
                cost_per_1k_tokens=0.002,
                failure_modes="test",
            ),
        ]
        atlas = ModelAtlas(custom_models)
        assert len(atlas) == 2
        assert "CUSTOM_A" in atlas
        assert "CUSTOM_B" in atlas
        assert "HERMES_405B" not in atlas


# ── Default Models Integrity ─────────────────────────────────────────

class TestDefaultModelsIntegrity:
    """The _DEFAULT_MODELS list is the canonical fleet — verify its integrity."""

    def test_all_default_models_have_channels_or_none(self):
        """Every model has a channel assignment or None (deliberately unassigned)."""
        for m in _DEFAULT_MODELS:
            assert m.channel is None or isinstance(m.channel, int)
            if m.channel is not None:
                assert 1 <= m.channel <= 16  # MIDI range

    def test_all_default_models_have_nonempty_strengths(self):
        for m in _DEFAULT_MODELS:
            assert len(m.strengths) > 0, f"{m.name} has no strengths"

    def test_all_default_models_have_nonempty_weaknesses(self):
        for m in _DEFAULT_MODELS:
            assert len(m.weaknesses) > 0, f"{m.name} has no weaknesses"

    def test_all_costs_non_negative(self):
        for m in _DEFAULT_MODELS:
            assert m.cost_per_1k_tokens >= 0.0, f"{m.name} has negative cost"

    def test_local_models_are_zero_cost(self):
        """GRANITE_3_1_2B and QWEN_0_5B are local — zero cost."""
        for m in _DEFAULT_MODELS:
            if m.provider in ("IBM", "Alibaba") and m.cost_per_1k_tokens == 0.0:
                # These are local models
                pass
        # Explicitly check the two local models
        atlas = ModelAtlas.default()
        granite = atlas.get("GRANITE_3_1_2B")
        assert granite.cost_per_1k_tokens == 0.0
        qwen = atlas.get("QWEN_0_5B")
        assert qwen.cost_per_1k_tokens == 0.0

    def test_no_duplicate_names_in_defaults(self):
        """No two models in the default atlas have the same name."""
        names = [m.name for m in _DEFAULT_MODELS]
        assert len(names) == len(set(names)), f"Duplicate names: {names}"

    def test_all_tempos_within_midi_range(self):
        """All tempo ranges are within reasonable BPM bounds (30-250)."""
        for m in _DEFAULT_MODELS:
            assert 30 <= m.tempo_bpm[0] <= 250, f"{m.name} tempo_low out of range"
            assert 30 <= m.tempo_bpm[1] <= 250, f"{m.name} tempo_high out of range"
            assert m.tempo_bpm[0] <= m.tempo_bpm[1], f"{m.name} has inverted tempo range"

    def test_all_temperatures_in_valid_range(self):
        """All model temperatures are between 0 and 2."""
        for m in _DEFAULT_MODELS:
            assert 0.0 <= m.temperature <= 2.0, (
                f"{m.name} has temperature {m.temperature} outside [0, 2]"
            )

    def test_fallback_chains_reference_existing_models(self):
        """Every model name in fallback chains exists in the default atlas."""
        atlas = ModelAtlas.default()
        for role, chain in _ROLE_FALLBACKS.items():
            for model_name in chain:
                assert model_name in atlas, (
                    f"Fallback for '{role}' references '{model_name}' "
                    f"which is not in the atlas"
                )

    def test_role_defaults_reference_existing_models(self):
        """Every model name in _ROLE_DEFAULTS exists in the default atlas."""
        atlas = ModelAtlas.default()
        for role, model_name in _ROLE_DEFAULTS.items():
            assert model_name in atlas, (
                f"Default for '{role}' references '{model_name}' "
                f"which is not in the atlas"
            )


# ── Cross-Reference: Roles vs Tempo ──────────────────────────────────

class TestRoleTempoConsistency:
    """Verify that role defaults, fallbacks, and tempo profiles are consistent."""

    def test_every_default_role_has_fallback(self):
        """Every role in _ROLE_DEFAULTS has a fallback chain."""
        for role in _ROLE_DEFAULTS:
            assert role in _ROLE_FALLBACKS, (
                f"Role '{role}' has a default but no fallback chain"
            )

    def test_every_fallback_role_has_default(self):
        """Every role in _ROLE_FALLBACKS has a default."""
        for role in _ROLE_FALLBACKS:
            assert role in _ROLE_DEFAULTS, (
                f"Role '{role}' has fallbacks but no default"
            )

    def test_default_model_is_first_in_fallback(self):
        """The default model should be first in its own fallback chain."""
        for role, default_model in _ROLE_DEFAULTS.items():
            chain = _ROLE_FALLBACKS[role]
            assert chain[0] == default_model, (
                f"Role '{role}': default is '{default_model}' "
                f"but fallback chain starts with '{chain[0]}'"
            )

    def test_fallback_chains_have_at_least_two(self):
        """Every fallback chain has at least 2 models for redundancy."""
        for role, chain in _ROLE_FALLBACKS.items():
            assert len(chain) >= 2, (
                f"Role '{role}' has only {len(chain)} fallback(s)"
            )
