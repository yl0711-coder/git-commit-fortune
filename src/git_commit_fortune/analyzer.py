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
        created_at = datetime.fromtimestamp(commit.timestamp).astimezone()
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
            omen="uncommitted timeline",
            fortune_level="unreadable",
            mood="silent but suspicious",
            spirit_animal="an empty terminal blinking at midnight",
            signs=["no commits were found"],
            prediction="The repository is waiting for its first questionable decision.",
            advice="Make the first commit before asking the oracle again.",
            lucky_command="git commit --allow-empty -m \"begin\"",
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
    omen = choose_omen(stats, fix_like, chaos_like, final_count)
    fortune_level = choose_fortune_level(stats, fix_like, chaos_like, final_count)
    mood = choose_mood(stats, fix_like, chaos_like)
    animal = choose_spirit_animal(stats, fix_like, chaos_like)
    prediction = choose_prediction(stats, fix_like, chaos_like, final_count)
    advice = choose_advice(stats, fix_like, chaos_like)
    lucky_command = choose_lucky_command(stats, fix_like, chaos_like, final_count)

    return Fortune(
        omen=omen,
        fortune_level=fortune_level,
        mood=mood,
        spirit_animal=animal,
        signs=signs,
        prediction=prediction,
        advice=advice,
        lucky_command=lucky_command,
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
    if stats.average_subject_length >= 48:
        signs.append("commit messages explain enough to make future blame awkward")

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
    if stats.average_subject_length >= 48:
        return "over-explained but emotionally sincere"
    if stats.authors >= 5:
        return "crowded but surprisingly civil"
    return "stable enough to be suspicious"


def choose_omen(
    stats: CommitStats,
    fix_like: int,
    chaos_like: int,
    final_count: int,
) -> str:
    """Choose the headline omen."""

    if final_count >= 2:
        return "The Final That Was Not Final"
    if stats.ratio(chaos_like) >= 0.25:
        return "The Temporary Permanent"
    if stats.ratio(fix_like) >= 0.35:
        return "The Endless Fix"
    if stats.ratio(stats.after_hours) >= 0.30:
        return "The Midnight Push"
    if stats.ratio(stats.weekend) >= 0.25:
        return "The Weekend Whisper"
    if stats.average_subject_length >= 48:
        return "The Verbose Prophecy"
    if stats.authors >= 5:
        return "The Many Hands"
    return "The Calm Before Refactor"


def choose_fortune_level(
    stats: CommitStats,
    fix_like: int,
    chaos_like: int,
    final_count: int,
) -> str:
    """Choose a playful severity level."""

    if final_count >= 2 or stats.ratio(chaos_like) >= 0.30:
        return "cursed but deployable"
    if stats.ratio(fix_like) >= 0.35 or stats.ratio(stats.after_hours) >= 0.35:
        return "unstable magic"
    if stats.ratio(stats.weekend) >= 0.25:
        return "weekend haunted"
    if stats.average_subject_length >= 48:
        return "well-documented anxiety"
    if stats.total < 5:
        return "too young to trust"
    return "mostly harmless"


def choose_spirit_animal(stats: CommitStats, fix_like: int, chaos_like: int) -> str:
    """Choose a spirit animal."""

    if stats.ratio(chaos_like) >= 0.20:
        return "a raccoon with deploy access"
    if stats.ratio(fix_like) >= 0.30:
        return "a caffeinated octopus holding a rollback plan"
    if stats.ratio(stats.after_hours) >= 0.30:
        return "an owl reviewing pull requests in the dark"
    if stats.average_subject_length >= 48:
        return "a librarian labeling every exception path"
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
    if stats.average_subject_length >= 48:
        return "The next commit message may qualify as internal documentation."
    return "The repository will remain peaceful until someone opens an old TODO."


def choose_advice(stats: CommitStats, fix_like: int, chaos_like: int) -> str:
    """Choose maintenance advice."""

    if stats.ratio(chaos_like) >= 0.20:
        return "Write down what 'temporary' means before it becomes architecture."
    if stats.ratio(fix_like) >= 0.30:
        return "Before the next fix, ask whether the bug is a symptom or a tradition."
    if stats.ratio(stats.after_hours) >= 0.30:
        return "Review late-night commits during daylight."
    if stats.average_subject_length >= 48:
        return "Keep writing context, but make sure the code still agrees."
    return "Tag a release while the repository still trusts you."


def choose_lucky_command(
    stats: CommitStats,
    fix_like: int,
    chaos_like: int,
    final_count: int,
) -> str:
    """Choose a lucky command to run next."""

    if final_count:
        return "git log --oneline --grep=final"
    if stats.ratio(chaos_like) >= 0.20:
        return "git grep -n \"TODO\\|temporary\\|hack\""
    if stats.ratio(fix_like) >= 0.30:
        return "git log --oneline --grep=fix"
    if stats.ratio(stats.after_hours) >= 0.30:
        return "git log --after=midnight --oneline"
    if stats.average_subject_length >= 48:
        return "git log --format=%s -n 5"
    return "git status --short"
