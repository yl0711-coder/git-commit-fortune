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
        f"Omen: {fortune.omen}",
        f"Fortune level: {fortune.fortune_level}",
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
            "",
            "Lucky command:",
            fortune.lucky_command,
        ]
    )

    return "\n".join(lines)


def render_json(fortune: Fortune, repository: str) -> str:
    """Render a machine-readable report."""

    payload = {
        "repository": repository,
        "fortune": {
            "omen": fortune.omen,
            "fortune_level": fortune.fortune_level,
            "mood": fortune.mood,
            "spirit_animal": fortune.spirit_animal,
            "signs": fortune.signs,
            "prediction": fortune.prediction,
            "advice": fortune.advice,
            "lucky_command": fortune.lucky_command,
        },
        "stats": asdict(fortune.stats),
    }

    return json.dumps(payload, indent=2, ensure_ascii=False)
