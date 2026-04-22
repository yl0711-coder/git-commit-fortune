"""Render fortune reports."""

from __future__ import annotations

from dataclasses import asdict
import json

from .models import Fortune


def render_text(fortune: Fortune, repository: str) -> str:
    """Render a terminal-friendly fortune report."""

    lines = [
        "Git Commit Fortune",
        "",
        f"Repository: {repository}",
        "",
        f"Repository mood: {fortune.mood}",
        f"Spirit animal: {fortune.spirit_animal}",
        "",
        "Signs:",
    ]

    for sign in fortune.signs:
        lines.append(f"- {sign}")

    lines.extend(
        [
            "",
            "Prediction:",
            fortune.prediction,
            "",
            "Advice:",
            fortune.advice,
        ]
    )

    return "\n".join(lines)


def render_json(fortune: Fortune, repository: str) -> str:
    """Render a machine-readable report."""

    payload = {
        "repository": repository,
        "fortune": {
            "mood": fortune.mood,
            "spirit_animal": fortune.spirit_animal,
            "signs": fortune.signs,
            "prediction": fortune.prediction,
            "advice": fortune.advice,
        },
        "stats": asdict(fortune.stats),
    }

    return json.dumps(payload, indent=2, ensure_ascii=False)

