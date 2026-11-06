import unittest
from fractions import Fraction

from services import scoring
from services.auth_service import validate_telegram_init_data
from tests.helpers import init_data
from config import BOT_TOKEN


class GridInTest(unittest.TestCase):
    def test_numbers(self):
        self.assertEqual(scoring.parse_number("-2.5"), Fraction(-5, 2))
        self.assertEqual(scoring.parse_number(".75"), Fraction(3, 4))
        self.assertEqual(scoring.parse_number("6/8"), Fraction(3, 4))
        self.assertIsNone(scoring.parse_number("abc"))
        self.assertIsNone(scoring.parse_number("1/0"))
        self.assertIsNone(scoring.parse_number(""))

    def test_equivalent_forms_are_accepted(self):
        question = {"type": "spr", "ans": ["2/3"]}
        for answer in ("2/3", "4/6", ".6667", "0.667"):
            self.assertTrue(scoring.sat_answer_correct(question, answer), answer)
        for answer in ("0.66", "1", "", None):
            self.assertFalse(scoring.sat_answer_correct(question, answer), answer)

    def test_multiple_choice(self):
        question = {"type": "mcq", "cor": "B"}
        self.assertTrue(scoring.sat_answer_correct(question, "B"))
        self.assertFalse(scoring.sat_answer_correct(question, "A"))


class ScoreModelTest(unittest.TestCase):
    def items(self, correct_share: float, difficulty: str = "Medium", count: int = 54):
        right = int(count * correct_share)
        return [(difficulty, "mcq", index < right) for index in range(count)]

    def test_more_correct_answers_never_lower_the_score(self):
        scores = [scoring.section_score(self.items(share))["score"] for share in (0, 0.25, 0.5, 0.75, 1)]
        self.assertEqual(scores, sorted(scores))
        self.assertGreaterEqual(scores[-1], 750)
        self.assertLessEqual(scores[0], 280)

    def test_hard_questions_count_for_more(self):
        easy = scoring.section_score(self.items(0.7, "Easy"))["score"]
        hard = scoring.section_score(self.items(0.7, "Hard"))["score"]
        self.assertGreater(hard, easy + 100)

    def test_range_contains_the_score_and_stays_on_the_scale(self):
        for share in (0, 0.5, 1):
            result = scoring.section_score(self.items(share))
            self.assertLessEqual(result["low"], result["score"])
            self.assertGreaterEqual(result["high"], result["score"])
            self.assertGreaterEqual(result["low"], 200)
            self.assertLessEqual(result["high"], 800)

    def test_total_range(self):
        section = {"score": 600, "low": 570, "high": 630, "spread": 30}
        total = scoring.total_score(section, section)
        self.assertEqual(total["score"], 1200)
        self.assertLess(total["low"], 1200)
        self.assertGreater(total["high"], 1200)

    def test_routing(self):
        self.assertEqual(scoring.route_for(15, 27), "hard")
        self.assertEqual(scoring.route_for(14, 27), "easy")


class IeltsTest(unittest.TestCase):
    def test_answer_normalizing(self):
        question = {"ans": "the 15th September", "alts": ["September 15"]}
        self.assertTrue(scoring.ielts_answer_correct({"ans": "library"}, " The Library. "))
        self.assertTrue(scoring.ielts_answer_correct(question, "september 15"))
        self.assertFalse(scoring.ielts_answer_correct({"ans": "library"}, ""))

    def test_bands(self):
        self.assertEqual(scoring.ielts_band(40, scoring.READING_BANDS), 9)
        self.assertEqual(scoring.ielts_band(30, scoring.READING_BANDS), 7)
        self.assertEqual(scoring.ielts_band(0, scoring.LISTENING_BANDS), 0)


class InitDataTest(unittest.TestCase):
    def test_valid_data(self):
        valid, user, _ = validate_telegram_init_data(init_data(42, "Ali"), BOT_TOKEN)
        self.assertTrue(valid)
        self.assertEqual(user["id"], 42)

    def test_wrong_token_is_rejected(self):
        self.assertFalse(validate_telegram_init_data(init_data(42, token="999:OTHER"), BOT_TOKEN)[0])

    def test_tampering_is_rejected(self):
        tampered = init_data(42).replace("42", "43")
        self.assertFalse(validate_telegram_init_data(tampered, BOT_TOKEN)[0])

    def test_old_data_is_rejected(self):
        self.assertFalse(validate_telegram_init_data(init_data(42, age_seconds=90000), BOT_TOKEN)[0])
