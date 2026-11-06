"""
Share cards: a PNG of a result for Telegram stories, reachable through a signed link.
"""

import hashlib
import hmac
import io
import json
from typing import Any, Optional

from database import db

SIZE = (1080, 1920)
BACKGROUND = (15, 23, 42)
ACCENT = (96, 165, 250)
TEXT = (241, 245, 249)
MUTED = (148, 163, 184)


def _signature(attempt_id: str, token: str) -> str:
    return hmac.new(token.encode(), attempt_id.encode(), hashlib.sha256).hexdigest()[:20]


def card_path(attempt_id: str, token: str) -> str:
    return f"/card/{attempt_id}-{_signature(attempt_id, token)}.png"


def verify(attempt_id: str, signature: str, token: str) -> bool:
    return hmac.compare_digest(_signature(attempt_id, token), signature)


def headline(attempt: dict[str, Any]) -> tuple[str, str]:
    """The big number on the card and what it measures."""
    kind = attempt["kind"]
    if kind == "sat_mock":
        return f"{attempt['score']:.0f}", "SAT mock (taxminiy ball)"
    if kind in ("ielts_reading", "ielts_listening"):
        name = "Reading" if kind == "ielts_reading" else "Listening"
        return f"{attempt['score']:.1f}", f"IELTS {name} (taxminiy band)"
    return f"{attempt['correct']}/{attempt['total']}", "to'g'ri javob"


def share_text(attempt: dict[str, Any]) -> str:
    value, label = headline(attempt)
    return f"Men IELTS & SAT Daily'da {value} natija oldim: {label}. Sen ham sinab ko'r!"


async def render_card(attempt_id: str) -> Optional[bytes]:
    from PIL import Image, ImageDraw, ImageFont

    row = await db.fetchrow(
        """SELECT attempts.kind, attempts.score, attempts.correct, attempts.total, attempts.report, users.first_name
           FROM attempts JOIN users ON users.id = attempts.user_id WHERE attempts.id = ?""",
        attempt_id,
    )
    if row is None:
        return None
    value, label = headline(row)
    report = json.loads(row["report"])

    image = Image.new("RGB", SIZE, BACKGROUND)
    draw = ImageDraw.Draw(image)

    def font(size: int):
        return ImageFont.load_default(size)

    def centered(y: int, text: str, size: int, fill: tuple[int, int, int]) -> None:
        box = draw.textbbox((0, 0), text, font=font(size))
        draw.text(((SIZE[0] - (box[2] - box[0])) / 2, y), text, font=font(size), fill=fill)

    draw.rounded_rectangle((90, 520, SIZE[0] - 90, 1340), radius=48, fill=(30, 41, 59))
    centered(250, "IELTS & SAT Daily", 64, TEXT)
    centered(340, "Mashq natijasi", 40, MUTED)
    centered(620, row["first_name"][:24] or "O'quvchi", 56, TEXT)
    centered(760, value, 200, ACCENT)
    centered(1020, label, 44, MUTED)
    sections = report.get("sections")
    if sections:
        centered(1130, f"Reading & Writing {sections['rw']['score']}  ·  Math {sections['math']['score']}", 44, TEXT)
    centered(1560, "Bepul mock testlar", 48, TEXT)
    centered(1630, "Telegram: @ieltssat_dailybot", 44, ACCENT)

    buffer = io.BytesIO()
    image.save(buffer, format="PNG", optimize=True)
    return buffer.getvalue()
