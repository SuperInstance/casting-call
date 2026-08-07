"""Tests for HarnessNotes — field performance observations for AI agent harnesses.

Tests HarnessProfile dataclass, HARNESS_NOTES registry, lookup functions,
and data integrity across all profiles.
"""

import pytest

from casting_call.harness_notes import (
    HarnessProfile,
    HARNESS_NOTES,
    get_harness,
    all_harnesses,
)


# ─── HarnessProfile dataclass tests ────────────────────────────────

class TestHarnessProfileCreation:
    def test_minimal_creation(self):
        hp = HarnessProfile(
            name="test",
            cli_path="/test",
            best_for=["x"],
            poor_for=["y"],
            notes="test notes",
            session_mgmt="test",
            speed="test",
            reliability="test",
        )
        assert hp.name == "test"
        assert hp.cli_path == "/test"

    def test_frozen(self):
        """HarnessProfile is frozen — immutable."""
        hp = HarnessProfile(
            name="test", cli_path="/t", best_for=[], poor_for=[],
            notes="", session_mgmt="", speed="", reliability="",
        )
        with pytest.raises((AttributeError, Exception)):
            hp.name = "changed"

    def test_field_types(self):
        hp = HARNESS_NOTES[0]
        assert isinstance(hp.name, str)
        assert isinstance(hp.cli_path, str)
        assert isinstance(hp.best_for, list)
        assert isinstance(hp.poor_for, list)
        assert isinstance(hp.notes, str)
        assert isinstance(hp.session_mgmt, str)
        assert isinstance(hp.speed, str)
        assert isinstance(hp.reliability, str)


# ─── HARNESS_NOTES registry tests ──────────────────────────────────

class TestHarnessRegistry:
    def test_registry_not_empty(self):
        assert len(HARNESS_NOTES) > 0

    def test_all_have_names(self):
        for h in HARNESS_NOTES:
            assert h.name, f"Harness with empty name: {h}"

    def test_names_are_unique(self):
        names = [h.name for h in HARNESS_NOTES]
        assert len(names) == len(set(names)), f"Duplicate names: {names}"

    def test_all_have_cli_paths(self):
        for h in HARNESS_NOTES:
            assert h.cli_path, f"{h.name}: empty cli_path"

    def test_all_have_best_for(self):
        for h in HARNESS_NOTES:
            assert len(h.best_for) > 0, f"{h.name}: empty best_for"

    def test_all_have_poor_for(self):
        for h in HARNESS_NOTES:
            assert len(h.poor_for) > 0, f"{h.name}: empty poor_for"

    def test_all_have_notes(self):
        for h in HARNESS_NOTES:
            assert len(h.notes) > 10, f"{h.name}: notes too short"

    def test_all_have_session_mgmt(self):
        for h in HARNESS_NOTES:
            assert h.session_mgmt, f"{h.name}: empty session_mgmt"

    def test_all_have_speed(self):
        for h in HARNESS_NOTES:
            assert h.speed, f"{h.name}: empty speed"

    def test_all_have_reliability(self):
        for h in HARNESS_NOTES:
            assert h.reliability, f"{h.name}: empty reliability"

    def test_known_harnesses_present(self):
        """All expected harnesses should be in the registry."""
        names = {h.name for h in HARNESS_NOTES}
        expected = {"KimiCode", "Claude Code (Fable)", "OpenCode", "MMX (MiniMax)",
                    "Ollama (Local GPU)", "DeepInfra MCP", "DeepSeek API",
                    "GLM Subagents (Z.ai Max)"}
        missing = expected - names
        assert not missing, f"Missing harnesses: {missing}"


class TestHarnessContent:
    def test_kimicode_spatial(self):
        h = get_harness("KimiCode")
        assert h is not None
        assert "spatial_reasoning" in h.best_for

    def test_claude_strategic(self):
        h = get_harness("Claude Code (Fable)")
        assert h is not None
        assert "strategic_thinking" in h.best_for

    def test_opencode_systems(self):
        h = get_harness("OpenCode")
        assert h is not None
        assert "systems_engineering" in h.best_for

    def test_mmx_media(self):
        h = get_harness("MMX (MiniMax)")
        assert h is not None
        assert "image_generation" in h.best_for

    def test_ollama_local(self):
        h = get_harness("Ollama (Local GPU)")
        assert h is not None
        assert "local_inference" in h.best_for

    def test_deepinfra_multi(self):
        h = get_harness("DeepInfra MCP")
        assert h is not None
        assert "multi_model_dispatch" in h.best_for

    def test_deepseek_cheap(self):
        h = get_harness("DeepSeek API")
        assert h is not None
        assert "cheap_analysis" in h.best_for

    def test_glm_bulk(self):
        h = get_harness("GLM Subagents (Z.ai Max)")
        assert h is not None
        assert "bulk_work" in h.best_for


# ─── get_harness tests ─────────────────────────────────────────────

class TestGetHarness:
    def test_exact_name(self):
        h = get_harness("KimiCode")
        assert h is not None
        assert h.name == "KimiCode"

    def test_case_insensitive(self):
        h = get_harness("kimicode")
        assert h is not None
        assert h.name == "KimiCode"

    def test_mixed_case(self):
        h = get_harness("KiMiCoDe")
        assert h is not None

    def test_not_found(self):
        assert get_harness("nonexistent") is None

    def test_empty_string(self):
        assert get_harness("") is None

    def test_partial_name_no_match(self):
        """Partial names should not match."""
        assert get_harness("Kimi") is None

    def test_name_with_spaces(self):
        h = get_harness("Claude Code (Fable)")
        assert h is not None

    def test_name_with_spaces_case_insensitive(self):
        h = get_harness("claude code (fable)")
        assert h is not None


# ─── all_harnesses tests ───────────────────────────────────────────

class TestAllHarnesses:
    def test_returns_list(self):
        result = all_harnesses()
        assert isinstance(result, list)

    def test_returns_copy(self):
        """Modifying the returned list should not affect HARNESS_NOTES."""
        result = all_harnesses()
        original_len = len(result)
        result.clear()
        assert len(HARNESS_NOTES) == original_len

    def test_contains_all(self):
        result = all_harnesses()
        assert len(result) == len(HARNESS_NOTES)

    def test_items_are_same_objects(self):
        """The profiles themselves are the same frozen objects."""
        result = all_harnesses()
        for i, h in enumerate(result):
            assert h is HARNESS_NOTES[i]


# ─── Cross-field consistency tests ─────────────────────────────────

class TestCrossFieldConsistency:
    def test_no_overlap_best_poor(self):
        """A harness shouldn't be best_for and poor_for the same thing."""
        for h in HARNESS_NOTES:
            overlap = set(h.best_for) & set(h.poor_for)
            assert not overlap, f"{h.name}: {overlap} in both best_for and poor_for"

    def test_notes_substantial(self):
        """Notes should contain actual observations, not just placeholders."""
        for h in HARNESS_NOTES:
            assert len(h.notes) > 50, f"{h.name}: notes too short ({len(h.notes)} chars)"

    def test_speed_mentioned_in_notes_or_speed(self):
        """Speed info should be present somewhere."""
        for h in HARNESS_NOTES:
            combined = (h.speed + " " + h.notes).lower()
            assert any(w in combined for w in ["fast", "slow", "speed", "tok", "min", "sec", "quick", "async", "polling"]), \
                f"{h.name}: no speed info"

    def test_reliability_mentioned(self):
        """Reliability info should contain actual reliability assessment."""
        for h in HARNESS_NOTES:
            assert len(h.reliability) > 10, f"{h.name}: reliability too short"
