"""Read commit history from Git."""

from __future__ import annotations

from pathlib import Path
import subprocess

from .models import Commit

# Guards against a hung or pathological `git log` blocking the CLI forever.
GIT_TIMEOUT_SECONDS = 15


class GitError(RuntimeError):
    """Raised when Git history cannot be read."""


def read_commits(repository: Path, limit: int, since: str | None = None) -> list[Commit]:
    """Read recent commits from a Git repository.

    The optional ``since`` value is passed to Git as-is so users can reuse
    familiar Git date expressions such as ``2 weeks ago`` or ``2026-01-01``.
    """

    command = [
        "git",
        "-C",
        str(repository),
        "log",
        f"--max-count={limit}",
        "--date=unix",
        "--format=%H%x1f%ct%x1f%an%x1f%s",
    ]
    if since:
        # Appended rather than inserted at a fixed index: git accepts log
        # options in any order, so this does not depend on the position of
        # the other flags above.
        command.append(f"--since={since}")

    try:
        result = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=GIT_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired as exc:
        raise GitError(f"git log timed out after {GIT_TIMEOUT_SECONDS}s") from exc
    except OSError as exc:
        raise GitError(f"failed to run git: {exc}") from exc

    if result.returncode != 0:
        message = result.stderr.strip() or "not a Git repository"
        raise GitError(message)

    commits: list[Commit] = []
    for line in result.stdout.splitlines():
        parts = line.split("\x1f", 3)
        if len(parts) != 4:
            continue
        commit_hash, timestamp, author, subject = parts
        try:
            commit_timestamp = int(timestamp)
        except ValueError:
            continue
        commits.append(
            Commit(
                hash=commit_hash,
                timestamp=commit_timestamp,
                author=author,
                subject=subject,
            )
        )

    return commits
