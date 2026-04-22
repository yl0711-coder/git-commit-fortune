"""Data models for commit analysis."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Commit:
    """A small normalized view of a Git commit."""

    hash: str
    timestamp: int
    author: str
    subject: str


@dataclass(frozen=True)
class CommitStats:
    """Statistics derived from Git commit history."""

    total: int
    authors: int
    after_hours: int
    weekend: int
    average_subject_length: float
    keyword_counts: dict[str, int] = field(default_factory=dict)

    def ratio(self, value: int) -> float:
        """Return a safe ratio for a count against total commits."""

        if self.total == 0:
            return 0.0
        return value / self.total


@dataclass(frozen=True)
class Fortune:
    """A generated repository fortune."""

    mood: str
    spirit_animal: str
    signs: list[str]
    prediction: str
    advice: str
    stats: CommitStats

