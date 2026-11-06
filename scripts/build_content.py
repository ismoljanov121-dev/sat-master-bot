"""
Builds everything the Mini App and the API read from webapp/data/.

SAT mocks are assembled from data/sat_question_bank.json by the official blueprint. Each section has a
routing module and two second modules. The two second modules share a medium-difficulty core, because a
student only ever sees one of them.

Center-only exams go to data/sealed_exams.json instead. That folder is not served, so their keys stay on
the server and a group exam can run without the answers being one request away.

Usage: python scripts/build_content.py
"""
import json
import random
import sys
from collections import Counter
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "scripts"))
OUT_DIR = BASE_DIR / "webapp" / "data"
SEALED_FILE = BASE_DIR / "data" / "sealed_exams.json"
MOCK_COUNT = 5
SEALED_MOCKS = {5}
SEALED_READING = {4}

RW = "rw"
MATH = "m"
CS, II = "Craft and Structure", "Information and Ideas"
SEC, EOI = "Standard English Conventions", "Expression of Ideas"
ALG, ADV = "Algebra", "Advanced Math"
PSDA, GEO = "Problem-Solving and Data Analysis", "Geometry and Trigonometry"
RW_DOMAIN_ORDER = [CS, II, SEC, EOI]

# Questions per module by domain. These follow the official share of each domain.
QUOTAS = {
    RW: {
        "m1": {CS: 8, II: 7, SEC: 7, EOI: 5},
        "core": {CS: 4, II: 3, SEC: 2, EOI: 2},
        "hard": {CS: 4, II: 4, SEC: 5, EOI: 3},
        "easy": {CS: 4, II: 4, SEC: 5, EOI: 3},
    },
    MATH: {
        "m1": {ALG: 8, ADV: 8, PSDA: 3, GEO: 3},
        "core": {ALG: 3, ADV: 3, PSDA: 1, GEO: 1},
        "hard": {ALG: 5, ADV: 5, PSDA: 2, GEO: 2},
        "easy": {ALG: 5, ADV: 5, PSDA: 2, GEO: 2},
    },
}

# Preferred difficulty order for each bucket, with the share of each level.
MIX = {
    "m1": {"Easy": 0.3, "Medium": 0.4, "Hard": 0.3},
    "core": {"Medium": 1.0},
    "hard": {"Hard": 0.8, "Medium": 0.2},
    "easy": {"Easy": 0.75, "Medium": 0.25},
}
FALLBACK = {"Easy": ["Medium", "Hard"], "Medium": ["Easy", "Hard"], "Hard": ["Medium", "Easy"]}
DIFFICULTY_RANK = {"Easy": 0, "Medium": 1, "Hard": 2}
SPR_SHARE = 0.25


def split_counts(total: int, mix: dict[str, float]) -> dict[str, int]:
    counts = {level: int(total * share) for level, share in mix.items()}
    order = sorted(mix, key=lambda level: total * mix[level] - counts[level], reverse=True)
    for level in order[: total - sum(counts.values())]:
        counts[level] += 1
    return counts


class Assembler:
    def __init__(self, bank: list[dict]):
        rng = random.Random(1600)
        shuffled = [q for q in bank if q.get("mock", True)]
        rng.shuffle(shuffled)
        self.pool = shuffled
        self.used: set[str] = set()

    def pick(self, section: str, domain: str, level: str, chosen: list[dict]) -> dict | None:
        candidates = [
            q for q in self.pool
            if q["sec"] == section and q["dom"] == domain and q["dif"] == level and q["id"] not in self.used
        ]
        if not candidates:
            return None
        skills = Counter(q["skill"] for q in chosen)
        spr_count = sum(q["type"] == "spr" for q in chosen)
        figure_count = sum("fig" in q for q in chosen)
        want_spr = section == MATH and spr_count < SPR_SHARE * (len(chosen) + 1)

        def rank(q: dict) -> tuple:
            return (
                0 if (q["type"] == "spr") == want_spr or section == RW else 1,
                0 if "fig" in q and figure_count < 2 else 1,
                skills[q["skill"]],
            )

        best = min(candidates, key=rank)
        self.used.add(best["id"])
        chosen.append(best)
        return best

    def fill(self, section: str, name: str, modules: list[list[dict]]) -> None:
        """Takes turns between mocks, so scarce questions spread evenly instead of landing in the first one."""
        for domain, count in QUOTAS[section][name].items():
            for level, need in split_counts(count, MIX[name]).items():
                for _ in range(need):
                    for chosen in modules:
                        levels = [level, *FALLBACK[level]]
                        if not any(self.pick(section, domain, option, chosen) for option in levels):
                            raise SystemExit(f"Not enough {domain} questions for {name}")


def order_module(section: str, questions: list[dict]) -> list[str]:
    if section == MATH:
        ranked = sorted(questions, key=lambda q: DIFFICULTY_RANK[q["dif"]])
    else:
        def rank(q: dict) -> tuple:
            domain = RW_DOMAIN_ORDER.index(q["dom"])
            skill = "" if q["dom"] == SEC else q["skill"]
            return domain, skill, DIFFICULTY_RANK[q["dif"]]
        ranked = sorted(questions, key=rank)
    return [q["id"] for q in ranked]


def build_mocks(bank: list[dict]) -> list[dict]:
    assembler = Assembler(bank)
    buckets: dict[tuple[int, str, str], list[dict]] = {}
    # Scarce levels go first: the hard and easy modules decide what is left for the routing module.
    for name in ("hard", "easy", "m1", "core"):
        for section in (MATH, RW):
            modules = [[] for _ in range(MOCK_COUNT)]
            assembler.fill(section, name, modules)
            for mock, chosen in enumerate(modules, start=1):
                buckets[mock, section, name] = chosen

    mocks = []
    for mock in range(1, MOCK_COUNT + 1):
        entry = {"id": f"sat_mock_{mock}", "num": mock, "title": f"Digital SAT Mock {mock}"}
        for section, key in ((RW, "rw"), (MATH, "math")):
            core = buckets[mock, section, "core"]
            entry[key] = {
                "m1": order_module(section, buckets[mock, section, "m1"]),
                "m2_hard": order_module(section, core + buckets[mock, section, "hard"]),
                "m2_easy": order_module(section, core + buckets[mock, section, "easy"]),
            }
        mocks.append(entry)
    return mocks


def build_ielts() -> dict:
    from generate_ielts_data import get_ielts_listening_tests, get_ielts_reading_tests

    listening = get_ielts_listening_tests()
    reading = get_ielts_reading_tests()
    manifest_file = BASE_DIR / "webapp" / "audio" / "manifest.json"
    if manifest_file.exists():
        manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
        for test in listening:
            if str(test["num"]) in manifest:
                test["audio"] = manifest[str(test["num"])]
    extra_file = BASE_DIR / "data" / "ielts_reading_full.json"
    if extra_file.exists():
        reading.extend(json.loads(extra_file.read_text(encoding="utf-8")))
    writing = json.loads((BASE_DIR / "data" / "ielts_writing.json").read_text(encoding="utf-8"))
    visuals = json.loads((BASE_DIR / "data" / "ielts_task1_visuals.json").read_text(encoding="utf-8"))
    for prompt in writing["task1"]:
        prompt["visual"] = visuals[prompt["id"]]
    return {"listening": listening, "reading": reading, "writing": writing}


def write_json(name: str, value) -> None:
    path = OUT_DIR / name
    path.write_text(json.dumps(value, ensure_ascii=False, separators=(",", ":")), encoding="utf-8", newline="\n")
    print(f"{name}: {path.stat().st_size // 1024} KB")


def mock_question_ids(mock: dict) -> set[str]:
    return {qid for part in ("rw", "math") for ids in mock[part].values() for qid in ids}


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    bank = [
        *json.loads((BASE_DIR / "data" / "sat_question_bank.json").read_text(encoding="utf-8")),
        *json.loads((BASE_DIR / "data" / "sat_math_practice.json").read_text(encoding="utf-8")),
    ]
    mocks = build_mocks(bank)
    in_mocks = {qid for mock in mocks for qid in mock_question_ids(mock)}
    sealed_ids = {qid for mock in mocks if mock["num"] in SEALED_MOCKS for qid in mock_question_ids(mock)}

    questions, notes, sealed_questions, sealed_notes = [], {}, [], {}
    for q in bank:
        note = {"exp": q["exp"], "strat": q["strat"]}
        item = {k: v for k, v in q.items() if k not in ("exp", "strat", "mock") and v not in ("", None)}
        if q["id"] in sealed_ids:
            sealed_questions.append(item)
            sealed_notes[q["id"]] = note
            continue
        if q["id"] not in in_mocks:
            item["free"] = 1
        questions.append(item)
        notes[q["id"]] = note

    write_json("sat_bank.json", questions)
    write_json("sat_notes.json", notes)
    write_json("sat_mocks.json", [mock for mock in mocks if mock["num"] not in SEALED_MOCKS])
    ielts = build_ielts()
    write_json("ielts.json", {
        "listening": ielts["listening"],
        "reading": [test for test in ielts["reading"] if test["num"] not in SEALED_READING],
    })
    write_json("ielts_writing.json", ielts["writing"])
    SEALED_FILE.write_text(json.dumps({
        "mocks": [mock for mock in mocks if mock["num"] in SEALED_MOCKS],
        "questions": sealed_questions, "notes": sealed_notes,
        "reading": [test for test in ielts["reading"] if test["num"] in SEALED_READING],
    }, ensure_ascii=False, separators=(",", ":")), encoding="utf-8", newline="\n")
    print(f"{len(bank)} questions: {len(in_mocks)} in mocks ({len(sealed_ids)} of them sealed), "
          f"{len(bank) - len(in_mocks)} for practice only")


if __name__ == "__main__":
    main()
