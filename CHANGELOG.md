# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-08-05

### Fixed
- Syntax error in atlas.py: unterminated string literal in DEEPSEEK_V3 failure_modes (mixed quotes)
- Test count: updated test_default_has_all_models from 13 to 15 models (GRANITE_3_1_2B and QWEN_0_5B added)

### Added
- MIT LICENSE
- This CHANGELOG.md

## [0.1.0] - 2026-08-04

### Added
- ModelAtlas with 15 model profiles covering the full SuperInstance fleet
- CastingDirector for role-to-model routing with counterpoint enforcement
- Tempo profiles for pipeline roles
- What-if analysis for model swaps
- Harness notes for integration patterns
- 86-test comprehensive suite covering atlas, casting, counterpoint, and what-if
