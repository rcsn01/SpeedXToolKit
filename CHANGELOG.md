# CHANGELOG

All notable changes to this project will be documented in this file.

The format is based on "Keep a Changelog" and this file is organized by version, with the newest versions at the top.

---

## v2.0 - 2025-09-22
### Highlights
- Project milestone labeled `v2.0` — consolidated cumulative improvements and enhancements since v1.0.
- Stable delta-calculation workflows and packaging/readme improvements were included.

### Added
- Consolidated earlier enhancements and README polish.

### Fixed
- Various fixes and cleanups across the codebase (presets, packaging notes, readme clarity).

---

## v1.5 - 2025-08-08
### Highlights
- Added delta calculation feature.

### Added
- `delta_calculation_model`: computes column1 - column2 as `delta`, with optional threshold logic integrated into Output rules.
- README updates documenting the delta calculation feature.

### Fixed
- Minor housekeeping and README clarifications.

---

## v1.1 - 2025-07-30
### Highlights
- Housekeeping and packaging readiness.

### Added
- Requirements fixes and clarifications.
- Project version number added to repository (version tracking).
- Readme updates and documentation polish.

### Fixed
- Typos and requirements management issues.

---

## v1.0 - 2025-07-30
### Highlights
- First major stable release.

### Added
- Core processing pipeline and UI stabilized:
  - Robust file import (Excel & CSV), header detection and duplication handling.
  - Column operations (keep/drop/rename), pivot support.
  - Output column generation and presets save/load.
  - Scrollable preview UI and theme polish.

### Fixed
- Consolidation of prior bug fixes and polishing from earlier pre-release iterations.

---

## v0.8 - 2025-04-23 → 2025-05-01
### Highlights
- Preset saving fixed and UI checkbox improvements.

### Added
- Checkbox selection UI improvements for column selection.

### Fixed
- Fixed broken preset saving introduced in earlier pre-release.

---

## v0.5 - 2025-04-05 → 2025-04-22
### Highlights
- Scrollable preview improvements and first implementation of preset save/load.

### Added
- Scrollable preview optimization and performance improvements.
- Ability to save processing order (basis for presets system).
- Initial preset save/load (marked as buggy in early commit notes).

### Fixed
- Iterative UI polish.

---

## v0.2 - 2025-03-28 → 2025-04-04
### Highlights
- Button wiring and controller scaffolding.

### Added
- Controllers to orchestrate UI actions.
- Button wiring across UI components.

### Fixed
- Initial connectivity and wiring issues.

---

## v0.1 - 2025-03-06 → 2025-03-23
### Highlights
- Initial project scaffold and basic GUI elements.

### Added
- Project scaffolding and temporary GUI windows.

---


### Notes
- Version boundaries were assigned from the git history using logical milestones and representative commits. If you prefer semantic versioning with different break points (for example marking delta calculation as `v2.0` if considered a major API change), I can reassign versions and update the changelog.

- Next optional steps:
  - Create git tags for `v1.0` and `v2.0` on their representative commits.
  - Add the changelog to repository and make a commit (done below).

