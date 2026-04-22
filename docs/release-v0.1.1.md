# Git Commit Fortune v0.1.1

This release keeps the project small while improving sharing, documentation, and commit-history filtering.

## Added

- Added `--one-line` output for compact, screenshot-friendly fortunes.
- Added `--since` support using Git-native date expressions, such as:
  - `--since "2 weeks ago"`
  - `--since 2026-01-01`
- Added Chinese README.
- Added bilingual documentation maintenance notes.
- Added extra fortune templates for verbose commit histories.

## Changed

- Clarified local-time handling when analyzing after-hours commits.
- Updated English and Chinese README files together so usage and examples remain aligned.

## Validation

- Unit tests passed.
- Source compilation passed.
- CLI output checks passed.

