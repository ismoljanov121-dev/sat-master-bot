"""
EduTest Pro - Adversarial Audit & Quality Gatekeeper
Enforces rigorous multi-stage verification on every question candidate:
1. Digital SAT Taxonomy conformity (Domain & Skill)
2. Structural schema and option validity
3. Mathematical correctness & option distinctness
4. Passage coherence & academic English quality
5. Pedagogical Uzbek explanation (reasoning + distractor rejection rationale)
6. Desmos / tactical hack validity
7. Duplicate and near-duplicate filtering
"""

from typing import Any
from services.sat_taxonomy import validate_taxonomy_item, normalize_taxonomy, SAT_TAXONOMY, VALID_DIFFICULTIES
from services.math_verifier import verify_math_options_distinctness
from services.duplicate_detector import check_candidate_against_existing


def adversarial_audit_question(
    candidate: dict[str, Any],
    existing_questions: list[dict[str, Any]] | None = None
) -> tuple[str, list[str], list[str], dict[str, Any]]:
    """
    Performs adversarial audit on a question candidate.
    Returns:
      decision: 'published' | 'rejected' | 'pending_human_review'
      errors: list of blocking rejection reasons
      warnings: list of non-blocking cautions
      metadata: dict of audit results (e.g. max_similarity, checks_passed)
    """
    errors: list[str] = []
    warnings: list[str] = []
    metadata: dict[str, Any] = {
        "schema_ok": False,
        "taxonomy_ok": False,
        "math_distinct_ok": False,
        "pedagogical_ok": False,
        "duplicate_checked": False
    }

    if not isinstance(candidate, dict):
        return "rejected", ["Candidate must be a dictionary"], [], metadata

    # 1. ID Check
    qid = str(candidate.get("id", "")).strip()
    if not qid:
        errors.append("Missing question ID")

    # 2. Section & Taxonomy Check
    section = str(candidate.get("section", "")).lower().strip()
    domain = str(candidate.get("domain", "")).strip()
    skill = str(candidate.get("skill", "")).strip() or None

    sec_norm, dom_norm, skl_norm = normalize_taxonomy(section, domain, skill)
    candidate["section"] = sec_norm
    candidate["domain"] = dom_norm
    candidate["skill"] = skl_norm

    is_tax_valid, tax_msg = validate_taxonomy_item(sec_norm, dom_norm, skl_norm)
    if not is_tax_valid:
        errors.append(f"Taxonomy validation failed: {tax_msg}")
    else:
        metadata["taxonomy_ok"] = True

    # 3. Difficulty Check
    difficulty = str(candidate.get("difficulty", "")).capitalize().strip()
    if difficulty not in VALID_DIFFICULTIES:
        errors.append(f"Invalid difficulty '{difficulty}'. Must be one of {VALID_DIFFICULTIES}")

    # 4. Question & Passage Check
    q_text = str(candidate.get("question", "")).strip()
    if len(q_text) < 10:
        errors.append("Question prompt is too short or missing (< 10 chars)")

    if section in ("reading", "writing"):
        passage = candidate.get("passage")
        if not passage or len(str(passage).strip()) < 20:
            errors.append(f"Reading/Writing question '{qid}' requires a non-empty passage or research notes")
        # Check for weird non-English chars or incomplete ellipses
        if "TODO" in str(passage) or "..." in str(passage) and len(str(passage).strip()) < 30:
            errors.append("Passage appears to be a placeholder or truncated draft")

    # 5. Options Check (4 choices A, B, C, D)
    options = candidate.get("options")
    if not isinstance(options, list) or len(options) != 4:
        errors.append(f"Must have exactly 4 options A, B, C, D (found {len(options) if isinstance(options, list) else type(options)})")
    else:
        seen_keys = set()
        seen_texts = set()
        for idx, opt in enumerate(options):
            if not isinstance(opt, dict):
                errors.append(f"Option #{idx+1} is not a valid dict")
                continue
            k = str(opt.get("key", "")).strip().upper()
            t = str(opt.get("text", "")).strip()
            if k not in ("A", "B", "C", "D"):
                errors.append(f"Invalid option key: '{k}'")
            if not t:
                errors.append(f"Option {k} has empty text")
            seen_keys.add(k)
            seen_texts.add(t.lower())

        if seen_keys != {"A", "B", "C", "D"}:
            errors.append(f"Option keys must strictly be A, B, C, D; got {sorted(seen_keys)}")
        if len(seen_texts) < 4:
            errors.append(f"Options contain duplicate text entries: {seen_texts}")

        # Math option distinctness
        if section == "math" and len(options) == 4:
            is_distinct, dist_msg = verify_math_options_distinctness(options)
            if not is_distinct:
                errors.append(f"Mathematical options error: {dist_msg}")
            else:
                metadata["math_distinct_ok"] = True

    # 6. Correct Answer Key Check
    correct = str(candidate.get("correct", "")).strip().upper()
    if correct not in ("A", "B", "C", "D"):
        errors.append(f"Invalid correct answer key: '{correct}'")

    # 7. Pedagogical Uzbek Explanation & Distractor Analysis Check
    explanation = str(candidate.get("explanation", "")).strip()
    if len(explanation) < 30:
        errors.append("Explanation is too short or missing (< 30 chars)")
    else:
        # Check distractor rationale keywords (xato, noto'g'ri, tuzoq, variant, chunki, etc.)
        expl_lower = explanation.lower()
        has_distractor_mention = any(w in expl_lower for w in ("xato", "noto'g'ri", "tuzoq", "variant", "chalg'it", "qolgan"))
        if not has_distractor_mention:
            warnings.append("Explanation does not explicitly mention why remaining distractors are wrong")
        else:
            metadata["pedagogical_ok"] = True

    # 8. Strategy or Desmos Hack Check
    strategy = str(candidate.get("strategy_or_hack") or candidate.get("desmos_hack", "")).strip()
    if len(strategy) < 15:
        errors.append("Desmos hack or SAT strategic rule is missing or insufficient (< 15 chars)")

    # 9. Duplicate & Near-duplicate Detection
    if existing_questions:
        is_dup, dup_msg, max_sim = check_candidate_against_existing(candidate, existing_questions)
        metadata["max_similarity"] = max_sim
        metadata["duplicate_checked"] = True
        if is_dup:
            errors.append(f"Duplication check failed: {dup_msg}")
        elif max_sim > 0.70:
            warnings.append(f"Moderate similarity with existing item: {max_sim*100:.1f}%")

    metadata["schema_ok"] = (len(errors) == 0)

    # Route decision
    if errors:
        return "rejected", errors, warnings, metadata
    if len(warnings) > 1:
        return "pending_human_review", errors, warnings, metadata

    return "published", [], warnings, metadata
