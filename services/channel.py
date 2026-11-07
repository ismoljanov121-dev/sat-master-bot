"""
Channel posts: ten a day in four slots, about SAT and IELTS, drawn from the static bank in data/channel/.

Every kind of post keeps its own cycle in channel_log, so an item comes back only after its whole pool has
been posted. When the database cannot be reached, the pick falls back to a fixed draw for the day, so the
channel keeps posting.
"""

import asyncio
import hashlib
import html
import json
import logging
import random
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Optional

from aiogram.exceptions import TelegramRetryAfter
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import BOT_USERNAME, CHANNEL_ID
from content_bank import IELTS_TIPS, IELTS_VOCAB_PACKS
from database import db, now_ts, today
from services.content import content

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "channel"

POLL_QUESTION_LIMIT = 300
POLL_OPTION_LIMIT = 100
POLL_EXPLANATION_LIMIT = 200
MESSAGE_LIMIT = 4096
PASSAGE_LIMIT = 900
POST_GAP_SECONDS = 3.0
FAMILY_SIZE = 8
FOOTER = f"\n\n━━━━━━━━━━━━━━━━━━━━\n🤖 <b>Bepul IELTS va SAT mashq testlari:</b> @{BOT_USERNAME}"

# Tashkent time: three posts in the morning, two at lunch, three after classes and two at night.
SLOTS: tuple[tuple[int, int, tuple[str, ...]], ...] = (
    (8, 0, ("sat_word", "ielts_word", "tip")),
    (13, 0, ("sat_quiz", "word_quiz")),
    (18, 0, ("math", "phrase", "ielts_quiz")),
    (21, 0, ("speaking", "extra")),
)
KINDS = tuple(kind for _, _, kinds in SLOTS for kind in kinds)

POS = {"v": ("verb", "fe'l"), "n": ("noun", "ot"), "adj": ("adjective", "sifat"), "adv": ("adverb", "ravish")}
PHRASE_TYPES = {
    "idiom": ("Idioma", "💬 Speaking'da tabiiy chiqadi. Writing'da idiomadan qoching."),
    "phrasal": ("Phrasal verb", "💬 Speaking uchun qulay. Writing'da rasmiyroq muqobilini tanlang."),
    "collocation": ("Kollokatsiya", "✍️ Writing'da ham, Speaking'da ham bemalol ishlating."),
}
SPEAKING_TIMING = {
    1: "⏱ 20–30 soniyada, 2–3 gap bilan javob bering: fikr, sabab, misol.",
    2: "⏱ 1 daqiqa tayyorlaning, keyin 2 daqiqa to'xtamay gapiring. Ovozingizni yozib, qayta tinglang.",
    3: "⏱ 40–60 soniyada fikringizni sabab va misol bilan asoslang, ikki tomonni ham ko'rsating.",
}
# Words too common in Uzbek glosses to show that two meanings are close.
_STOPWORDS = {
    "qilmoq", "bo'lmoq", "etmoq", "bermoq", "olmoq", "qilish", "bo'lish", "qiluvchi", "bo'lgan", "qilingan",
    "narsa", "narsani", "holat", "holati", "kishi", "odam", "odamni", "uchun", "bilan", "juda", "biror", "yoki",
    "emas", "qattiq", "kuchli", "yaxshi", "yomon", "tomon", "tomonidan", "ko'proq", "ortiqcha", "o'zini", "boshqa",
    "barcha", "hamma", "orqali", "keyin", "oldin", "vaqtda", "vaqtinchalik", "birga", "qismi", "ishni", "ishlar",
}

_PLAIN_SYMBOLS = (
    (r"\cdot", "·"), (r"\le", "≤"), (r"\ge", "≥"), (r"\ne", "≠"), (r"\pm", "±"), (r"\pi", "π"), (r"\theta", "θ"),
    (r"\times", "×"), (r"\div", "÷"), (r"\left", ""), (r"\right", ""), ("^{2}", "²"), ("^{3}", "³"), (r"^{\circ}", "°"),
)


@dataclass(frozen=True)
class Poll:
    question: str
    options: tuple[str, ...]
    correct: int
    explanation: str = ""


@dataclass(frozen=True)
class Post:
    source: str  # deep-link tag on the button, so the admin funnel shows which posts bring students in
    text: str = ""  # HTML; sent before the poll when a post has both, such as a reading passage
    poll: Optional[Poll] = None


def esc(value: Any) -> str:
    return html.escape(str(value), quote=False)


def tg_len(text: str) -> int:
    """Telegram counts UTF-16 code units, so an emoji takes two."""
    return len(text.encode("utf-16-le")) // 2


def clip(text: str, limit: int = POLL_EXPLANATION_LIMIT) -> str:
    """Fits text into a limit on a sentence end where possible. Also folds line breaks, which polls limit."""
    text = " ".join(text.split())
    if tg_len(text) <= limit:
        return text
    cut = text[:limit]
    while tg_len(cut) > limit - 1:
        cut = cut[:-1]
    sentence_end = max(cut.rfind(". "), cut.rfind("! "), cut.rfind("? "))
    return cut[: sentence_end + 1] if sentence_end > 60 else cut.rstrip() + "…"


def plain_text(text: str) -> Optional[str]:
    """Turns LaTeX into text Telegram can show in a poll. Returns None if a formula is too complex for that."""
    def formula(match: re.Match) -> str:
        value = match.group(1)
        value = re.sub(r"\\frac\{([^{}]+)\}\{([^{}]+)\}", r"\1/\2", value)
        value = re.sub(r"\\sqrt\{([^{}]+)\}", r"√(\1)", value)
        for source, target in _PLAIN_SYMBOLS:
            value = value.replace(source, target)
        value = re.sub(r"_\{(\d+)\}", r"\1", value)
        return value.replace("{,}", ",").strip()

    result = re.sub(r"\\\((.+?)\\\)", formula, text, flags=re.S)
    return None if "\\" in result or "{" in result or "^" in result else result


def short_explanation(text: str) -> str:
    return clip(plain_text(text) or "")


def item_id(prefix: str, *parts: str) -> str:
    """Stable id from the content itself, so adding items later does not disturb what was already posted."""
    return f"{prefix}:{hashlib.sha1('|'.join(parts).encode('utf-8')).hexdigest()[:10]}"


def practice_button(source: str, label: str = "📱 Ko'proq mashq qilish") -> InlineKeyboardMarkup:
    url = f"https://t.me/{BOT_USERNAME}?start=ch_{source}"
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=label, url=url)]])


def _load(prefix: str) -> list[dict[str, Any]]:
    """Reads every data/channel/<prefix>*.json file, so a bank can grow in several files."""
    items: list[dict[str, Any]] = []
    for path in sorted(DATA_DIR.glob(f"{prefix}*.json")):
        items.extend(json.loads(path.read_text(encoding="utf-8")))
    return items


# ---------------------------------------------------------------- SAT questions from the practice bank

SAT_LABELS = {"m": "🎯 SAT Math", "rw": "🎯 SAT R&W"}


def channel_quiz_candidates() -> list[dict[str, Any]]:
    """MCQ questions no mock uses, so the channel never gives away a mock."""
    candidates = []
    for question in content.bank.values():
        if not question.get("free") or question["type"] != "mcq" or "fig" in question:
            continue
        stem = plain_text(question["q"])
        options = [plain_text(option) for option in question["opts"]]
        passage = plain_text(question.get("pas", "")) if question.get("pas") else ""
        if stem is None or passage is None or None in options:
            continue
        if tg_len(f"{SAT_LABELS[question['sec']]}\n\n{stem}") > POLL_QUESTION_LIMIT or len(passage) > PASSAGE_LIMIT:
            continue
        if any(tg_len(option) > POLL_OPTION_LIMIT for option in options):
            continue
        candidates.append({"id": question["id"], "sec": question["sec"], "dom": question["dom"], "stem": stem,
                           "passage": passage, "options": options, "correct": "ABCD".index(question["cor"])})
    return candidates


def bank_question_post(item: dict[str, Any]) -> Post:
    text = f"📄 <b>Kunning savoli: matn</b>\n\n{esc(item['passage'])}" if item["passage"] else ""
    return Post(source="quiz", text=text, poll=Poll(
        question=f"{SAT_LABELS[item['sec']]}\n\n{item['stem']}", options=tuple(item["options"]),
        correct=item["correct"], explanation=short_explanation(content.notes[item["id"]]["exp"]),
    ))


# ---------------------------------------------------------------- words, phrases and their quizzes

def _roots(text: str) -> set[str]:
    words = re.findall(r"[a-zʻ'’]+", text.lower())
    return {word[:5] for word in words if len(word) >= 5 and word not in _STOPWORDS}


def _related(a: dict[str, Any], b: dict[str, Any]) -> bool:
    """True when two entries could pass for each other, so one must not be a wrong option for the other.
    'near' lists the close pairs that sit in different meaning groups, which no automatic check would catch."""
    if b["w"] in a.get("near", []) or a["w"] in b.get("near", []):
        return True
    a_words = {a["w"].lower(), *(s.lower() for s in a.get("syn", []))}
    b_words = {b["w"].lower(), *(s.lower() for s in b.get("syn", []))}
    return bool(a_words & b_words) or bool(_roots(a["uz"]) & _roots(b["uz"]))


def distractors(target: dict[str, Any], bank: list[dict[str, Any]], seed: str, count: int = 3) -> list[dict[str, Any]]:
    """Wrong options of the same part of speech, from other meaning groups, with no shared sense."""
    pool = [item for item in bank if item is not target and item.get("pos") == target.get("pos")
            and item["g"] != target["g"] and not _related(target, item)]
    random.Random(seed).shuffle(pool)
    picked: list[dict[str, Any]] = []
    for item in pool:
        if all(not _related(item, other) for other in picked):
            picked.append(item)
        if len(picked) == count:
            break
    return picked


def _options(correct: str, wrong: list[str], seed: str) -> tuple[tuple[str, ...], int]:
    options = [correct, *wrong]
    random.Random(seed).shuffle(options)
    return tuple(options), options.index(correct)


def word_card(word: dict[str, Any], exam: str) -> Post:
    english, uzbek = POS[word["pos"]]
    head = "📘 <b>SAT so'zi</b>" if exam == "SAT" else "📗 <b>IELTS so'zi</b>"
    if word.get("topic"):
        head += f" · {esc(word['topic'])}"
    lines = [head, "", f"<b>{esc(word['w'])}</b> <i>({english} · {uzbek})</i>",
             f"🇺🇿 {esc(word['uz'])}", f"📖 {esc(word['en'])}", "", f"✍️ <i>{esc(word['ex'])}</i>"]
    if word.get("syn"):
        lines.append(f"🔁 <b>Sinonimlar:</b> {esc(', '.join(word['syn']))}")
    return Post(source=f"{exam.lower()}_word", text="\n".join(lines))


def word_quizzes(word: dict[str, Any], bank: list[dict[str, Any]], exam: str) -> dict[str, Post]:
    """Up to three quizzes per word: its meaning, the word for a meaning, and its synonym."""
    posts: dict[str, Post] = {}
    tag = f"🔤 So'z testi · {exam}"
    key = f"{exam}:{word['w']}"

    wrong = distractors(word, bank, f"{key}:meaning")
    if len(wrong) == 3:
        options, correct = _options(word["uz"], [item["uz"] for item in wrong], f"{key}:meaning")
        posts[item_id("wq", key, "meaning")] = Post(source="word_quiz", poll=Poll(
            question=f"{tag}\n\n«{word['w']}» so'zining ma'nosi qaysi?", options=options, correct=correct,
            explanation=clip(f"{word['w']} — {word['uz']}. {word['ex']}")))

    wrong = distractors(word, bank, f"{key}:reverse")
    if len(wrong) == 3:
        options, correct = _options(word["w"], [item["w"] for item in wrong], f"{key}:reverse")
        posts[item_id("wq", key, "reverse")] = Post(source="word_quiz", poll=Poll(
            question=f"{tag}\n\nQaysi so'z «{word['uz']}» degan ma'noni beradi?", options=options, correct=correct,
            explanation=clip(f"{word['w']} — {word['en']}. {word['ex']}")))

    synonyms = word.get("syn") or []
    wrong = distractors(word, bank, f"{key}:synonym")
    if synonyms and len(wrong) == 3:
        options, correct = _options(synonyms[0], [item["w"] for item in wrong], f"{key}:synonym")
        posts[item_id("wq", key, "synonym")] = Post(source="word_quiz", poll=Poll(
            question=f"🔁 Sinonim · {exam}\n\n«{word['w']}» so'ziga ma'nosi eng yaqin so'z qaysi?",
            options=options, correct=correct,
            explanation=clip(f"{word['w']} ≈ {', '.join(synonyms)}. Ma'nosi: {word['uz']}.")))
    return posts


def phrase_card(phrase: dict[str, Any]) -> Post:
    label, note = PHRASE_TYPES[phrase["t"]]
    lines = [f"🧩 <b>{label}</b> · IELTS", "", f"<b>{esc(phrase['w'])}</b>",
             f"🇺🇿 {esc(phrase['uz'])}", f"📖 {esc(phrase['en'])}", "", f"✍️ <i>{esc(phrase['ex'])}</i>", "", note]
    if phrase.get("f"):
        lines.append(f"🎓 Rasmiy muqobili: <b>{esc(phrase['f'])}</b>")
    return Post(source="phrase", text="\n".join(lines))


def phrase_quiz(phrase: dict[str, Any], bank: list[dict[str, Any]]) -> Optional[Post]:
    wrong = distractors(phrase, bank, f"phrase:{phrase['w']}")
    if len(wrong) < 3:
        return None
    label = PHRASE_TYPES[phrase["t"]][0]
    options, correct = _options(phrase["uz"], [item["uz"] for item in wrong], f"phrase:{phrase['w']}")
    return Post(source="ielts_quiz", poll=Poll(
        question=f"🧩 {label} · IELTS\n\n«{phrase['w']}» nimani anglatadi?", options=options, correct=correct,
        explanation=clip(f"{phrase['w']} — {phrase['uz']}. {phrase['ex']}")))


def family_posts(words: list[dict[str, Any]], exam: str) -> dict[str, Post]:
    """SAT words that share a meaning group, shown side by side, since the test rewards telling them apart."""
    groups: dict[str, list[dict[str, Any]]] = {}
    for word in words:
        groups.setdefault(word["g"], []).append(word)
    posts = {}
    for group, members in groups.items():
        if len(members) < 4:
            continue
        lines = [f"🧬 <b>Ma'nodosh so'zlar · {exam}</b>", "", "Ma'nosi yaqin, lekin bir xil emas:", ""]
        lines += [f"• <b>{esc(w['w'])}</b> — {esc(w['uz'])}" for w in members[:FAMILY_SIZE]]
        lines += ["", "💡 Words in Context savollarida gapning ohangiga qarab eng aniq so'zni tanlang."]
        posts[item_id("family", exam, group)] = Post(source="sat_word", text="\n".join(lines))
    return posts


def topic_packs(words: list[dict[str, Any]]) -> dict[str, Post]:
    """IELTS words gathered by topic into short lists, for revision before Writing and Speaking."""
    topics: dict[str, list[dict[str, Any]]] = {}
    for word in words:
        topics.setdefault(word.get("topic") or "Umumiy", []).append(word)
    posts = {}
    for topic, members in topics.items():
        for start in range(0, len(members), FAMILY_SIZE):
            chunk = members[start:start + FAMILY_SIZE]
            if len(chunk) < 4:
                continue
            lines = [f"📦 <b>IELTS so'zlari · {esc(topic)}</b>", ""]
            lines += [f"• <b>{esc(w['w'])}</b> — {esc(w['uz'])}" for w in chunk]
            lines += ["", "✍️ Shu mavzudagi inshoda kamida uchtasini ishlatib ko'ring."]
            posts[item_id("topic", topic, chunk[0]["w"])] = Post(source="ielts_word", text="\n".join(lines))
    return posts


def vocab_pack_post(pack: dict[str, Any]) -> Post:
    lines = ["📖 <b>IELTS: 10 ta so'z to'plami</b>", f"🏷 <b>Mavzu</b>: {esc(pack['topic'])}", ""]
    for number, word in enumerate(pack["words"], start=1):
        lines.append(f"<b>{number}. {esc(word['w'])}</b> — {esc(word['m'])}\n   🔗 <i>Kollokatsiya:</i> <code>{esc(word['c'])}</code>")
    return Post(source="vocab", text="\n".join(lines))


# ---------------------------------------------------------------- tips, facts, speaking and quizzes

IELTS_SECTIONS = ("Listening", "Reading", "Writing", "Speaking", "Vocabulary")


def legacy_tip_exam(title: str) -> str:
    """The older tips in content_bank.py mix both exams, and their titles say which one."""
    if title.startswith("SAT"):
        return "SAT"
    return "IELTS" if title.split(":")[0].split()[0] in IELTS_SECTIONS else "SAT va IELTS"


def tip_post(tip: dict[str, Any]) -> Post:
    title = tip["title"] if tip["title"].startswith(tip["exam"]) else f"{tip['exam']} maslahati: {tip['title']}"
    return Post(source="tip", text=f"💡 <b>{esc(title)}</b>\n\n{esc(tip['body'])}")


def fact_post(fact: dict[str, Any]) -> Post:
    return Post(source="fact", text=f"📌 <b>Bilasizmi?</b> · {esc(fact['exam'])}\n\n{esc(fact['text'])}")


def speaking_post(item: dict[str, Any]) -> Post:
    lines = [f"🗣 <b>IELTS Speaking · Part {item['part']}</b>", "", f"<b>{esc(item['q'])}</b>"]
    if item.get("cue"):
        lines += ["You should say:", *(f"• {esc(cue)}" for cue in item["cue"])]
    lines += ["", "💡 <b>Foydali iboralar:</b>", *(f"• <i>{esc(phrase)}</i>" for phrase in item["ph"])]
    if item.get("h"):
        lines += ["", f"🎯 {esc(item['h'])}"]
    lines += ["", SPEAKING_TIMING[item["part"]]]
    return Post(source="speaking", text="\n".join(lines))


def quiz_post(item: dict[str, Any], label: str, source: str) -> Post:
    """Options are shuffled by a fixed seed, so the answer is not always in the place it was written."""
    right = item["o"][item["a"]]
    options, correct = _options(right, [option for i, option in enumerate(item["o"]) if i != item["a"]], item["q"])
    text = f"📄 <b>Matn</b>\n\n{esc(item['pas'])}" if item.get("pas") else ""
    return Post(source=source, text=text, poll=Poll(
        question=f"{label} · {item['t']}\n\n{item['q']}", options=options, correct=correct,
        explanation=clip(item["e"])))


@lru_cache(maxsize=1)
def pools() -> dict[str, dict[str, Post]]:
    """Every post the channel can make, by kind, keyed by a stable id."""
    result: dict[str, dict[str, Post]] = {kind: {} for kind in KINDS}

    def add(kind: str, key: str, post: Post) -> None:
        # Two items with one id would silently replace each other, so a clash is reported instead.
        if key in result[kind]:
            logger.error("Channel item %s in %s is a duplicate and was skipped", key, kind)
            return
        result[kind][key] = post

    sat_words, ielts_words, phrases = _load("sat_words"), _load("ielts_words"), _load("phrases")
    for words, exam, prefix in ((sat_words, "SAT", "sw"), (ielts_words, "IELTS", "iw")):
        for word in words:
            add(f"{exam.lower()}_word", item_id(prefix, word["w"]), word_card(word, exam))
            for key, post in word_quizzes(word, words, exam).items():
                add("word_quiz", key, post)
    for phrase in phrases:
        add("phrase", item_id("ph", phrase["w"]), phrase_card(phrase))
        quiz = phrase_quiz(phrase, phrases)
        if quiz:
            add("ielts_quiz", item_id("phq", phrase["w"]), quiz)

    for tip in [*({"exam": legacy_tip_exam(tip["title"]), **tip} for tip in IELTS_TIPS), *_load("tips")]:
        add("tip", item_id("tip", tip["exam"], tip["title"]), tip_post(tip))

    for item in channel_quiz_candidates():
        add("sat_quiz", item["id"], bank_question_post(item))
    # Several written quizzes share a stem such as "Which spelling is correct?", so the options are part of the id.
    for prefix, kind, label, source in (("sat_quizzes", "sat_quiz", "✍️ SAT R&W", "quiz"),
                                        ("ielts_quizzes", "ielts_quiz", "🧠 IELTS", "ielts_quiz"),
                                        ("sat_math", "math", "➗ SAT Math", "math")):
        for item in _load(prefix):
            add(kind, item_id(kind, item["q"], *item["o"]), quiz_post(item, label, source))
    for item in _load("speaking"):
        add("speaking", item_id("sp", str(item["part"]), item["q"]), speaking_post(item))

    for fact in _load("facts"):
        add("extra", item_id("fact", fact["text"]), fact_post(fact))
    for number, pack in enumerate(IELTS_VOCAB_PACKS):
        add("extra", f"pack:{number}", vocab_pack_post(pack))
    for key, post in [*family_posts(sat_words, "SAT").items(), *topic_packs(ielts_words).items()]:
        add("extra", key, post)
    return result


# ---------------------------------------------------------------- picking and sending

async def next_item(kind: str, item_ids: list[str]) -> str:
    """Picks an item not posted yet. When all have been used, the cycle starts over."""
    try:
        rows = await db.fetch("SELECT item_id FROM channel_log WHERE kind = ?", kind)
    except Exception as error:
        logger.warning("channel_log unreadable (%s), so %s is drawn by date", type(error).__name__, kind)
        return random.Random(f"{kind}:{today()}").choice(sorted(item_ids))
    used = {row["item_id"] for row in rows}
    fresh = [item for item in item_ids if item not in used]
    choice = random.choice(fresh or list(item_ids))
    try:
        if not fresh:
            await db.execute("DELETE FROM channel_log WHERE kind = ?", kind)
        await db.execute(
            "INSERT INTO channel_log (kind, item_id, posted_at) VALUES (?, ?, ?) ON CONFLICT (kind, item_id) DO NOTHING",
            kind, choice, now_ts(),
        )
    except Exception as error:
        logger.warning("channel_log not updated for %s: %s", kind, type(error).__name__)
    return choice


async def pick(kind: str) -> Post:
    pool = pools()[kind]
    return pool[await next_item(kind, sorted(pool))]


async def _send(method, **kwargs):
    try:
        return await method(**kwargs)
    except TelegramRetryAfter as error:
        await asyncio.sleep(error.retry_after + 1)
        return await method(**kwargs)


async def deliver(bot, post: Post) -> None:
    markup = practice_button(post.source)
    if post.poll is None:
        await _send(bot.send_message, chat_id=CHANNEL_ID, text=post.text + FOOTER, parse_mode="HTML", reply_markup=markup)
        return
    if post.text:
        await _send(bot.send_message, chat_id=CHANNEL_ID, text=post.text, parse_mode="HTML")
    poll = post.poll
    # The bot's default parse mode is HTML and aiogram applies it to the question and explanation too.
    await _send(
        bot.send_poll, chat_id=CHANNEL_ID, question=esc(poll.question), question_parse_mode="HTML",
        options=list(poll.options), type="quiz", correct_option_id=poll.correct,
        explanation=esc(poll.explanation) or None, explanation_parse_mode="HTML",
        is_anonymous=True, reply_markup=markup,
    )


async def post_slot(bot, slot: int) -> int:
    """Posts one slot of the day. A failed post is logged and the rest of the slot still goes out."""
    kinds = SLOTS[slot][2]
    sent = 0
    for position, kind in enumerate(kinds):
        if position:
            await asyncio.sleep(POST_GAP_SECONDS)
        try:
            await deliver(bot, await pick(kind))
            sent += 1
        except Exception as error:
            logger.error("Channel post %s failed: %s", kind, error)
    logger.info("Channel slot %s: %s of %s posts sent", slot, sent, len(kinds))
    return sent
