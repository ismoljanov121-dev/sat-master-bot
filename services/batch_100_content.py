"""
EduTest Pro - 100 New Original Digital SAT Question Candidates (Batch 100)
- 40 Math (Algebra, Advanced Math, Problem-Solving & Data Analysis, Geometry & Trigonometry)
- 30 Reading (Craft & Structure, Information & Ideas)
- 30 Writing (Standard English Conventions, Expression of Ideas)
"""

from services.batch_100_math import BATCH_100_MATH
from services.batch_100_reading import BATCH_100_READING
from services.batch_100_writing import BATCH_100_WRITING

def _normalize_question(q: dict) -> dict:
    norm = dict(q)
    # Ensure correct answer keys
    ans = str(q.get("correct") or q.get("correct_answer") or "A").upper().strip()
    norm["correct"] = ans
    norm["correct_answer"] = ans
    
    # Ensure options structure
    raw_options = q.get("options", [])
    if raw_options and isinstance(raw_options[0], str):
        keys = ["A", "B", "C", "D", "E"]
        norm["options"] = [{"key": keys[i], "text": str(opt)} for i, opt in enumerate(raw_options)]
    else:
        norm["options"] = raw_options

    # Ensure difficulty capitalization
    diff = str(q.get("difficulty", "Medium")).capitalize()
    norm["difficulty"] = diff

    # Ensure strategy_or_hack
    if not norm.get("strategy_or_hack"):
        sec = norm.get("section", "")
        if sec == "reading":
            norm["strategy_or_hack"] = "⚡ READING STRATEGY: Savol kalit so'zini matndan toping va faqat matn daliliga tayaning, shaxsiy fikr qo'shmang."
        elif sec == "writing":
            norm["strategy_or_hack"] = "⚡ WRITING STRATEGY: Gap chegarasini va ega-kesim moslashuvini aniqlang, eng lo'nda va grammatik to'g'ri variantni tanlang."
        else:
            norm["strategy_or_hack"] = "⚡ MATH STRATEGY: Formulani qo'llang yoki Desmos kalkulyatorida tenglamani chizib yechimni tekshiring."

    norm["author"] = "internal_authoring"
    norm["license"] = "proprietary_original"
    norm["status"] = "published"
    return norm

BATCH_100_DATA = [_normalize_question(q) for q in (BATCH_100_MATH + BATCH_100_READING + BATCH_100_WRITING)]

def get_batch_100():
    return BATCH_100_DATA
