# Git Commit Fortune

Read a repository's Git history and generate a playful fortune about the codebase.

It is not a serious analytics tool. It is a small local CLI that turns commit patterns into a screenshot-friendly repository reading.

## Why It Exists

Git history contains patterns:

- too many midnight commits
- too many commits containing `fix`
- too many `final`, `temporary`, or `wip` messages
- weekend commits that should probably have waited
- short commit messages that hide motive

`git-commit-fortune` reads those signals and turns them into a small fortune report.

## Installation

From a source checkout:

```bash
bin/git-commit-fortune
```

Or install locally in editable mode:

```bash
python3 -m pip install -e .
git-commit-fortune
```

## Usage

Analyze the current repository:

```bash
git-commit-fortune
```

Analyze another repository:

```bash
git-commit-fortune /path/to/repo
```

Use fewer commits:

```bash
git-commit-fortune --limit 30
```

Print JSON:

```bash
git-commit-fortune --json
```

## Example Output

```text
Git Commit Fortune

Repository: /path/to/repo

Omen: The Final That Was Not Final
Fortune level: cursed but deployable
Repository mood: functional but emotionally unavailable
Spirit animal: a caffeinated octopus holding a rollback plan

Signs:
- 80 recent commits were consulted
- 2 author(s) left fingerprints in the history
- 26 commit(s) mention fix, bug, or hotfix
- 7 commit(s) happened after 10 PM or before 6 AM
- "final" appeared 2 time(s), which is rarely final

Prediction:
A commit called 'final final' will appear before anyone admits defeat.

Advice:
Before the next fix, ask whether the bug is a symptom or a tradition.

Lucky command:
git log --oneline --grep=final
```

## JSON Output

```bash
git-commit-fortune --json
```

JSON output includes:

- repository path
- generated fortune
- statistics used by the fortune generator
- lucky command suggestion

This is useful if you want to build a badge, dashboard, or another wrapper around the output.

## What It Checks

The first version looks at recent commit history and detects:

- author count
- commit count
- after-hours commits
- weekend commits
- average subject length
- keywords such as `fix`, `bug`, `hotfix`, `wip`, `temporary`, `final`, `hack`, and `release`

## Non-Goals

This project is intentionally small.

It does not try to be:

- a serious Git analytics platform
- a productivity tracker
- a team performance measurement tool
- a dashboard
- a remote service

It should stay local, lightweight, and fun.

## Development

Run tests:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```

Compile source:

```bash
python3 -m compileall src tests
```

Run the CLI from source:

```bash
bin/git-commit-fortune --limit 20
```

## License

MIT
