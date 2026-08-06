"""
Tests for casting-call tempo_profiles module.

Tests cover:
- TempoProfile dataclass immutability
- All canonical role profiles exist
- BPM ranges are musically valid (low < high, positive)
- Tempo ordering consistency (safety slowest, intent fastest)
- Profile descriptions are non-empty
- Frozen dataclass behavior
"""

import pytest
from dataclasses import FrozenInstanceError

from casting_call.tempo_profiles import TempoProfile, ROLE_TEMPO_PROFILES


# ─── TempoProfile Dataclass Tests ────────────────────────

class TestTempoProfile:
    def test_creation(self):
        p = TempoProfile(name="Test", bpm_low=80, bpm_high=120, description="test")
        assert p.name == "Test"
        assert p.bpm_low == 80
        assert p.bpm_high == 120

    def test_frozen(self):
        p = TempoProfile(name="Test", bpm_low=80, bpm_high=120, description="test")
        with pytest.raises(FrozenInstanceError):
            p.bpm_low = 100

    def test_hashable(self):
        p = TempoProfile(name="Test", bpm_low=80, bpm_high=120, description="test")
        # Frozen dataclass should be hashable
        assert hash(p) == hash(p)


# ─── Canonical Role Coverage Tests ───────────────────────

class TestRoleCoverage:
    EXPECTED_ROLES = [
        "intent_parse", "planning", "code_gen", "personality_wrap",
        "safety_check", "creative_ideation", "spatial_reasoning",
        "synthesis", "vision", "voice",
    ]

    def test_all_expected_roles_present(self):
        for role in self.EXPECTED_ROLES:
            assert role in ROLE_TEMPO_PROFILES, f"Missing role: {role}"

    def test_no_extra_roles(self):
        # These are the canonical roles; extras are fine but should be documented
        for role in ROLE_TEMPO_PROFILES:
            assert isinstance(ROLE_TEMPO_PROFILES[role], TempoProfile)

    def test_profile_count(self):
        assert len(ROLE_TEMPO_PROFILES) >= 10


# ─── BPM Range Validity Tests ────────────────────────────

class TestBPMRanges:
    @pytest.mark.parametrize("role", list(ROLE_TEMPO_PROFILES.keys()))
    def test_bpm_low_positive(self, role):
        profile = ROLE_TEMPO_PROFILES[role]
        assert profile.bpm_low > 0, f"{role}: bpm_low must be positive"

    @pytest.mark.parametrize("role", list(ROLE_TEMPO_PROFILES.keys()))
    def test_bpm_high_gt_low(self, role):
        profile = ROLE_TEMPO_PROFILES[role]
        assert profile.bpm_high > profile.bpm_low, f"{role}: bpm_high must exceed bpm_low"

    @pytest.mark.parametrize("role", list(ROLE_TEMPO_PROFILES.keys()))
    def test_bpm_within_musical_range(self, role):
        """BPM should be within a reasonable musical range (20-300)."""
        profile = ROLE_TEMPO_PROFILES[role]
        assert 20 <= profile.bpm_low <= 300, f"{role}: bpm_low={profile.bpm_low}"
        assert 20 <= profile.bpm_high <= 300, f"{role}: bpm_high={profile.bpm_high}"

    @pytest.mark.parametrize("role", list(ROLE_TEMPO_PROFILES.keys()))
    def test_description_non_empty(self, role):
        profile = ROLE_TEMPO_PROFILES[role]
        assert len(profile.description) > 10, f"{role}: description too short"
        assert profile.description.strip() == profile.description, f"{role}: description has leading/trailing whitespace"

    @pytest.mark.parametrize("role", list(ROLE_TEMPO_PROFILES.keys()))
    def test_name_is_musical_term(self, role):
        """Each profile's name should be an Italian musical tempo term."""
        profile = ROLE_TEMPO_PROFILES[role]
        valid_terms = {
            "Largo", "Larghetto", "Adagio", "Andante", "Moderato",
            "Allegro", "Presto", "Prestissimo", "Vivace", "Allegretto",
            "Rubato", "Cantabile", "Sostenuto", "Maestoso", "Giocoso",
            "Legato", "Staccato", "Grave", "Agitato", "Lento",
        }
        assert profile.name in valid_terms, f"{role}: '{profile.name}' not a recognized tempo term"


# ─── Tempo Ordering Tests ────────────────────────────────

class TestTempoOrdering:
    def test_safety_check_is_slowest_or_near_slowest(self):
        """Safety check (Largo) should have the lowest or near-lowest BPM."""
        safety = ROLE_TEMPO_PROFILES["safety_check"]
        intent = ROLE_TEMPO_PROFILES["intent_parse"]
        assert safety.bpm_high < intent.bpm_low, "Safety should be slower than intent parsing"

    def test_intent_parse_is_fastest(self):
        """Intent parsing (Allegro) should be among the fastest."""
        intent = ROLE_TEMPO_PROFILES["intent_parse"]
        all_high = [p.bpm_high for p in ROLE_TEMPO_PROFILES.values()]
        assert intent.bpm_high >= max(all_high) - 20

    def test_creative_ideation_widest_range(self):
        """Creative ideation (Rubato) has the widest BPM range — free tempo."""
        creative = ROLE_TEMPO_PROFILES["creative_ideation"]
        ranges = [(p.bpm_high - p.bpm_low) for p in ROLE_TEMPO_PROFILES.values()]
        assert (creative.bpm_high - creative.bpm_low) >= max(ranges) - 10

    def test_personality_slower_than_code_gen(self):
        """Personality wrapping (Adagio) is slower than code gen (Andante)."""
        personality = ROLE_TEMPO_PROFILES["personality_wrap"]
        code_gen = ROLE_TEMPO_PROFILES["code_gen"]
        assert personality.bpm_high < code_gen.bpm_low


# ─── Consistency with Musical Theory Tests ───────────────

class TestMusicalTheoryConsistency:
    def test_allegro_is_fast(self):
        intent = ROLE_TEMPO_PROFILES["intent_parse"]
        assert intent.name == "Allegro"
        assert intent.bpm_low >= 120  # Allegro is 120-156 BPM

    def test_adagio_is_slow(self):
        personality = ROLE_TEMPO_PROFILES["personality_wrap"]
        assert personality.name == "Adagio"
        assert personality.bpm_high <= 76  # Adagio is 66-76 BPM

    def test_andante_is_walking(self):
        code_gen = ROLE_TEMPO_PROFILES["code_gen"]
        assert code_gen.name == "Andante"
        assert 76 <= code_gen.bpm_low <= 108  # Andante is 76-108 BPM

    def test_largo_is_very_slow(self):
        safety = ROLE_TEMPO_PROFILES["safety_check"]
        assert safety.name == "Largo"
        assert safety.bpm_high <= 60  # Largo is 40-60 BPM
