"""
SAT Master AI - Question Service Engine
Manages authentic Digital SAT Question Bank (Reading, Writing, Math)
and provides endless dynamic SAT Math generation for infinite practice.
"""

import json
import logging
import os
import random
from typing import Any, Tuple

logger = logging.getLogger("QuestionService")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CURATED_BANK_FILE = os.path.join(BASE_DIR, "data", "sat_question_bank.json")
DIAGNOSTIC_BANK_FILE = os.path.join(BASE_DIR, "data", "questions.json")

class QuestionService:
    def __init__(self):
        self.curated_questions: list[dict[str, Any]] = []
        self._load_bank()

    def _load_bank(self):
        """Loads curated SAT questions from disk."""
        questions: list[dict[str, Any]] = []
        
        # Load main question bank if available
        if os.path.exists(CURATED_BANK_FILE):
            try:
                with open(CURATED_BANK_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        questions.extend(data)
                        logger.info(f"Loaded {len(data)} questions from sat_question_bank.json")
            except Exception as e:
                logger.error(f"Error loading sat_question_bank.json: {e}")

        # Load diagnostic questions as additional math practice
        if os.path.exists(DIAGNOSTIC_BANK_FILE):
            try:
                with open(DIAGNOSTIC_BANK_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        for q in data:
                            q_copy = dict(q)
                            q_copy["id"] = f"diag_{q.get('id')}"
                            q_copy["section"] = "math"
                            q_copy["difficulty"] = "Medium"
                            q_copy["strategy_or_hack"] = q.get("desmos_hack", "")
                            # Avoid duplicates
                            if not any(item.get("id") == q_copy["id"] for item in questions):
                                questions.append(q_copy)
            except Exception as e:
                logger.error(f"Error loading questions.json: {e}")

        self.curated_questions = questions

    def reload(self):
        """Reloads the bank from disk."""
        self._load_bank()

    def get_question_by_id(self, qid: str) -> dict[str, Any] | None:
        """Finds a question by its unique ID."""
        for q in self.curated_questions:
            if str(q.get("id")) == str(qid):
                return q
        return None

    def get_questions_by_section(self, section: str) -> list[dict[str, Any]]:
        """Filters questions by section: 'reading', 'writing', 'math'."""
        sec = section.lower().strip()
        return [q for q in self.curated_questions if q.get("section", "").lower() == sec]

    def get_questions_count_by_section(self) -> dict[str, int]:
        """Returns question count per section."""
        counts = {"math": 0, "reading": 0, "writing": 0}
        for q in self.curated_questions:
            sec = str(q.get("section", "")).lower().strip()
            if sec in counts:
                counts[sec] += 1
        return counts

    @staticmethod
    def validate_question_schema(q: dict[str, Any]) -> Tuple[bool, str]:
        """
        Validates individual question against schema:
        - unique ID
        - section in ('math', 'reading', 'writing')
        - non-empty question
        - exactly 4 options with keys A, B, C, D
        - valid correct key
        - non-empty explanation
        """
        if not isinstance(q, dict):
            return False, "Question is not a dict"
        if not q.get("id"):
            return False, "Missing id"
        if q.get("section") not in ("math", "reading", "writing"):
            return False, f"Invalid section: {q.get('section')}"
        if not q.get("question"):
            return False, "Missing question text"
        options = q.get("options", [])
        if not isinstance(options, list) or len(options) != 4:
            return False, f"Expected 4 options, got {len(options) if isinstance(options, list) else 'non-list'}"
        keys = [opt.get("key") for opt in options if isinstance(opt, dict)]
        if set(keys) != {"A", "B", "C", "D"}:
            return False, f"Option keys must be A, B, C, D; got {keys}"
        if q.get("correct") not in ("A", "B", "C", "D"):
            return False, f"Invalid correct key: {q.get('correct')}"
        if not q.get("explanation"):
            return False, "Missing explanation"
        return True, "Valid"


    def get_next_question(self, answered_ids: list[str], section: str = "mixed") -> dict[str, Any]:
        """
        Selects the next question for practice.
        If all curated questions in this section have been answered,
        or for endless math, dynamically generates infinite authentic SAT questions!
        """
        sec = section.lower().strip()
        answered_set = set(str(qid) for qid in answered_ids)

        # 1. Filter candidates from curated bank
        if sec == "mixed":
            pool = self.curated_questions
        else:
            pool = [q for q in self.curated_questions if q.get("section", "").lower() == sec]

        unanswered = [q for q in pool if str(q.get("id")) not in answered_set]

        # 2. If there are unanswered curated questions, pick one randomly
        if unanswered:
            return random.choice(unanswered)

        # 3. If pool is empty or all answered:
        # If user is in math or mixed mode, generate a dynamic infinite question!
        if sec in ("math", "mixed") or not pool:
            return self.generate_dynamic_sat_question()

        # If reading or writing pool exhausted, recycle pool with random choice
        return random.choice(pool)

    def generate_dynamic_sat_question(self) -> dict[str, Any]:
        """
        Generates infinite, authentic Digital SAT Math questions algorithmically
        covering top College Board tested templates with verified answers and Desmos hacks.
        """
        generator_choice = random.choice([1, 2, 3, 4, 5])
        
        if generator_choice == 1:
            # Linear System with No Solution (Parallel lines: A1/A2 = B1/B2 != C1/C2)
            A = random.choice([2, 3, 5, 7])
            B = random.choice([3, 4, 6])
            mult = random.choice([2, 3, 4])
            A2 = A * mult
            B2 = B * mult
            C1 = random.randint(5, 20)
            C2 = C1 * mult + random.randint(1, 5) # ensures no solution
            
            question_text = (
                f"Tenglamalar sistemasi berilgan:\n\n"
                f"{A}x + {B}y = {C1}\n"
                f"kx + {B2}y = {C2}\n\n"
                f"Agar berilgan tenglamalar sistemasi yechimga ega bo'lmasa (no solution), k o'zgarmas sonining qiymati nechaga teng?"
            )
            correct_val = A2
            options_values = [correct_val, correct_val - 2, correct_val + mult, correct_val * 2]
            random.shuffle(options_values)
            correct_key = ["A", "B", "C", "D"][options_values.index(correct_val)]
            
            return {
                "id": f"dyn_lin_sys_{random.randint(1000, 9999)}",
                "section": "math",
                "domain": "Algebra - Systems of Linear Equations (No Solution)",
                "difficulty": "Medium",
                "passage": None,
                "question": question_text,
                "options": [
                    {"key": "A", "text": str(options_values[0])},
                    {"key": "B", "text": str(options_values[1])},
                    {"key": "C", "text": str(options_values[2])},
                    {"key": "D", "text": str(options_values[3])}
                ],
                "correct": correct_key,
                "explanation": (
                    f"Chiziqli tenglamalar sistemasi yechimga ega bo'lmasligi (parallel to'g'ri chiziqlar) uchun "
                    f"x va y oldidagi koeffitsiyentlar nisbati teng bo'lishi shart: A₁/A₂ = B₁/B₂ ≠ C₁/C₂.\n"
                    f"Demak: {A}/k = {B}/{B2} => {A}/k = 1/{mult} => k = {A} * {mult} = {correct_val}."
                ),
                "strategy_or_hack": (
                    f"⚡ DESMOS HACK:\n"
                    f"1. 1-qatorga {A}x + {B}y = {C1} ni yozing.\n"
                    f"2. 2-qatorga kx + {B2}y = {C2} ni yozib, k ga slayder qo'shing.\n"
                    f"3. Variantlardagi qiymatlarni k o'rniga qo'ying: qachonki ikkala to'g'ri chiziq parallel (kesishmaydigan) bo'lsa, o'sha qiymat to'g'ri bo'ladi! k = {correct_val}."
                )
            }

        elif generator_choice == 2:
            # Circle Equation Radius & Center
            h = random.randint(2, 7)
            k = random.randint(2, 7)
            r = random.choice([3, 4, 5, 6, 7, 8])
            r2 = r * r
            F = h * h + k * k - r2
            sign_h = f"- {2*h}x"
            sign_k = f"+ {2*k}y"
            sign_F = f"+ {F}" if F >= 0 else f"- {abs(F)}"
            
            question_text = (
                f"xy-tekisligida quyidagi tenglama aylanani ifodalaydi:\n\n"
                f"x² + y² {sign_h} {sign_k} {sign_F} = 0\n\n"
                f"Ushbu aylananing radiusi nechaga teng?"
            )
            correct_val = r
            opts = [r, r2, 2*r, r + 2]
            random.shuffle(opts)
            correct_key = ["A", "B", "C", "D"][opts.index(correct_val)]
            
            return {
                "id": f"dyn_circle_{random.randint(1000, 9999)}",
                "section": "math",
                "domain": "Geometry and Trigonometry - Circle Equation",
                "difficulty": "Hard",
                "passage": None,
                "question": question_text,
                "options": [
                    {"key": "A", "text": str(opts[0])},
                    {"key": "B", "text": str(opts[1])},
                    {"key": "C", "text": str(opts[2])},
                    {"key": "D", "text": str(opts[3])}
                ],
                "correct": correct_key,
                "explanation": (
                    f"To'la kvadratga ajratamiz:\n"
                    f"(x - {h})² + (y + {k})² = -({sign_F}) + {h*h} + {k*k} = {r2}.\n"
                    f"Aylana tenglamasi: (x - h)² + (y - k)² = R² bo'lgani sababli, R² = {r2} => R = {r}."
                ),
                "strategy_or_hack": (
                    f"⚡ DESMOS HACK (10 SONIYADA):\n"
                    f"1. Tenglamani xuddi o'zidek Desmosga yozing: x^2 + y^2 {sign_h} {sign_k} {sign_F} = 0\n"
                    f"2. Aylana chiziladi! Markazini bosing: ({h}, {-k}).\n"
                    f"3. Aylana chetini bosing va radiusni darhol ko'ring: R = {r}!"
                )
            }

        elif generator_choice == 3:
            # Quadratic Vertex / Maximum or Minimum
            a_val = random.choice([-2, -1, 1, 2])
            h = random.randint(1, 6)
            k = random.randint(5, 30)
            B_coeff = -2 * a_val * h
            C_coeff = a_val * (h ** 2) + k
            sign_b = f"+ {B_coeff}x" if B_coeff >= 0 else f"- {abs(B_coeff)}x"
            sign_c = f"+ {C_coeff}" if C_coeff >= 0 else f"- {abs(C_coeff)}"
            
            extremum_type = "maksimal" if a_val < 0 else "minimal"
            
            question_text = (
                f"Funksiya berilgan: f(x) = {a_val}x² {sign_b} {sign_c}\n\n"
                f"Ushbu funksiyaning {extremum_type} qiymati nechaga teng?"
            )
            correct_val = k
            opts = [k, h, C_coeff, k + 4]
            random.shuffle(opts)
            correct_key = ["A", "B", "C", "D"][opts.index(correct_val)]
            
            return {
                "id": f"dyn_vertex_{random.randint(1000, 9999)}",
                "section": "math",
                "domain": "Advanced Math - Quadratic Functions & Extremum",
                "difficulty": "Medium",
                "passage": None,
                "question": question_text,
                "options": [
                    {"key": "A", "text": str(opts[0])},
                    {"key": "B", "text": str(opts[1])},
                    {"key": "C", "text": str(opts[2])},
                    {"key": "D", "text": str(opts[3])}
                ],
                "correct": correct_key,
                "explanation": (
                    f"Parabolaning uchi (vertex): x = -b / (2a) = -({B_coeff}) / (2 * {a_val}) = {h}.\n"
                    f"Funksiyaning {extremum_type} qiymati f({h}) ga teng: f({h}) = {k}."
                ),
                "strategy_or_hack": (
                    f"⚡ DESMOS HACK (5 SONIYADA):\n"
                    f"1. Desmosga yozing: y = {a_val}x^2 {sign_b} {sign_c}\n"
                    f"2. Sichqoncha yoki barmog'ingiz bilan parabolaning eng cho'qqi nuqtasini bosing.\n"
                    f"3. Ko'rinadi: ({h}, {k}). y qiymati ya'ni {k} — funksiyaning {extremum_type} qiymatidir!"
                )
            }

        elif generator_choice == 4:
            # Equivalent Polynomial Constants
            c1 = random.randint(2, 5)
            c2 = random.randint(2, 6)
            k_val = random.randint(3, 8)
            A_quad = c1 * c2
            B_quad = c2 * k_val - 3 * c1
            C_quad = -3 * k_val
            sign_B = f"+ {B_quad}x" if B_quad >= 0 else f"- {abs(B_quad)}x"
            sign_C = f"+ {C_quad}" if C_quad >= 0 else f"- {abs(C_quad)}"

            question_text = (
                f"Barcha x qiymatlari uchun quyidagi tenglik o'rinli:\n\n"
                f"({c1}x + k)({c2}x - 3) = {A_quad}x² {sign_B} {sign_C}\n\n"
                f"Bunda k o'zgarmas son. k ning qiymati nechaga teng?"
            )
            correct_val = k_val
            opts = [k_val, -k_val, k_val * 2, abs(C_quad)]
            random.shuffle(opts)
            correct_key = ["A", "B", "C", "D"][opts.index(correct_val)]

            return {
                "id": f"dyn_equiv_{random.randint(1000, 9999)}",
                "section": "math",
                "domain": "Algebra - Equivalent Expressions & Constants",
                "difficulty": "Easy",
                "passage": None,
                "question": question_text,
                "options": [
                    {"key": "A", "text": str(opts[0])},
                    {"key": "B", "text": str(opts[1])},
                    {"key": "C", "text": str(opts[2])},
                    {"key": "D", "text": str(opts[3])}
                ],
                "correct": correct_key,
                "explanation": (
                    f"Ozod hadlarni taqqoslaymiz: chap tomonda k * (-3) = -3k.\n"
                    f"O'ng tomonda ozod had: {C_quad}.\n"
                    f"Demak: -3k = {C_quad} => k = {k_val}."
                ),
                "strategy_or_hack": (
                    f"⚡ DESMOS HACK:\n"
                    f"Desmosga ozod hadlar bo'linmasini yozing: {C_quad} / (-3) => darhol {k_val} javobi chiqadi!"
                )
            }

        else:
            # Exponential Growth / Decay
            initial = random.choice([500, 1000, 1500, 2000, 2500])
            rate_pct = random.choice([4, 5, 8, 12, 15])
            factor = 1 + (rate_pct / 100)
            
            question_text = (
                f"Bank hisobvarag'idagi dastlabki summa ${initial} ni tashkil qiladi. "
                f"Hisobdagi pul har yili {rate_pct}% ga doimiy oshib boradi (murakkab foiz). "
                f"Quyidagi funksiyalardan qaysi biri t yildan so'ng hisobdagi umumiy pul miqdori P(t) ni to'g'ri ifodalaydi?"
            )
            correct_opt = f"P(t) = {initial}({factor})^t"
            wrong_1 = f"P(t) = {initial}({rate_pct})^t"
            wrong_2 = f"P(t) = {initial} + {rate_pct}t"
            wrong_3 = f"P(t) = {initial}({1 - rate_pct/100})^t"
            
            opts = [correct_opt, wrong_1, wrong_2, wrong_3]
            random.shuffle(opts)
            correct_key = ["A", "B", "C", "D"][opts.index(correct_opt)]

            return {
                "id": f"dyn_exp_{random.randint(1000, 9999)}",
                "section": "math",
                "domain": "Advanced Math - Exponential Functions",
                "difficulty": "Easy",
                "passage": None,
                "question": question_text,
                "options": [
                    {"key": "A", "text": opts[0]},
                    {"key": "B", "text": opts[1]},
                    {"key": "C", "text": opts[2]},
                    {"key": "D", "text": opts[3]}
                ],
                "correct": correct_key,
                "explanation": (
                    f"Murakkab foiz o'sish formulasi: P(t) = P₀(1 + r)^t.\n"
                    f"P₀ = {initial}, r = {rate_pct}% = {rate_pct/100}.\n"
                    f"Demak asos: 1 + {rate_pct/100} = {factor}. To'g'ri ifoda: P(t) = {initial}({factor})^t."
                ),
                "strategy_or_hack": (
                    f"⚡ SAT STRATEGIYASI:\n"
                    f"{rate_pct}% o'sish degani 100% + {rate_pct}% = {100+rate_pct}% ya'ni {factor} ga ko'paytirish degani! "
                    f"Asos har doim 1 dan katta bo'lishi kerak."
                )
            }

qs = QuestionService()
