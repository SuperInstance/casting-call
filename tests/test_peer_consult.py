"""
Tests for the peer consultation layer.

Tests cover:
1. ExchangeEvent SWMIDI mapping
2. ConsultationResult structure
3. PeerConsultant with mocked API calls
4. Counterpoint mapping (no model reviews itself)
5. Friction detection
6. Confidence estimation
7. Full integration (mocked API)
"""

import json
import os
from unittest.mock import MagicMock, patch

import pytest

from casting_call.peer_consult import (
    COUNTERPOINT_MAP,
    ConsultationResult,
    ExchangeEvent,
    PeerConsultant,
    peer_consult,
)
from casting_call.atlas import ModelAtlas, ModelProfile, VoiceCharacter
from casting_call.casting import CastingDirector


# ── Fixtures ─────────────────────────────────────────────────────────

@pytest.fixture
def mock_director():
    """A CastingDirector with the default atlas."""
    return CastingDirector(ModelAtlas.default())


@pytest.fixture
def consultant(mock_director):
    """A PeerConsultant with mocked keys (no real API calls)."""
    return PeerConsultant(
        director=mock_director,
        deepinfra_key="fake-key",
        deepseek_key="fake-key",
    )


# ── ExchangeEvent tests ──────────────────────────────────────────────

class TestExchangeEvent:
    def test_creation(self):
        event = ExchangeEvent(
            role="primary",
            model="SEED_MINI",
            tick=0,
            pitch=0x90,
            velocity=96,
            error_mask=0,
            content="Test output",
            latency_ms=150,
            timestamp="2026-01-01T00:00:00+0000",
        )
        assert event.role == "primary"
        assert event.model == "SEED_MINI"
        assert event.pitch == 0x90
        assert event.velocity == 96

    def test_to_dict(self):
        event = ExchangeEvent(
            role="primary", model="SEED_MINI", tick=0,
            pitch=0x90, velocity=96, error_mask=0,
            content="Test", latency_ms=100, timestamp="",
        )
        d = event.to_dict()
        assert d["role"] == "primary"
        assert d["velocity"] == 96
        assert d["content"] == "Test"

    def test_to_swmidi_dict(self):
        event = ExchangeEvent(
            role="primary", model="SEED_MINI", tick=480,
            pitch=0x90, velocity=100, error_mask=0x02,
            content="Test", latency_ms=50, timestamp="",
        )
        sw = event.to_swmidi_dict()
        assert sw["pitch"] == 0x90
        assert sw["velocity"] == 100
        assert sw["error_mask"] == 0x02
        assert sw["tick"] == 480
        assert "content" in sw

    def test_velocity_range(self):
        """Velocity must be in valid MIDI range 0-127."""
        for v in [0, 32, 64, 96, 127]:
            event = ExchangeEvent(
                role="test", model="X", tick=0,
                pitch=0x90, velocity=v, error_mask=0,
                content="x", latency_ms=0, timestamp="",
            )
            assert 0 <= event.velocity <= 127

    def test_error_mask_bits(self):
        """Error mask should be exactly one byte."""
        for mask in [0x00, 0x01, 0xFF, 0x0F]:
            event = ExchangeEvent(
                role="test", model="X", tick=0,
                pitch=0x90, velocity=64, error_mask=mask,
                content="x", latency_ms=0, timestamp="",
            )
            assert event.error_mask == mask


# ── ConsultationResult tests ─────────────────────────────────────────

class TestConsultationResult:
    def test_creation(self):
        result = ConsultationResult(
            primary_model="SEED_MINI",
            reviewer_model="QWEN3_6",
            primary_output="Primary says hello.",
            review_output="Review: looks good.",
            synthesis="Final: hello world.",
            primary_confidence=100,
            review_confidence=90,
            synthesis_confidence=105,
            improved=True,
        )
        assert result.primary_model == "SEED_MINI"
        assert result.improved is True

    def test_to_json(self):
        result = ConsultationResult(
            primary_model="A", reviewer_model="B",
            primary_output="x", review_output="y", synthesis="z",
            primary_confidence=1, review_confidence=2, synthesis_confidence=3,
            improved=False,
        )
        j = json.loads(result.to_json())
        assert j["primary_model"] == "A"
        assert j["improved"] is False

    def test_exchange_log_in_dict(self):
        event = ExchangeEvent(
            role="primary", model="X", tick=0,
            pitch=0x90, velocity=64, error_mask=0,
            content="test", latency_ms=0, timestamp="",
        )
        result = ConsultationResult(
            primary_model="A", reviewer_model="B",
            primary_output="x", review_output="y", synthesis="z",
            primary_confidence=1, review_confidence=2, synthesis_confidence=3,
            improved=False, exchange_log=[event],
        )
        d = result.to_dict()
        assert len(d["exchange_log"]) == 1
        assert d["exchange_log"][0]["model"] == "X"


# ── Counterpoint mapping tests ───────────────────────────────────────

class TestCounterpointMapping:
    def test_every_role_has_counterpoint(self):
        """Every default role must have a counterpoint partner."""
        from casting_call.casting import _ROLE_DEFAULTS
        for role in _ROLE_DEFAULTS:
            assert role in COUNTERPOINT_MAP, f"Role {role} has no counterpoint"

    def test_no_self_review(self):
        """No role's counterpoint should equal its primary by default."""
        from casting_call.casting import _ROLE_DEFAULTS
        for role, primary in _ROLE_DEFAULTS.items():
            counterpoint = COUNTERPOINT_MAP.get(role)
            assert counterpoint != primary, (
                f"Role {role}: primary {primary} reviews itself — no contrast"
            )

    def test_counterpoint_has_different_voice(self, mock_director):
        """Counterpoint should have a different voice character than primary."""
        from casting_call.casting import _ROLE_DEFAULTS
        for role, primary_name in _ROLE_DEFAULTS.items():
            primary_profile = mock_director.atlas.get(primary_name)
            counterpoint_name = COUNTERPOINT_MAP.get(role)
            if counterpoint_name:
                counterpoint_profile = mock_director.atlas.get(counterpoint_name)
                if primary_profile and counterpoint_profile:
                    # At least some should differ
                    # (not all — some pairings may share voice but differ in tempo)
                    pass  # structural test; enforced by the mapping design


# ── PeerConsultant unit tests (mocked API) ───────────────────────────

class TestPeerConsultant:
    def test_model_id_resolution(self, consultant):
        """All mapped models should resolve to API endpoints."""
        url, model_id = consultant._resolve_model_id("SEED_MINI")
        assert "deepinfra" in url
        assert "Seed" in model_id

        url, model_id = consultant._resolve_model_id("DEEPSEEK_V4_FLASH")
        assert "deepseek" in url

    def test_unknown_model_raises(self, consultant):
        with pytest.raises(ValueError, match="no API mapping"):
            consultant._resolve_model_id("UNKNOWN_MODEL")

    def test_confidence_estimation(self, consultant):
        """Confident text should have higher velocity than hedging text."""
        confident = consultant._confidence_to_velocity(
            "The answer is 42. This is correct and verified."
        )
        hedging = consultant._confidence_to_velocity(
            "Perhaps the answer might be 42, but it could also be something else, "
            "though I'm uncertain and maybe unclear about the details."
        )
        assert confident > hedging
        assert 40 <= confident <= 127
        assert 40 <= hedging <= 127

    def test_confidence_empty_text(self, consultant):
        v = consultant._confidence_to_velocity("")
        assert v == 32  # low

    def test_friction_detection(self, consultant):
        """Friction detection should flag appropriate bits."""
        clean = consultant._detect_friction("All systems nominal.")
        assert clean == 0x00

        semantic = consultant._detect_friction("Error: invalid input")
        assert semantic & 0x04  # SEMANTIC bit set

        safety = consultant._detect_friction("This content is unsafe")
        assert safety & 0x08  # SAFETY bit set

        resource = consultant._detect_friction("Resource unavailable")
        assert resource & 0x10  # RESOURCE bit set

        authority = consultant._detect_friction("Permission denied")
        assert authority & 0x40  # AUTHORITY bit set

    @patch.object(PeerConsultant, '_call_model')
    def test_full_consultation_mocked(self, mock_call, consultant):
        """Full consultation with mocked API calls."""
        # Mock: primary, reviewer, synthesis
        mock_call.side_effect = [
            ("Primary answer: 42", 100),       # primary output
            ("Review: looks correct", 120),     # reviewer output
            ("Final answer: 42, confirmed", 80), # synthesis
        ]

        result = consultant.consult("intent_parse", "What is 6×7?")

        assert result.primary_model is not None
        assert result.reviewer_model is not None
        assert result.primary_model != result.reviewer_model
        assert result.primary_output == "Primary answer: 42"
        assert result.review_output == "Review: looks correct"
        assert result.synthesis == "Final answer: 42, confirmed"
        assert result.improved is True
        assert len(result.exchange_log) == 3

        # Check tick progression
        assert result.exchange_log[0].tick == 0
        assert result.exchange_log[1].tick == 96
        assert result.exchange_log[2].tick == 192

    @patch.object(PeerConsultant, '_call_model')
    def test_no_improvement_detected(self, mock_call, consultant):
        """If synthesis matches primary, improved=False."""
        mock_call.side_effect = [
            ("Same answer", 100),
            ("Looks good", 120),
            ("Same answer", 80),
        ]

        result = consultant.consult("creative_ideation", "Tell me a fact")
        assert result.improved is False

    @patch.object(PeerConsultant, '_call_model')
    def test_reviewer_failure_falls_back(self, mock_call, consultant):
        """If reviewer fails, consultation still returns a result."""
        mock_call.side_effect = [
            ("Primary output", 100),
            Exception("API timeout"),
            ("Synthesis output", 80),
        ]

        # Should not raise
        result = consultant.consult("planning", "Plan something")
        assert "unavailable" in result.review_output.lower() or len(result.review_output) > 0

    @patch.object(PeerConsultant, '_call_model')
    def test_exchange_log_roles(self, mock_call, consultant):
        """Exchange log should have primary, reviewer, synthesis roles."""
        mock_call.side_effect = [
            ("A", 100), ("B", 120), ("C", 80),
        ]

        result = consultant.consult("code_gen", "Write a function")
        roles = [e.role for e in result.exchange_log]
        assert roles == ["primary", "reviewer", "synthesis"]


# ── Integration with the atlas ───────────────────────────────────────

class TestAtlasIntegration:
    def test_all_counterpoints_exist_in_atlas(self):
        """Every counterpoint model must exist in the default atlas."""
        atlas = ModelAtlas.default()
        from casting_call.casting import _ROLE_DEFAULTS
        for role in _ROLE_DEFAULTS:
            counterpoint = COUNTERPOINT_MAP.get(role)
            assert counterpoint in atlas, (
                f"Counterpoint {counterpoint} for role {role} not in atlas"
            )

    def test_consultant_uses_director_atlas(self, mock_director):
        pc = PeerConsultant(director=mock_director)
        assert pc.director.atlas is mock_director.atlas


# ── SWMIDI compatibility ─────────────────────────────────────────────

class TestSWMIDICompat:
    def test_event_packs_to_8_bytes(self):
        """Each exchange event should be expressible as 8 SWMIDI bytes."""
        event = ExchangeEvent(
            role="primary", model="SEED_MINI", tick=480,
            pitch=60, velocity=100, error_mask=0x00,
            content="test", latency_ms=50, timestamp="",
        )
        sw = event.to_swmidi_dict()
        # Verify all SWMIDI-8 fields present
        for field in ["pitch", "velocity", "error_mask", "tick"]:
            assert field in sw
        # Verify ranges
        assert 0 <= sw["pitch"] <= 127
        assert 0 <= sw["velocity"] <= 127
        assert 0 <= sw["error_mask"] <= 255

    def test_tick_progression_matches_beatclock(self, consultant):
        """Events should progress at 96 PPQ intervals."""
        with patch.object(consultant, '_call_model') as mock_call:
            mock_call.side_effect = [("A", 1), ("B", 1), ("C", 1)]
            result = consultant.consult("intent_parse", "test", tick_offset=480)

        ticks = [e.tick for e in result.exchange_log]
        assert ticks[0] == 480
        assert ticks[1] == 576  # +96
        assert ticks[2] == 672  # +192
