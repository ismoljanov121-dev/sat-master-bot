"""
Unit tests for Question Vault, Math Verifier, Duplicate Detector, and Adversarial Audit.
"""

import os
import unittest
from services.question_repository import QuestionRepository
from services.math_verifier import verify_math_options_distinctness, verify_single_correct_choice
from services.duplicate_detector import check_candidate_against_existing, compute_jaccard_similarity
from services.adversarial_audit import adversarial_audit_question


class TestQuestionEngineVault(unittest.TestCase):
    def setUp(self):
        self.test_db_path = os.path.join(os.path.dirname(__file__), "test_vault.db")
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
        self.repo = QuestionRepository(db_path=self.test_db_path)
        self.repo._initialized = True

    def tearDown(self):
        if hasattr(self.repo, "_local") and hasattr(self.repo._local, "conn") and self.repo._local.conn:
            self.repo._local.conn.close()
            self.repo._local.conn = None
        if os.path.exists(self.test_db_path):
            try:
                os.remove(self.test_db_path)
            except Exception:
                pass

    def test_vault_lifecycle_and_filtering(self):
        """Vault must store lifecycle states and only return published questions to public queries."""
        q_pub = {
            "id": "q_pub_01",
            "section": "math",
            "domain": "Algebra",
            "skill": "Linear equations in one variable",
            "difficulty": "Easy",
            "question": "If 3x + 9 = 24, what is x?",
            "options": [{"key": "A", "text": "5"}, {"key": "B", "text": "6"}, {"key": "C", "text": "7"}, {"key": "D", "text": "8"}],
            "correct": "A",
            "explanation": "3x = 15 => x = 5. B, C, D are wrong calculations.",
            "strategy_or_hack": "Direct algebra"
        }
        q_draft = {
            "id": "q_draft_01",
            "section": "math",
            "domain": "Algebra",
            "skill": "Linear equations in one variable",
            "difficulty": "Easy",
            "question": "Draft question prompt...",
            "options": [{"key": "A", "text": "1"}, {"key": "B", "text": "2"}, {"key": "C", "text": "3"}, {"key": "D", "text": "4"}],
            "correct": "A",
            "explanation": "Draft explanation.",
            "strategy_or_hack": "Draft hack"
        }

        ok1, msg1 = self.repo.upsert_question(q_pub, status="published")
        self.assertTrue(ok1, msg1)

        ok2, msg2 = self.repo.upsert_question(q_draft, status="draft")
        self.assertTrue(ok2, msg2)

        # Public query must only return published items
        published = self.repo.get_published_questions()
        self.assertEqual(len(published), 1)
        self.assertEqual(published[0]["id"], "q_pub_01")

        # Status counts must track both accurately
        counts = self.repo.get_counts_by_status()
        self.assertEqual(counts["published"], 1)
        self.assertEqual(counts["draft"], 1)

    def test_duplicate_stem_hash_rejection(self):
        """Vault must block questions with exact duplicate stems."""
        q1 = {
            "id": "q1",
            "section": "math",
            "domain": "Algebra",
            "skill": "Linear equations",
            "difficulty": "Easy",
            "question": "What is the value of x when x + 2 = 10?",
            "options": [{"key": "A", "text": "8"}, {"key": "B", "text": "10"}, {"key": "C", "text": "12"}, {"key": "D", "text": "14"}],
            "correct": "A",
            "explanation": "x = 8. Other options are wrong.",
            "strategy_or_hack": "Direct solve"
        }
        q2 = dict(q1)
        q2["id"] = "q2_different_id" # Different ID but same prompt

        ok1, _ = self.repo.upsert_question(q1, status="published")
        self.assertTrue(ok1)

        ok2, msg2 = self.repo.upsert_question(q2, status="published")
        self.assertFalse(ok2)
        self.assertIn("Duplicate", msg2)

    def test_math_verifier_identical_options(self):
        """Math verifier must catch identical or equivalent options like 2/4 and 0.5."""
        opts_dup = [
            {"key": "A", "text": "2/4"},
            {"key": "B", "text": "0.5"},
            {"key": "C", "text": "3"},
            {"key": "D", "text": "4"}
        ]
        ok, msg = verify_math_options_distinctness(opts_dup)
        self.assertFalse(ok)
        self.assertTrue("mathematically equivalent" in msg or "identical" in msg)

        opts_clean = [
            {"key": "A", "text": "1/2"},
            {"key": "B", "text": "3/4"},
            {"key": "C", "text": "1"},
            {"key": "D", "text": "2"}
        ]
        ok_clean, _ = verify_math_options_distinctness(opts_clean)
        self.assertTrue(ok_clean)

    def test_duplicate_detector_near_duplicate(self):
        """Duplicate detector must catch near-duplicate stems."""
        existing = [{
            "id": "e1",
            "passage": None,
            "question": "A car travels at a speed of 60 miles per hour on the highway for 3 hours."
        }]
        candidate_near = {
            "id": "c1",
            "passage": None,
            "question": "A car travels at a speed of 70 miles per hour on the highway for 4 hours."
        }
        is_dup, msg, sim = check_candidate_against_existing(candidate_near, existing, similarity_threshold=0.75)
        self.assertTrue(is_dup)
        self.assertGreaterEqual(sim, 0.75)

    def test_adversarial_audit_clean_and_rejected(self):
        """Adversarial audit must pass clean questions and reject flawed ones."""
        good_q = {
            "id": "test_good_01",
            "section": "math",
            "domain": "Algebra",
            "skill": "Linear equations in one variable",
            "difficulty": "Easy",
            "passage": None,
            "question": "If 5x - 10 = 25, what is the value of x?",
            "options": [
                {"key": "A", "text": "7"},
                {"key": "B", "text": "5"},
                {"key": "C", "text": "3"},
                {"key": "D", "text": "10"}
            ],
            "correct": "A",
            "explanation": "5x = 35 => x = 7. B (5) xato chunki 5*5-10=15. C va D ham noto'g'ri hisob-kitob tuzoqlaridir.",
            "strategy_or_hack": "⚡ DESMOS HACK: 1-qator: y = 5x - 10; 2-qator: y = 25. Kesishish x = 7."
        }
        decision, errs, warns, meta = adversarial_audit_question(good_q)
        self.assertEqual(decision, "published", f"Errors: {errs}")

        bad_q = dict(good_q)
        bad_q["id"] = "test_bad_01"
        bad_q["options"] = [{"key": "A", "text": "7"}, {"key": "B", "text": "5"}] # Only 2 options
        decision_bad, errs_bad, _, _ = adversarial_audit_question(bad_q)
        self.assertEqual(decision_bad, "rejected")
        self.assertTrue(any("4 options" in e for e in errs_bad))


if __name__ == "__main__":
    unittest.main()
