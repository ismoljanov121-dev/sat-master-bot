"""
Read-only access to the built content. The API grades against these same files.

webapp/data/ is public. Sealed exams live in data/sealed_exams.json, which is never served, so they reach
students only through a group exam and without answer keys.
"""

import json
from pathlib import Path
from typing import Any, Optional

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "webapp" / "data"
SEALED_FILE = BASE_DIR / "data" / "sealed_exams.json"

SAT_DOMAINS = {
    "rw": ["Craft and Structure", "Information and Ideas", "Standard English Conventions", "Expression of Ideas"],
    "m": ["Algebra", "Advanced Math", "Problem-Solving and Data Analysis", "Geometry and Trigonometry"],
}


DOMAIN_NAMES = {
    "Craft and Structure": "So'z va matn tuzilishi",
    "Information and Ideas": "Axborot va g'oyalar",
    "Standard English Conventions": "Grammatika qoidalari",
    "Expression of Ideas": "Fikrni ifodalash",
    "Algebra": "Algebra",
    "Advanced Math": "Murakkab algebra",
    "Problem-Solving and Data Analysis": "Ma'lumotlar tahlili",
    "Geometry and Trigonometry": "Geometriya va trigonometriya",
}


def _load(name: str) -> Any:
    return json.loads((DATA_DIR / name).read_text(encoding="utf-8"))


def mock_question_ids(mock: dict[str, Any]) -> set[str]:
    return {question_id for part in ("rw", "math") for ids in mock[part].values() for question_id in ids}


class Content:
    def __init__(self) -> None:
        sealed = json.loads(SEALED_FILE.read_text(encoding="utf-8"))
        self.bank: dict[str, dict[str, Any]] = {q["id"]: q for q in [*_load("sat_bank.json"), *sealed["questions"]]}
        self.notes: dict[str, dict[str, str]] = {**_load("sat_notes.json"), **sealed["notes"]}
        self.mocks: dict[str, dict[str, Any]] = {m["id"]: m for m in [*_load("sat_mocks.json"), *sealed["mocks"]]}
        ielts = _load("ielts.json")
        self.listening: dict[int, dict[str, Any]] = {t["num"]: t for t in ielts["listening"]}
        self.reading: dict[int, dict[str, Any]] = {t["num"]: t for t in [*ielts["reading"], *sealed["reading"]]}
        self.writing: dict[str, list[dict[str, Any]]] = _load("ielts_writing.json")
        self.writing_by_id = {w["id"]: w for items in self.writing.values() for w in items}

        self.sealed_questions: set[str] = {q["id"] for q in sealed["questions"]}
        self.sealed_mocks: set[str] = {m["id"] for m in sealed["mocks"]}
        self.sealed_reading: set[int] = {t["num"] for t in sealed["reading"]}
        self.mock_questions: dict[str, set[str]] = {m["id"]: mock_question_ids(m) for m in self.mocks.values()}
        self.mock_of: dict[str, str] = {qid: mock_id for mock_id, ids in self.mock_questions.items() for qid in ids}

    def public_mocks(self) -> list[dict[str, Any]]:
        return sorted((m for m in self.mocks.values() if m["id"] not in self.sealed_mocks), key=lambda m: m["num"])

    def next_mock(self, taken: set[str]) -> Optional[str]:
        """The open mock a student reaches next. Practice stays away from it, so it remains a clean measure."""
        return next((m["id"] for m in self.public_mocks() if m["id"] not in taken), None)

    def mock_modules(self, mock_id: str, route: dict[str, str]) -> dict[str, list[str]]:
        """Question ids of the four modules a student took, keyed rw_m1, rw_m2, math_m1, math_m2."""
        mock = self.mocks[mock_id]
        return {
            "rw_m1": mock["rw"]["m1"],
            "rw_m2": mock["rw"][f"m2_{route['rw']}"],
            "math_m1": mock["math"]["m1"],
            "math_m2": mock["math"][f"m2_{route['math']}"],
        }


content = Content()
