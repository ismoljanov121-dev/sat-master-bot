"""
EduTest Pro - Duplicate & Similarity Detector
Prevents trivial rewording, number-swapping, and near-duplicate stems using
n-gram token analysis and Levenshtein/SequenceMatcher ratios.
"""

import difflib
import re
from typing import Any


def tokenize_stem(text: str) -> list[str]:
    """Extracts normalized words from text, stripping punctuation."""
    cleaned = re.sub(r"[^a-zA-Z0-9\s]", " ", text.lower())
    return [w for w in cleaned.split() if len(w) > 1]


def get_ngrams(tokens: list[str], n: int = 2) -> set[tuple[str, ...]]:
    """Generates word n-grams from a list of tokens."""
    if len(tokens) < n:
        return set()
    return set(tuple(tokens[i:i+n]) for i in range(len(tokens) - n + 1))


def compute_jaccard_similarity(text1: str, text2: str, n: int = 2) -> float:
    """Computes n-gram Jaccard similarity between two texts."""
    t1 = tokenize_stem(text1)
    t2 = tokenize_stem(text2)
    ng1 = get_ngrams(t1, n)
    ng2 = get_ngrams(t2, n)
    if not ng1 or not ng2:
        return 0.0
    intersection = len(ng1.intersection(ng2))
    union = len(ng1.union(ng2))
    return intersection / union if union > 0 else 0.0


def compute_text_similarity_ratio(text1: str, text2: str) -> float:
    """Computes SequenceMatcher ratio between two normalized texts."""
    s1 = " ".join(tokenize_stem(text1))
    s2 = " ".join(tokenize_stem(text2))
    if not s1 or not s2:
        return 0.0
    return difflib.SequenceMatcher(None, s1, s2).ratio()


def check_candidate_against_existing(
    candidate: dict[str, Any],
    existing_questions: list[dict[str, Any]],
    similarity_threshold: float = 0.82
) -> tuple[bool, str, float]:
    """
    Checks candidate question against a collection of existing questions.
    Returns: (is_duplicate_or_near_duplicate, message, max_similarity)
    """
    c_passage = str(candidate.get("passage") or "").strip()
    c_prompt = str(candidate.get("question", "")).strip()
    c_stem = (c_passage + " " + c_prompt).strip()

    max_sim = 0.0
    most_similar_id = None

    for existing in existing_questions:
        if str(existing.get("id")) == str(candidate.get("id")):
            continue

        e_passage = str(existing.get("passage") or "").strip()
        e_prompt = str(existing.get("question", "")).strip()
        e_stem = (e_passage + " " + e_prompt).strip()

        # 1. Exact match
        if c_stem.lower() == e_stem.lower():
            return True, f"Exact duplicate of question '{existing.get('id')}'", 1.0

        # 2. SequenceMatcher similarity
        sim_ratio = compute_text_similarity_ratio(c_stem, e_stem)
        # 3. Jaccard bigram similarity
        jaccard_sim = compute_jaccard_similarity(c_stem, e_stem, n=2)

        combined_sim = max(sim_ratio, jaccard_sim)
        if combined_sim > max_sim:
            max_sim = combined_sim
            most_similar_id = existing.get("id")

        if combined_sim >= similarity_threshold:
            return (
                True,
                f"Near-duplicate detected with question '{existing.get('id')}' (Similarity: {combined_sim*100:.1f}%)",
                combined_sim
            )

    return False, f"Unique question (Max similarity: {max_sim*100:.1f}% with '{most_similar_id}')", max_sim
