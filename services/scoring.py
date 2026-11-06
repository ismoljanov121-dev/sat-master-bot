"""
Grading and score estimates.

SAT sections use a small item-response model: each question has a difficulty, the student an ability,
and the estimate is the posterior mean over a normal prior. Harder questions therefore count for more,
and the posterior spread gives an honest score range. The calibration is ours, not College Board's.
"""

import math
import re
from fractions import Fraction
from typing import Any, Iterable, Optional

DIFFICULTY_B = {"Easy": -1.0, "Medium": 0.0, "Hard": 1.0}
DISCRIMINATION = 1.3
GUESS_MCQ = 0.2
SCALE_MEAN = 500
SCALE_SD = 110
ROUTE_THRESHOLD = 0.55

_GRID = [i / 10 for i in range(-45, 46)]
_PRIOR = [math.exp(-t * t / 2) for t in _GRID]

LISTENING_BANDS = [(39, 9), (37, 8.5), (35, 8), (32, 7.5), (30, 7), (26, 6.5), (23, 6), (18, 5.5), (16, 5),
                   (13, 4.5), (10, 4), (8, 3.5), (6, 3), (4, 2.5), (3, 2), (2, 1.5), (1, 1)]
READING_BANDS = [(39, 9), (37, 8.5), (35, 8), (33, 7.5), (30, 7), (27, 6.5), (23, 6), (19, 5.5), (15, 5),
                 (13, 4.5), (10, 4), (8, 3.5), (6, 3), (4, 2.5), (3, 2), (2, 1.5), (1, 1)]


def parse_number(text: Any) -> Optional[Fraction]:
    """Reads a grid-in answer: 12, -2.5, .75 or 3/4."""
    value = str(text if text is not None else "").strip().replace(" ", "").replace("−", "-").replace(",", ".")
    if not re.fullmatch(r"-?(\d+(\.\d*)?|\.\d+)(/\d+(\.\d*)?)?", value):
        return None
    try:
        if "/" in value:
            top, bottom = value.split("/")
            return Fraction(top) / Fraction(bottom)
        return Fraction(value)
    except (ValueError, ZeroDivisionError):
        return None


def sat_answer_correct(question: dict[str, Any], value: Any) -> bool:
    if question["type"] == "spr":
        given = parse_number(value)
        if given is None:
            return False
        for accepted in question["ans"]:
            target = parse_number(accepted)
            # A rounded decimal such as 0.6667 is accepted for 2/3.
            if target is not None and abs(given - target) <= Fraction(1, 2000):
                return True
        return False
    return value == question["cor"]


def estimate_ability(items: Iterable[tuple[str, str, bool]]) -> tuple[float, float]:
    """Takes (difficulty, type, correct) rows and returns the ability estimate and its uncertainty."""
    log_likelihood = [0.0] * len(_GRID)
    for difficulty, kind, correct in items:
        b = DIFFICULTY_B[difficulty]
        guess = GUESS_MCQ if kind == "mcq" else 0.0
        for index, theta in enumerate(_GRID):
            p = guess + (1 - guess) / (1 + math.exp(-DISCRIMINATION * (theta - b)))
            log_likelihood[index] += math.log(p if correct else 1 - p)
    peak = max(log_likelihood)
    weights = [prior * math.exp(ll - peak) for prior, ll in zip(_PRIOR, log_likelihood)]
    total = sum(weights)
    mean = sum(w * t for w, t in zip(weights, _GRID)) / total
    variance = sum(w * (t - mean) ** 2 for w, t in zip(weights, _GRID)) / total
    return mean, math.sqrt(variance)


def _round10(value: float) -> int:
    return int(round(value / 10) * 10)


def _clip(value: float) -> int:
    return min(800, max(200, _round10(value)))


def section_score(items: list[tuple[str, str, bool]]) -> dict[str, int]:
    theta, spread = estimate_ability(items)
    center = SCALE_MEAN + SCALE_SD * theta
    half = max(20, _round10(SCALE_SD * spread))
    return {"score": _clip(center), "low": _clip(center - half), "high": _clip(center + half), "spread": half}


def total_score(rw: dict[str, int], math_section: dict[str, int]) -> dict[str, int]:
    score = rw["score"] + math_section["score"]
    half = max(30, _round10(math.hypot(rw["spread"], math_section["spread"])))
    return {"score": score, "low": max(400, score - half), "high": min(1600, score + half)}


def route_for(correct: int, total: int) -> str:
    return "hard" if total and correct / total >= ROUTE_THRESHOLD else "easy"


def normalize_ielts(value: Any) -> str:
    text = str(value if value is not None else "").strip().lower()
    text = re.sub(r"(\d),(?=\d{3}\b)", r"\1", text)
    text = re.sub(r"(\d)(st|nd|rd|th)\b", r"\1", text)
    text = re.sub(r"^(a|an|the)\s+", "", text)
    text = re.sub(r"[.\s]+$", "", text)
    return re.sub(r"\s+", " ", text)


def ielts_answer_correct(question: dict[str, Any], value: Any) -> bool:
    given = normalize_ielts(value)
    if not given:
        return False
    return any(normalize_ielts(accepted) == given for accepted in [question["ans"], *question.get("alts", [])])


def ielts_band(correct: int, table: list[tuple[int, float]]) -> float:
    return next((band for minimum, band in table if correct >= minimum), 0.0)
