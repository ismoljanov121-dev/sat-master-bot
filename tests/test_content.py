import json
import sys
import unittest
from collections import Counter
from pathlib import Path

from services.content import SAT_DOMAINS, content
from services.scoring import parse_number

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "scripts"))

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


class PracticeBankTest(unittest.TestCase):
    def test_the_file_matches_the_generator_and_every_check_passes(self):
        import generate_math_practice

        stored = json.loads((BASE_DIR / "data" / "sat_math_practice.json").read_text(encoding="utf-8"))
        self.assertEqual(generate_math_practice.build(), stored)

    def test_generated_questions_are_practice_only(self):
        generated = [q for q in content.bank.values() if q["id"].startswith("g_")]
        self.assertGreaterEqual(len(generated), 200)
        for question in generated:
            self.assertTrue(question.get("free"), question["id"])
            self.assertNotIn(question["id"], content.mock_of)

    def test_every_math_skill_of_the_two_big_domains_has_practice_questions(self):
        practice = Counter(q["skill"] for q in content.bank.values() if q.get("free") and q["dom"] in ("Algebra", "Advanced Math"))
        for skill in ("Linear equations in one variable", "Linear equations in two variables", "Linear functions",
                      "Linear inequalities in one or two variables", "Systems of two linear equations in two variables",
                      "Equivalent expressions", "Nonlinear equations and systems", "Nonlinear functions"):
            self.assertGreaterEqual(practice[skill], 15, skill)


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


TASK1_KINDS = {
    "Line Graph": {"line"}, "Bar Chart": {"bar"}, "Pie Chart": {"pie"}, "Table": {"table"}, "Process": {"flow"}, "Map": {"map"},
    "Multiple Graphs": {"bar", "line"},
}


class Task1VisualTest(unittest.TestCase):
    def parts(self):
        for prompt in content.writing["task1"]:
            for part in prompt["visual"]["parts"]:
                yield prompt["id"], part

    def test_every_prompt_shows_the_kind_of_visual_it_names(self):
        for prompt in content.writing["task1"]:
            with self.subTest(prompt=prompt["id"]):
                self.assertEqual({part["kind"] for part in prompt["visual"]["parts"]}, TASK1_KINDS[prompt["type"]])

    def test_task_2_has_no_visual(self):
        self.assertFalse(any("visual" in prompt for prompt in content.writing["task2"]))

    def test_every_part_has_a_title(self):
        for prompt_id, part in self.parts():
            self.assertTrue(part["title"].strip(), prompt_id)

    def test_series_match_their_axis(self):
        for prompt_id, part in self.parts():
            if part["kind"] in ("line", "bar"):
                labels = part["x"] if part["kind"] == "line" else part["categories"]
                for series in part["series"]:
                    self.assertEqual(len(series["values"]), len(labels), f"{prompt_id} {series['name']}")
                self.assertLessEqual(len(part["series"]), 5, prompt_id)

    def test_pie_charts_add_up_to_one_hundred_and_keep_the_same_order(self):
        for prompt in content.writing["task1"]:
            pies = [part for part in prompt["visual"]["parts"] if part["kind"] == "pie"]
            for pie in pies:
                self.assertEqual(sum(item["value"] for item in pie["slices"]), 100, pie["title"])
                self.assertLessEqual(len(pie["slices"]), 5, pie["title"])
            orders = {tuple(item["name"] for item in pie["slices"]) for pie in pies}
            self.assertLessEqual(len(orders), 2, prompt["id"])

    def test_tables_are_rectangular(self):
        for prompt_id, part in self.parts():
            if part["kind"] == "table":
                self.assertTrue(all(len(row) == len(part["head"]) for row in part["rows"]), prompt_id)

    def test_maps_describe_their_facts_for_the_ai(self):
        for prompt_id, part in self.parts():
            if part["kind"] == "map":
                self.assertGreater(len(part["facts"]), 80, prompt_id)
                self.assertTrue(part["items"], prompt_id)

    def test_key_figures_in_the_guides_match_the_data(self):
        def pie(prompt_id, index):
            part = content.writing_by_id[prompt_id]["visual"]["parts"][index]
            return {item["name"]: item["value"] for item in part["slices"]}

        self.assertEqual((pie("w1_03", 0)["Technology"], pie("w1_03", 1)["Technology"]), (3, 18))
        self.assertEqual((pie("w1_12", 0)["Coal"], pie("w1_12", 1)["Coal"]), (42, 26))
        self.assertEqual(pie("w1_19", 2)["Drip"], 22)
