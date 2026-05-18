# Git Commit Fortune v0.1.2

This maintenance release finishes the strict-mode work and fixes package version metadata.

## Added

- Added `--strict` mode for CI-friendly checks.
- `--strict` keeps the normal fortune output and exits with code `1` when risky commit patterns are detected.
- Strict findings are printed to stderr so CI logs show why the command failed.

## Fixed

- Updated `pyproject.toml` to `0.1.2`.
- Updated `git_commit_fortune.__version__` to `0.1.2`.
- Kept package metadata aligned with the current release tag.

## Validation

- Unit tests passed.
- Source compilation passed.
- Package metadata installation check passed.
- CLI strict-mode behavior is covered by tests.
