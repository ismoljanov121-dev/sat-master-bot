"""
Read-only access to the built content in webapp/data/. The API grades against these same files.
"""

import json
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).resolve().parent.parent / "webapp" / "data"

SAT_DOMAINS = {
    "rw": ["Craft and Structure", "Information and Ideas", "Standard English Conventions", "Expression of Ideas"],
    "m": ["Algebra", "Advanced Math", "Problem-Solving and Data Analysis", "Geometry and Trigonometry"],
}


def _load(name: str) -> Any:
    return json.loads((DATA_DIR / name).read_text(encoding="utf-8"))


class Content:
    def __init__(self) -> None:
        self.bank: dict[str, dict[str, Any]] = {q["id"]: q for q in _load("sat_bank.json")}
        self.notes: dict[str, dict[str, str]] = _load("sat_notes.json")
        self.mocks: dict[str, dict[str, Any]] = {m["id"]: m for m in _load("sat_mocks.json")}
        ielts = _load("ielts.json")
        self.listening: dict[int, dict[str, Any]] = {t["num"]: t for t in ielts["listening"]}
        self.reading: dict[int, dict[str, Any]] = {t["num"]: t for t in ielts["reading"]}
        self.writing: dict[str, list[dict[str, Any]]] = _load("ielts_writing.json")
        self.writing_by_id = {w["id"]: w for items in self.writing.values() for w in items}

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
