import unittest
import json
import os

from services.question_validator import validate_question, audit_question_collection
from services.question_service import qs
from handlers.practice import get_user_filters, set_user_filter, reset_user_filters
from database import db


class TestQuestionBankAudit(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.bank_file = os.path.join(self.base_dir, "data", "sat_question_bank.json")
        self.diag_file = os.path.join(self.base_dir, "data", "questions.json")

    def test_all_bank_questions_pass_strict_validation(self):
        """Every question in the active question bank must strictly pass 6-stage validation."""
        with open(self.bank_file, "r", encoding="utf-8") as f:
            bank = json.load(f)

        audit_res = audit_question_collection(bank)
        self.assertEqual(audit_res["rejected_count"], 0, f"Rejected bank questions: {audit_res['rejected']}")
        self.assertEqual(audit_res["imported_count"], len(bank))
        self.assertGreaterEqual(audit_res["imported_count"], 70)

    def test_all_diagnostic_questions_pass_validation(self):
        """Diagnostic questions must also pass validation when normalized."""
        with open(self.diag_file, "r", encoding="utf-8") as f:
            diag = json.load(f)

        normalized = []
        for q in diag:
            normalized.append({
                "id": f"diag_{q.get('id')}",
                "section": "math",
                "domain": q.get("topic", "Math - General"),
                "difficulty": "Medium",
                "passage": None,
                "question": q.get("question"),
                "options": q.get("options"),
                "correct": q.get("correct"),
                "explanation": q.get("explanation"),
                "strategy_or_hack": q.get("desmos_hack")
            })

        audit_res = audit_question_collection(normalized)
        self.assertEqual(audit_res["rejected_count"], 0)
        self.assertEqual(audit_res["imported_count"], 7)

    def test_validator_rejects_malformed_questions(self):
        """Validator must catch and reject malformed or incomplete questions."""
        # 1. Missing option
        bad_q1 = {
            "id": "bad_1",
            "section": "math",
            "domain": "Algebra",
            "difficulty": "Easy",
            "question": "What is 2 + 2?",
            "options": [{"key": "A", "text": "4"}, {"key": "B", "text": "5"}],
            "correct": "A",
            "explanation": "2 + 2 = 4.",
            "strategy_or_hack": "Mental math"
        }
        ok1, errs1 = validate_question(bad_q1)
        self.assertFalse(ok1)
        self.assertTrue(any("4 options" in e for e in errs1))

        # 2. Duplicate options
        bad_q2 = {
            "id": "bad_2",
            "section": "math",
            "domain": "Algebra",
            "difficulty": "Easy",
            "question": "Solve for x: x = 5",
            "options": [
                {"key": "A", "text": "5"},
                {"key": "B", "text": "5"},
                {"key": "C", "text": "6"},
                {"key": "D", "text": "7"}
            ],
            "correct": "A",
            "explanation": "Clearly x = 5.",
            "strategy_or_hack": "Direct solution"
        }
        ok2, errs2 = validate_question(bad_q2)
        self.assertFalse(ok2)
        self.assertTrue(any("Duplicate option texts" in e for e in errs2))

        # 3. Invalid correct key
        bad_q3 = {
            "id": "bad_3",
            "section": "math",
            "domain": "Algebra",
            "difficulty": "Easy",
            "question": "What is x when 2x = 8?",
            "options": [
                {"key": "A", "text": "1"},
                {"key": "B", "text": "2"},
                {"key": "C", "text": "3"},
                {"key": "D", "text": "4"}
            ],
            "correct": "E",
            "explanation": "8 / 2 = 4.",
            "strategy_or_hack": "Division"
        }
        ok3, errs3 = validate_question(bad_q3)
        self.assertFalse(ok3)
        self.assertTrue(any("Invalid correct key" in e for e in errs3))

    def test_question_service_filtering(self):
        """QuestionService must accurately filter by section, difficulty, and domain."""
        qs.reload()
        
        # Section counts
        counts = qs.get_questions_count_by_section()
        self.assertGreaterEqual(counts["math"], 28)
        self.assertGreaterEqual(counts["reading"], 19)
        self.assertGreaterEqual(counts["writing"], 21)

        # Filter by difficulty
        hard_qs = qs.filter_questions(difficulty="Hard")
        self.assertTrue(all(str(q.get("difficulty")).capitalize() == "Hard" for q in hard_qs))
        self.assertGreaterEqual(len(hard_qs), 30)

        easy_qs = qs.filter_questions(difficulty="Easy")
        self.assertTrue(all(str(q.get("difficulty")).capitalize() == "Easy" for q in easy_qs))
        self.assertGreaterEqual(len(easy_qs), 8)

        # Filter by section and difficulty
        hard_math = qs.filter_questions(section="math", difficulty="Hard")
        self.assertTrue(all(q.get("section") == "math" and str(q.get("difficulty")).capitalize() == "Hard" for q in hard_math))

        # Filter by domain keyword
        algebra_qs = qs.filter_questions(section="math", domain="algebra")
        self.assertTrue(all("algebra" in str(q.get("domain")).lower() for q in algebra_qs))
        self.assertGreater(len(algebra_qs), 0)

    def test_user_filter_state_persistence(self):
        """User practice filters must persist in cache and be resettable."""
        test_uid = 999111888
        reset_user_filters(test_uid)

        f = get_user_filters(test_uid)
        self.assertEqual(f["section"], "mixed")
        self.assertEqual(f["difficulty"], "all")
        self.assertEqual(f["domain"], "all")

        set_user_filter(test_uid, "section", "math")
        set_user_filter(test_uid, "difficulty", "hard")
        set_user_filter(test_uid, "domain", "Geometry")

        f2 = get_user_filters(test_uid)
        self.assertEqual(f2["section"], "math")
        self.assertEqual(f2["difficulty"], "hard")
        self.assertEqual(f2["domain"], "Geometry")

        reset_user_filters(test_uid)
        f3 = get_user_filters(test_uid)
        self.assertEqual(f3["section"], "mixed")
        self.assertEqual(f3["difficulty"], "all")


if __name__ == "__main__":
    unittest.main()
