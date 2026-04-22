"""Analyze commit history and generate a fortune."""

from __future__ import annotations

from datetime import datetime

from .models import Commit, CommitStats, Fortune

KEYWORDS = [
    "fix",
    "bug",
    "hotfix",
    "wip",
    "temp",
    "temporary",
    "final",
    "quick",
    "hack",
    "refactor",
    "release",
]


def analyze(commits: list[Commit]) -> CommitStats:
    """Build commit statistics."""

    authors = {commit.author for commit in commits}
    after_hours = 0
    weekend = 0
    total_subject_length = 0
    keyword_counts = {keyword: 0 for keyword in KEYWORDS}

    for commit in commits:
        created_at = datetime.fromtimestamp(commit.timestamp)
        if created_at.hour >= 22 or created_at.hour < 6:
            after_hours += 1
        if created_at.weekday() >= 5:
            weekend += 1

        subject = commit.subject.lower()
        total_subject_length += len(commit.subject)
        for keyword in KEYWORDS:
            if keyword in subject:
                keyword_counts[keyword] += 1

    total = len(commits)
    average_subject_length = total_subject_length / total if total else 0.0

    return CommitStats(
        total=total,
        authors=len(authors),
        after_hours=after_hours,
        weekend=weekend,
        average_subject_length=average_subject_length,
        keyword_counts=keyword_counts,
    )


def generate_fortune(stats: CommitStats) -> Fortune:
    """Generate a playful fortune from commit statistics."""

    if stats.total == 0:
        return Fortune(
            mood="silent but suspicious",
            spirit_animal="an empty terminal blinking at midnight",
            signs=["no commits were found"],
            prediction="The repository is waiting for its first questionable decision.",
            advice="Make the first commit before asking the oracle again.",
            stats=stats,
        )

    fix_like = (
        stats.keyword_counts.get("fix", 0)
        + stats.keyword_counts.get("bug", 0)
        + stats.keyword_counts.get("hotfix", 0)
    )
    chaos_like = (
        stats.keyword_counts.get("wip", 0)
        + stats.keyword_counts.get("temp", 0)
        + stats.keyword_counts.get("temporary", 0)
        + stats.keyword_counts.get("hack", 0)
    )
    final_count = stats.keyword_counts.get("final", 0)

    signs = build_signs(stats, fix_like, chaos_like, final_count)
    mood = choose_mood(stats, fix_like, chaos_like)
    animal = choose_spirit_animal(stats, fix_like, chaos_like)
    prediction = choose_prediction(stats, fix_like, chaos_like, final_count)
    advice = choose_advice(stats, fix_like, chaos_like)

    return Fortune(
        mood=mood,
        spirit_animal=animal,
        signs=signs,
        prediction=prediction,
        advice=advice,
        stats=stats,
    )


def build_signs(
    stats: CommitStats,
    fix_like: int,
    chaos_like: int,
    final_count: int,
) -> list[str]:
    """Build human-readable signs for the fortune."""

    signs = [
        f"{stats.total} recent commits were consulted",
        f"{stats.authors} author(s) left fingerprints in the history",
    ]

    if fix_like:
        signs.append(f"{fix_like} commit(s) mention fix, bug, or hotfix")
    if chaos_like:
        signs.append(f"{chaos_like} commit(s) smell like WIP, temporary code, or hacks")
    if final_count:
        signs.append(f'"final" appeared {final_count} time(s), which is rarely final')
    if stats.after_hours:
        signs.append(f"{stats.after_hours} commit(s) happened after 10 PM or before 6 AM")
    if stats.weekend:
        signs.append(f"{stats.weekend} commit(s) happened during the weekend")
    if stats.average_subject_length < 18:
        signs.append("commit messages are short enough to hide motive")

    return signs


def choose_mood(stats: CommitStats, fix_like: int, chaos_like: int) -> str:
    """Choose a repository mood."""

    if stats.ratio(chaos_like) >= 0.25:
        return "held together by intent and terminal history"
    if stats.ratio(fix_like) >= 0.35:
        return "functional but emotionally unavailable"
    if stats.ratio(stats.after_hours) >= 0.30:
        return "nocturnal and slightly over-caffeinated"
    if stats.ratio(stats.weekend) >= 0.25:
        return "unable to respect weekends"
    if stats.authors >= 5:
        return "crowded but surprisingly civil"
    return "stable enough to be suspicious"


def choose_spirit_animal(stats: CommitStats, fix_like: int, chaos_like: int) -> str:
    """Choose a spirit animal."""

    if stats.ratio(chaos_like) >= 0.20:
        return "a raccoon with deploy access"
    if stats.ratio(fix_like) >= 0.30:
        return "a caffeinated octopus holding a rollback plan"
    if stats.ratio(stats.after_hours) >= 0.30:
        return "an owl reviewing pull requests in the dark"
    if stats.authors >= 5:
        return "a committee of ants carrying one architecture diagram"
    return "a calm capybara sitting on green CI"


def choose_prediction(
    stats: CommitStats,
    fix_like: int,
    chaos_like: int,
    final_count: int,
) -> str:
    """Choose a future prediction."""

    if final_count:
        return "A commit called 'final final' will appear before anyone admits defeat."
    if stats.ratio(chaos_like) >= 0.20:
        return "A temporary decision will become infrastructure."
    if stats.ratio(fix_like) >= 0.30:
        return "The next fix will reveal the previous fix's secret twin."
    if stats.ratio(stats.after_hours) >= 0.30:
        return "A late-night commit will look brave until morning."
    return "The repository will remain peaceful until someone opens an old TODO."


def choose_advice(stats: CommitStats, fix_like: int, chaos_like: int) -> str:
    """Choose maintenance advice."""

    if stats.ratio(chaos_like) >= 0.20:
        return "Write down what 'temporary' means before it becomes architecture."
    if stats.ratio(fix_like) >= 0.30:
        return "Before the next fix, ask whether the bug is a symptom or a tradition."
    if stats.ratio(stats.after_hours) >= 0.30:
        return "Review late-night commits during daylight."
    return "Tag a release while the repository still trusts you."

