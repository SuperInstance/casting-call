"""
Tempo profiles for pipeline roles.

Each role has a natural tempo — the BPM range where that stage feels right.
Intent parsing is Allegro (fast, expansive). Personality wrapping is Adagio
(slow, deliberate). Code generation is Andante (steady, walking).

These map to the TempoMap stages in slackwater-tempo (Layer 3) and to the
pipeline beat structure in the Grand Plan §2 data flow.
"""

from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class TempoProfile:
    """The natural tempo for a pipeline role."""
    name: str          # Italian term: Allegro, Andante, etc.
    bpm_low: int       # minimum BPM for this role
    bpm_high: int      # maximum BPM for this role
    description: str   # what this tempo feels like in the pipeline


# The canonical tempo assignments, from the Grand Plan and Nemotron analysis §6.3.
# These are the same numbers that slackwater-tempo's TempoMap uses for stage transitions.

ROLE_TEMPO_PROFILES: dict[str, TempoProfile] = {
    "intent_parse": TempoProfile(
        name="Allegro",
        bpm_low=120,
        bpm_high=140,
        description="Fast, expansive — parse the intent before the player finishes sitting down.",
    ),
    "planning": TempoProfile(
        name="Moderato",
        bpm_low=90,
        bpm_high=110,
        description="Walking pace — the planner needs to think but must not stall.",
    ),
    "code_gen": TempoProfile(
        name="Andante",
        bpm_low=80,
        bpm_high=100,
        description="Steady, walking — code generation is a rhythm, not a sprint.",
    ),
    "personality_wrap": TempoProfile(
        name="Adagio",
        bpm_low=50,
        bpm_high=70,
        description="Slow, expressive — the voice takes its time because the line matters.",
    ),
    "safety_check": TempoProfile(
        name="Largo",
        bpm_low=40,
        bpm_high=55,
        description="Very slow, solemn — safety is the cathedral gate. It does not hurry.",
    ),
    "creative_ideation": TempoProfile(
        name="Rubato",
        bpm_low=60,
        bpm_high=160,
        description="Free tempo — creativity follows no metronome.",
    ),
    "spatial_reasoning": TempoProfile(
        name="Moderato",
        bpm_low=85,
        bpm_high=110,
        description="Measured, deliberate — spatial decomposition needs room to breathe.",
    ),
    "synthesis": TempoProfile(
        name="Andante",
        bpm_low=70,
        bpm_high=95,
        description="Gentle, gathering — synthesis pulls threads together without rushing.",
    ),
    "vision": TempoProfile(
        name="Moderato",
        bpm_low=90,
        bpm_high=115,
        description="Clear, forward-looking — vision scans the horizon at a steady walk.",
    ),
    "voice": TempoProfile(
        name="Adagio",
        bpm_low=55,
        bpm_high=75,
        description="Slow, warm — the spoken line arrives after the build, like a breath.",
    ),
    "forced_perspective": TempoProfile(
        name="Vivace",
        bpm_low=100,
        bpm_high=160,
        description="Lively, shifting — the catalyst cracks open assumptions at a whim.",
    ),
    "creative_nonfiction": TempoProfile(
        name="Andante",
        bpm_low=70,
        bpm_high=95,
        description="Walking, deliberate — prose that takes its time because each sentence carries weight.",
    ),
    "sensory_creative": TempoProfile(
        name="Lento",
        bpm_low=50,
        bpm_high=80,
        description="Slow, sensual — sensory writing goes to the body first. The body does not hurry.",
    ),
}
