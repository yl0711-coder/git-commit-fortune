# Git Commit Fortune v0.1.0

Initial public release of Git Commit Fortune.

Git Commit Fortune is a small local CLI that reads Git commit history and generates a playful repository fortune.

## Features

- Analyze the current Git repository or a specified repository path.
- Limit the number of recent commits consulted with `--limit`.
- Detect commit-history signals such as:
  - author count
  - after-hours commits
  - weekend commits
  - short commit messages
  - keywords such as `fix`, `bug`, `hotfix`, `wip`, `temporary`, `final`, and `hack`
- Generate a terminal-friendly report with:
  - omen
  - fortune level
  - repository mood
  - spirit animal
  - signs
  - prediction
  - advice
  - lucky command
- Support JSON output with `--json`.
- Run locally without external APIs or third-party runtime dependencies.

## Example

```bash
bin/git-commit-fortune /path/to/repo --limit 40
```

```text
Git Commit Fortune

Repository: /path/to/repo

Omen: The Calm Before Refactor
Fortune level: mostly harmless
Repository mood: stable enough to be suspicious
Spirit animal: a calm capybara sitting on green CI

Signs:
- 37 recent commits were consulted
- 2 author(s) left fingerprints in the history
- 2 commit(s) mention fix, bug, or hotfix

Prediction:
The repository will remain peaceful until someone opens an old TODO.

Advice:
Tag a release while the repository still trusts you.

Lucky command:
git status --short
```

## Non-Goals

This is intentionally not a serious Git analytics platform, productivity tracker, dashboard, or team performance measurement tool.

It is meant to stay local, lightweight, and fun.
