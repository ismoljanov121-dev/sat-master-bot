import unittest
from collections import Counter

from services.content import SAT_DOMAINS, content
from services.scoring import parse_number

RANK = {"Easy": 0, "Medium": 1, "Hard": 2}


class QuestionBankTest(unittest.TestCase):
    def test_every_question_is_complete(self):
        for question in content.bank.values():
            with self.subTest(question=question["id"]):
                self.assertIn(question["dom"], SAT_DOMAINS[question["sec"]])
                self.assertIn(question["dif"], RANK)
                self.assertTrue(question["q"].strip())
                notes = content.notes[question["id"]]
                self.assertTrue(notes["exp"].strip())
                if question["type"] == "mcq":
                    self.assertEqual(len(question["opts"]), 4)
                    self.assertEqual(len(set(question["opts"])), 4)
                    self.assertIn(question["cor"], "ABCD")
                else:
                    self.assertEqual(question["type"], "spr")
                    self.assertIsNotNone(parse_number(question["ans"][0]))

    def test_grid_in_explanations_do_not_mention_answer_letters(self):
        for question in content.bank.values():
            if question["type"] == "spr":
                self.assertNotRegex(content.notes[question["id"]]["exp"], r"To'g'ri javob:\s*[A-D]\b", question["id"])

    def test_answer_letters_are_balanced(self):
        letters = Counter(q["cor"] for q in content.bank.values() if q["type"] == "mcq")
        self.assertLess(max(letters.values()) / min(letters.values()), 1.35)


class MockBlueprintTest(unittest.TestCase):
    def module(self, ids):
        return [content.bank[question_id] for question_id in ids]

    def test_module_sizes_and_domains(self):
        for mock in content.mocks.values():
            for key, size, quota in (
                ("rw", 27, {"Craft and Structure": 8, "Information and Ideas": 7,
                            "Standard English Conventions": 7, "Expression of Ideas": 5}),
                ("math", 22, {"Algebra": 8, "Advanced Math": 8, "Problem-Solving and Data Analysis": 3,
                              "Geometry and Trigonometry": 3}),
            ):
                for name, ids in mock[key].items():
                    with self.subTest(mock=mock["id"], section=key, module=name):
                        self.assertEqual(len(ids), size)
                        self.assertEqual(len(set(ids)), size)
                        self.assertEqual(dict(Counter(q["dom"] for q in self.module(ids))), quota)

    def test_no_question_appears_in_two_mocks(self):
        seen = {}
        for mock in content.mocks.values():
            ids = {qid for key in ("rw", "math") for module in mock[key].values() for qid in module}
            for question_id in ids:
                self.assertNotIn(question_id, seen, f"{question_id} is in {seen.get(question_id)} and {mock['id']}")
                seen[question_id] = mock["id"]

    def test_routing_a_student_changes_difficulty(self):
        def mean(ids):
            return sum(RANK[q["dif"]] for q in self.module(ids)) / len(ids)

        for mock in content.mocks.values():
            for key in ("rw", "math"):
                self.assertGreater(mean(mock[key]["m2_hard"]), mean(mock[key]["m1"]))
                self.assertLess(mean(mock[key]["m2_easy"]), mean(mock[key]["m1"]))

    def test_mocks_are_comparable(self):
        means = [
            sum(RANK[q["dif"]] for q in self.module(mock["math"]["m1"])) / 22 for mock in content.mocks.values()
        ]
        self.assertLess(max(means) - min(means), 0.2)

    def test_math_modules_run_from_easy_to_hard(self):
        for mock in content.mocks.values():
            for ids in mock["math"].values():
                ranks = [RANK[q["dif"]] for q in self.module(ids)]
                self.assertEqual(ranks, sorted(ranks))

    def test_reading_modules_follow_the_official_domain_order(self):
        order = SAT_DOMAINS["rw"]
        for mock in content.mocks.values():
            for ids in mock["rw"].values():
                positions = [order.index(q["dom"]) for q in self.module(ids)]
                self.assertEqual(positions, sorted(positions))

    def test_math_has_grid_in_questions_near_the_official_share(self):
        for mock in content.mocks.values():
            for ids in mock["math"].values():
                share = sum(q["type"] == "spr" for q in self.module(ids)) / len(ids)
                self.assertGreaterEqual(share, 0.18)
                self.assertLessEqual(share, 0.4)


class IeltsContentTest(unittest.TestCase):
    def test_tests_have_forty_numbered_questions(self):
        for test in [*content.listening.values(), *content.reading.values()]:
            with self.subTest(test=test["title"]):
                numbers = [question["num"] for question in test["questions"]]
                self.assertEqual(numbers, list(range(1, 41)))
                for question in test["questions"]:
                    self.assertTrue(str(question["ans"]).strip())

    def test_writing_bank(self):
        self.assertEqual(len(content.writing["task1"]), 23)
        self.assertEqual(len(content.writing["task2"]), 23)
        self.assertEqual(len(content.writing_by_id), 46)
