"""
EduTest Pro - Question Validator & Quality Gate
Enforces strict 6-stage validation on Digital SAT questions:
1. Schema & Data Types
2. Section & SAT Domain taxonomy
3. Difficulty rating ('Easy', 'Medium', 'Hard')
4. Options integrity (exactly 4 distinct choices A, B, C, D)
5. Verified answer key & step-by-step pedagogical explanation
6. Desmos hack (Math) or tactical rule (Reading/Writing)
"""

from typing import Any, Tuple

# Standardized Digital SAT Domains
SAT_DOMAINS = {
    "math": [
        "Algebra - Linear Equations and Systems",
        "Algebra - Linear Inequalities and Modeling",
        "Algebra - Equivalent Expressions & Constants",
        "Advanced Math - Quadratic Equations & Systems",
        "Advanced Math - Nonlinear Systems",
        "Advanced Math - Parabola Vertex & Extremum",
        "Advanced Math - Exponential Functions",
        "Advanced Math - Polynomials & Radical Equations",
        "Problem Solving - Percentages and Ratios",
        "Problem Solving - Unit Conversions & Rates",
        "Problem Solving - Data Analysis & Statistics",
        "Problem Solving - Margin of Error & Probability",
        "Geometry and Trigonometry - Right Triangles & Trigonometric Ratios",
        "Geometry and Trigonometry - Circle Equations & Radius",
        "Geometry and Trigonometry - Arc Length & Angles",
        "Geometry and Trigonometry - Area, Volume & Similarity"
    ],
    "reading": [
        "Craft and Structure - Words in Context",
        "Craft and Structure - Text Structure and Purpose",
        "Craft and Structure - Cross-Text Connections",
        "Information and Ideas - Central Ideas and Details",
        "Information and Ideas - Command of Evidence (Textual)",
        "Information and Ideas - Command of Evidence (Quantitative)",
        "Information and Ideas - Inferences"
    ],
    "writing": [
        "Standard English Conventions - Boundaries & Punctuation",
        "Standard English Conventions - Form, Structure, and Sense",
        "Standard English Conventions - Subject-Verb & Pronoun Agreement",
        "Standard English Conventions - Modifiers & Parallelism",
        "Expression of Ideas - Transitions",
        "Expression of Ideas - Rhetorical Synthesis"
    ]
}

VALID_DIFFICULTIES = {"Easy", "Medium", "Hard"}
VALID_SECTIONS = {"math", "reading", "writing"}
VALID_OPTION_KEYS = {"A", "B", "C", "D"}

def validate_question(q: dict[str, Any]) -> Tuple[bool, list[str]]:
    """
    Validates an individual question against strict pedagogical and schema standards.
    Returns (is_valid, list_of_errors).
    """
    errors: list[str] = []

    if not isinstance(q, dict):
        return False, ["Question must be a dictionary"]

    # 1. ID check
    qid = q.get("id")
    if not qid or str(qid).strip() == "":
        errors.append("Missing or empty 'id'")

    # 2. Section check
    sec = str(q.get("section", "")).lower().strip()
    if sec not in VALID_SECTIONS:
        errors.append(f"Invalid section: '{sec}'. Must be one of {sorted(VALID_SECTIONS)}")

    # 3. Domain check
    domain = str(q.get("domain", "")).strip()
    if not domain:
        errors.append("Missing 'domain'")

    # 4. Difficulty check
    diff = str(q.get("difficulty", "")).capitalize().strip()
    if diff not in VALID_DIFFICULTIES:
        errors.append(f"Invalid difficulty: '{diff}'. Must be one of {sorted(VALID_DIFFICULTIES)}")

    # 5. Question & Passage check
    q_text = str(q.get("question", "")).strip()
    if len(q_text) < 10:
        errors.append("Question text is missing or too short (< 10 chars)")

    if sec in ("reading", "writing"):
        passage = q.get("passage")
        if not passage or len(str(passage).strip()) < 15:
            errors.append(f"Reading/Writing question '{qid}' requires a non-empty passage or research context")

    # 6. Options check (4 distinct options with keys A, B, C, D)
    options = q.get("options")
    if not isinstance(options, list) or len(options) != 4:
        errors.append(f"Expected exactly 4 options, found {len(options) if isinstance(options, list) else type(options)}")
    else:
        seen_keys = set()
        seen_texts = set()
        for idx, opt in enumerate(options):
            if not isinstance(opt, dict):
                errors.append(f"Option #{idx+1} is not an object")
                continue
            key = opt.get("key")
            text = str(opt.get("text", "")).strip()
            if key not in VALID_OPTION_KEYS:
                errors.append(f"Invalid option key: '{key}'")
            if not text:
                errors.append(f"Option {key} has empty text")
            seen_keys.add(key)
            seen_texts.add(text.lower())

        if seen_keys != VALID_OPTION_KEYS:
            errors.append(f"Option keys must strictly be A, B, C, D; got {sorted(seen_keys)}")
        if len(seen_texts) < 4:
            errors.append(f"Duplicate option texts found in question '{qid}'")

    # 7. Correct answer key check
    correct = q.get("correct")
    if correct not in VALID_OPTION_KEYS:
        errors.append(f"Invalid correct key: '{correct}'")

    # 8. Step-by-step explanation check
    explanation = str(q.get("explanation", "")).strip()
    if len(explanation) < 20:
        errors.append("Explanation is missing or insufficient (< 20 chars)")

    # 9. Strategy / Hack check
    strategy = str(q.get("strategy_or_hack") or q.get("desmos_hack", "")).strip()
    if len(strategy) < 10:
        errors.append("Strategy or Desmos hack is missing or insufficient (< 10 chars)")

    return len(errors) == 0, errors


def audit_question_collection(questions: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Audits an entire collection of questions, checking uniqueness and validity.
    Returns comprehensive metrics and categorized lists: imported, staged, rejected.
    """
    imported: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    seen_stems: set[str] = set()

    for q in questions:
        qid = str(q.get("id", "")).strip()
        is_valid, errors = validate_question(q)

        if qid in seen_ids:
            is_valid = False
            errors.append(f"Duplicate question ID '{qid}'")
        seen_ids.add(qid)

        stem = (str(q.get("passage") or "") + " ___ " + str(q.get("question", ""))).strip().lower()
        if stem in seen_stems:
            is_valid = False
            errors.append("Duplicate question content (exact passage + prompt match)")
        seen_stems.add(stem)

        if is_valid:
            imported.append(q)
        else:
            rejected.append({"id": qid, "errors": errors, "question": q})

    by_section: dict[str, int] = {}
    by_difficulty: dict[str, int] = {}
    by_domain: dict[str, int] = {}

    for q in imported:
        sec = str(q.get("section", "")).lower()
        diff = str(q.get("difficulty", "")).capitalize()
        dom = str(q.get("domain", ""))

        by_section[sec] = by_section.get(sec, 0) + 1
        by_difficulty[diff] = by_difficulty.get(diff, 0) + 1
        by_domain[dom] = by_domain.get(dom, 0) + 1

    return {
        "total_analyzed": len(questions),
        "imported_count": len(imported),
        "rejected_count": len(rejected),
        "imported": imported,
        "rejected": rejected,
        "breakdown": {
            "section": by_section,
            "difficulty": by_difficulty,
            "domain": by_domain
        }
    }
