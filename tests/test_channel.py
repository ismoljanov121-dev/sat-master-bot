"""The channel bank and the daily slots: every post fits Telegram, quizzes have one clear answer, nothing runs out."""

import collections
import importlib.util
import json
import re
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from aiogram.exceptions import TelegramRetryAfter

from services import channel
from tests.helpers import DatabaseTestCase

ROOT = Path(__file__).resolve().parent.parent
ALLOWED_TAGS = {"b", "i", "code"}


def load_math_generator():
    spec = importlib.util.spec_from_file_location("generate_channel_math", ROOT / "scripts" / "generate_channel_math.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def html_problems(text: str) -> list[str]:
    """Telegram rejects unknown tags, unbalanced tags and bare < > &."""
    problems, stack = [], []
    for match in re.finditer(r"<(/?)([a-z]+)>", text):
        closing, tag = match.groups()
        if tag not in ALLOWED_TAGS:
            problems.append(f"tag <{tag}>")
        elif closing:
            if not stack or stack.pop() != tag:
                problems.append(f"unbalanced </{tag}>")
        else:
            stack.append(tag)
    if stack:
        problems.append(f"unclosed {stack}")
    bare = re.sub(r"</?(b|i|code)>", "", text)
    bare = re.sub(r"&(lt|gt|amp|quot);", "", bare)
    problems += [f"bare {ch!r}" for ch in "<>&" if ch in bare]
    return problems


class ChannelBankTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pools = channel.pools()

    def test_ten_posts_a_day_in_four_slots(self):
        self.assertEqual(len(channel.SLOTS), 4)
        self.assertEqual(sum(len(kinds) for _, _, kinds in channel.SLOTS), 10)
        self.assertEqual(set(channel.KINDS), set(self.pools))

    def test_no_kind_repeats_within_four_months(self):
        per_day = collections.Counter(channel.KINDS)
        for kind, pool in self.pools.items():
            with self.subTest(kind=kind):
                self.assertGreaterEqual(len(pool) / per_day[kind], 120, f"{kind} has {len(pool)} posts")

    def test_no_item_is_lost_to_an_id_clash(self):
        load = channel._load
        sat, ielts, phrases = load("sat_words"), load("ielts_words"), load("phrases")
        expected = {
            "sat_word": len(sat), "ielts_word": len(ielts), "phrase": len(phrases),
            "tip": len(channel.IELTS_TIPS) + len(load("tips")),
            "sat_quiz": len(channel.channel_quiz_candidates()) + len(load("sat_quizzes")),
            "ielts_quiz": len(phrases) + len(load("ielts_quizzes")),
            "math": len(load("sat_math")), "speaking": len(load("speaking")),
            "extra": len(load("facts")) + len(channel.IELTS_VOCAB_PACKS)
            + len(channel.family_posts(sat, "SAT")) + len(channel.topic_packs(ielts)),
            "word_quiz": sum(len(channel.word_quizzes(w, sat, "SAT")) for w in sat)
            + sum(len(channel.word_quizzes(w, ielts, "IELTS")) for w in ielts),
        }
        self.assertEqual({kind: len(pool) for kind, pool in self.pools.items()}, expected)

    def test_bank_holds_thousands_of_posts(self):
        self.assertGreaterEqual(sum(len(pool) for pool in self.pools.values()), 3000)

    def test_polls_fit_telegram_limits(self):
        for kind, pool in self.pools.items():
            for item_id, post in pool.items():
                if not post.poll:
                    continue
                poll = post.poll
                with self.subTest(kind=kind, item=item_id):
                    self.assertLessEqual(channel.tg_len(poll.question), channel.POLL_QUESTION_LIMIT)
                    self.assertTrue(2 <= len(poll.options) <= 10)
                    self.assertTrue(all(1 <= channel.tg_len(o) <= channel.POLL_OPTION_LIMIT for o in poll.options))
                    self.assertEqual(len({o.strip().lower() for o in poll.options}), len(poll.options), poll.options)
                    self.assertTrue(0 <= poll.correct < len(poll.options))
                    self.assertLessEqual(channel.tg_len(poll.explanation), channel.POLL_EXPLANATION_LIMIT)
                    self.assertLessEqual(poll.explanation.count("\n"), 2)

    def test_messages_are_valid_telegram_html(self):
        for kind, pool in self.pools.items():
            for item_id, post in pool.items():
                if not post.text:
                    continue
                with self.subTest(kind=kind, item=item_id):
                    self.assertEqual(html_problems(post.text), [])
                    self.assertLessEqual(channel.tg_len(post.text + channel.FOOTER), channel.MESSAGE_LIMIT)

    def test_word_and_phrase_banks_are_complete(self):
        for prefix, required in (("sat_words", ("w", "pos", "g", "uz", "en", "ex")),
                                 ("ielts_words", ("w", "pos", "g", "uz", "en", "ex", "topic")),
                                 ("phrases", ("w", "t", "g", "uz", "en", "ex"))):
            bank = channel._load(prefix)
            heads = [item["w"].lower() for item in bank]
            with self.subTest(bank=prefix):
                self.assertEqual([w for w, n in collections.Counter(heads).items() if n > 1], [])
                for item in bank:
                    self.assertTrue(all(item.get(field) for field in required), item.get("w"))
                    for near in item.get("near", []):
                        self.assertIn(near.lower(), heads, f"{item['w']} lists unknown near word {near}")
        sat = {w["w"].lower() for w in channel._load("sat_words")}
        ielts = {w["w"].lower() for w in channel._load("ielts_words")}
        self.assertEqual(sat & ielts, set())

    def test_wrong_options_never_share_a_meaning(self):
        for prefix in ("sat_words", "ielts_words", "phrases"):
            bank = channel._load(prefix)
            for item in bank:
                wrong = channel.distractors(item, bank, f"check:{item['w']}")
                with self.subTest(bank=prefix, word=item["w"]):
                    self.assertEqual(len(wrong), 3)
                    for other in wrong:
                        self.assertNotEqual(other["g"], item["g"])
                        self.assertFalse(channel._related(item, other))

    def test_every_word_has_its_quizzes(self):
        for prefix, exam in (("sat_words", "SAT"), ("ielts_words", "IELTS")):
            bank = channel._load(prefix)
            for word in bank:
                with self.subTest(word=word["w"]):
                    self.assertEqual(len(channel.word_quizzes(word, bank, exam)), 3 if word.get("syn") else 2)

    def test_written_quizzes_have_one_answer_in_varied_places(self):
        for prefix in ("sat_quizzes", "ielts_quizzes"):
            items = channel._load(prefix)
            positions = collections.Counter()
            for item in items:
                with self.subTest(bank=prefix, question=item["q"][:40]):
                    self.assertEqual(len(item["o"]), 4)
                    self.assertEqual(len(set(item["o"])), 4)
                    self.assertTrue(0 <= item["a"] < 4)
                post = channel.quiz_post(item, "x", "x")
                self.assertEqual(post.poll.options[post.poll.correct], item["o"][item["a"]])
                positions[post.poll.correct] += 1
            self.assertEqual(len(positions), 4, f"{prefix} answers sit in {dict(positions)}")

    def test_math_file_is_exactly_what_the_generator_builds(self):
        generator = load_math_generator()
        stored = json.loads((channel.DATA_DIR / "sat_math.json").read_text(encoding="utf-8"))
        self.assertEqual(stored, generator.build())

    def test_math_answers_are_the_computed_ones(self):
        generator = load_math_generator()
        self.assertEqual(generator.poly(2, -3, 1), "2x² - 3x + 1")
        self.assertEqual(generator.poly(1, 0, -9), "x² - 9")
        self.assertEqual(generator.poly(-1, 1), "-x + 1")
        self.assertEqual(generator.fmt(12345), "12,345")
        self.assertEqual(generator.fmt(generator.Fraction(6, 4)), "3/2")

    def test_older_tips_are_labelled_with_their_own_exam(self):
        self.assertEqual(channel.legacy_tip_exam("SAT Math: Grid-in Qoidalari"), "SAT")
        self.assertEqual(channel.legacy_tip_exam("Reading: Matching Headings"), "IELTS")
        self.assertEqual(channel.legacy_tip_exam("Kunlik Odat"), "SAT va IELTS")
        header = channel.tip_post({"exam": "SAT", "title": "SAT Math: Grid-in Qoidalari", "body": "x"}).text.split("\n")[0]
        self.assertEqual(header, "💡 <b>SAT Math: Grid-in Qoidalari</b>")
        for post in self.pools["tip"].values():
            self.assertNotIn("IELTS maslahati: SAT", post.text)

    def test_speaking_prompts_are_complete(self):
        items = channel._load("speaking")
        parts = collections.Counter(item["part"] for item in items)
        self.assertGreaterEqual(min(parts.values()), 30)
        for item in items:
            with self.subTest(question=item["q"][:40]):
                self.assertIn(item["part"], channel.SPEAKING_TIMING)
                self.assertGreaterEqual(len(item["ph"]), 2)
                if item["part"] == 2:
                    self.assertEqual(len(item["cue"]), 4)


class ChannelPostingTest(DatabaseTestCase):
    def fake_bot(self, **overrides):
        return SimpleNamespace(send_message=AsyncMock(), send_poll=AsyncMock(), **overrides)

    async def test_a_day_of_slots_makes_ten_posts(self):
        bot = self.fake_bot()
        with patch.object(channel, "POST_GAP_SECONDS", 0):
            sent = [await channel.post_slot(bot, slot) for slot in range(len(channel.SLOTS))]
        self.assertEqual(sent, [len(kinds) for _, _, kinds in channel.SLOTS])
        self.assertGreaterEqual(bot.send_poll.await_count, 4)
        for call in bot.send_poll.await_args_list:
            self.assertEqual(call.kwargs["question_parse_mode"], "HTML")
            self.assertTrue(call.kwargs["is_anonymous"])

    async def test_poll_text_is_escaped_for_html(self):
        bot = self.fake_bot()
        post = channel.Post(source="math", poll=channel.Poll("If x < 5 & y > 2", ("1", "2"), 0, "a < b"))
        await channel.deliver(bot, post)
        kwargs = bot.send_poll.await_args.kwargs
        self.assertEqual(kwargs["question"], "If x &lt; 5 &amp; y &gt; 2")
        self.assertEqual(kwargs["explanation"], "a &lt; b")
        self.assertEqual(kwargs["options"], ["1", "2"])

    async def test_one_failed_post_does_not_stop_the_slot(self):
        bot = self.fake_bot()
        bot.send_message.side_effect = [RuntimeError("telegram down"), None, None, None]
        with patch.object(channel, "POST_GAP_SECONDS", 0):
            sent = await channel.post_slot(bot, 0)
        self.assertEqual(sent, len(channel.SLOTS[0][2]) - 1)

    async def test_flood_limit_waits_and_retries(self):
        bot = self.fake_bot()
        error = TelegramRetryAfter(method=SimpleNamespace(), message="Flood control", retry_after=1)
        bot.send_message.side_effect = [error, None]
        with patch.object(channel.asyncio, "sleep", AsyncMock()) as sleep:
            await channel.deliver(bot, channel.Post(source="tip", text="hello"))
        sleep.assert_awaited_once_with(2)
        self.assertEqual(bot.send_message.await_count, 2)

    async def test_channel_keeps_posting_when_the_database_is_down(self):
        bot = self.fake_bot()
        with patch.object(channel.db, "fetch", AsyncMock(side_effect=ConnectionError("db down"))), \
                patch.object(channel, "POST_GAP_SECONDS", 0):
            sent = await channel.post_slot(bot, 3)
        self.assertEqual(sent, len(channel.SLOTS[3][2]))

    async def test_kinds_cycle_through_their_whole_pool(self):
        items = sorted(channel.pools()["speaking"])
        picked = [await channel.next_item("speaking", items) for _ in items]
        self.assertEqual(sorted(picked), items)
