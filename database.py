"""
Async storage layer. Uses Postgres when DATABASE_URL is set, otherwise a local SQLite file.

Queries are written once with `?` placeholders and the portable subset of SQL both engines share.
"""

import asyncio
import contextvars
import logging
import re
import time
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from zoneinfo import ZoneInfo

from config import DATABASE_URL, SQLITE_PATH, TIMEZONE

logger = logging.getLogger(__name__)

TZ = ZoneInfo(TIMEZONE)


def now_ts() -> int:
    return int(time.time())


def today(ts: int | None = None) -> str:
    return datetime.fromtimestamp(now_ts() if ts is None else ts, TZ).strftime("%Y-%m-%d")


def shift_day(day: str, days: int) -> str:
    return (datetime.strptime(day, "%Y-%m-%d") + timedelta(days=days)).strftime("%Y-%m-%d")


def day_diff(later: str, earlier: str) -> int:
    return (datetime.strptime(later, "%Y-%m-%d") - datetime.strptime(earlier, "%Y-%m-%d")).days


SCHEMA = [
    """CREATE TABLE IF NOT EXISTS users (
        id BIGINT PRIMARY KEY,
        first_name TEXT NOT NULL DEFAULT '',
        username TEXT NOT NULL DEFAULT '',
        language_code TEXT NOT NULL DEFAULT '',
        created_at BIGINT NOT NULL,
        last_seen_at BIGINT NOT NULL,
        source TEXT NOT NULL DEFAULT '',
        referred_by BIGINT,
        referral_rewarded BIGINT NOT NULL DEFAULT 0,
        bot_started BIGINT NOT NULL DEFAULT 0,
        blocked BIGINT NOT NULL DEFAULT 0,
        onboarded BIGINT NOT NULL DEFAULT 0,
        focus TEXT NOT NULL DEFAULT '',
        target_sat BIGINT,
        target_ielts DOUBLE PRECISION,
        exam_date TEXT,
        daily_minutes BIGINT NOT NULL DEFAULT 30,
        reminder_hour BIGINT NOT NULL DEFAULT 19,
        reminders_on BIGINT NOT NULL DEFAULT 1,
        streak BIGINT NOT NULL DEFAULT 0,
        best_streak BIGINT NOT NULL DEFAULT 0,
        last_active_day TEXT,
        last_reminded_day TEXT,
        ai_bonus BIGINT NOT NULL DEFAULT 0
    )""",
    """CREATE TABLE IF NOT EXISTS attempts (
        id TEXT PRIMARY KEY,
        user_id BIGINT NOT NULL,
        kind TEXT NOT NULL,
        ref TEXT NOT NULL DEFAULT '',
        title TEXT NOT NULL DEFAULT '',
        session_code TEXT,
        correct BIGINT NOT NULL DEFAULT 0,
        total BIGINT NOT NULL DEFAULT 0,
        score DOUBLE PRECISION,
        score_low DOUBLE PRECISION,
        score_high DOUBLE PRECISION,
        duration_s BIGINT NOT NULL DEFAULT 0,
        report TEXT NOT NULL DEFAULT '{}',
        created_at BIGINT NOT NULL,
        day TEXT NOT NULL
    )""",
    "CREATE INDEX IF NOT EXISTS idx_attempts_user ON attempts (user_id, created_at)",
    "CREATE INDEX IF NOT EXISTS idx_attempts_session ON attempts (session_code)",
    """CREATE TABLE IF NOT EXISTS answers (
        attempt_id TEXT NOT NULL,
        user_id BIGINT NOT NULL,
        question_id TEXT NOT NULL,
        section TEXT NOT NULL DEFAULT '',
        domain TEXT NOT NULL DEFAULT '',
        skill TEXT NOT NULL DEFAULT '',
        difficulty TEXT NOT NULL DEFAULT '',
        module TEXT NOT NULL DEFAULT '',
        chosen TEXT NOT NULL DEFAULT '',
        is_correct BIGINT NOT NULL DEFAULT 0,
        time_s BIGINT NOT NULL DEFAULT 0,
        created_at BIGINT NOT NULL,
        PRIMARY KEY (attempt_id, question_id)
    )""",
    "CREATE INDEX IF NOT EXISTS idx_answers_user ON answers (user_id, created_at)",
    "CREATE INDEX IF NOT EXISTS idx_answers_question ON answers (question_id)",
    """CREATE TABLE IF NOT EXISTS review_items (
        user_id BIGINT NOT NULL,
        question_id TEXT NOT NULL,
        box BIGINT NOT NULL DEFAULT 0,
        due_day TEXT NOT NULL,
        wrong_count BIGINT NOT NULL DEFAULT 1,
        resolved BIGINT NOT NULL DEFAULT 0,
        last_chosen TEXT NOT NULL DEFAULT '',
        updated_at BIGINT NOT NULL,
        PRIMARY KEY (user_id, question_id)
    )""",
    "CREATE INDEX IF NOT EXISTS idx_review_due ON review_items (user_id, resolved, due_day)",
    """CREATE TABLE IF NOT EXISTS writing_submissions (
        id TEXT PRIMARY KEY,
        user_id BIGINT NOT NULL,
        task BIGINT NOT NULL,
        prompt_id TEXT NOT NULL DEFAULT '',
        prompt TEXT NOT NULL DEFAULT '',
        essay TEXT NOT NULL DEFAULT '',
        word_count BIGINT NOT NULL DEFAULT 0,
        minutes BIGINT NOT NULL DEFAULT 0,
        band DOUBLE PRECISION,
        feedback TEXT NOT NULL DEFAULT '{}',
        model TEXT NOT NULL DEFAULT '',
        created_at BIGINT NOT NULL,
        day TEXT NOT NULL
    )""",
    "CREATE INDEX IF NOT EXISTS idx_writing_user ON writing_submissions (user_id, created_at)",
    "CREATE INDEX IF NOT EXISTS idx_writing_day ON writing_submissions (day)",
    """CREATE TABLE IF NOT EXISTS channel_log (
        kind TEXT NOT NULL,
        item_id TEXT NOT NULL,
        posted_at BIGINT NOT NULL,
        PRIMARY KEY (kind, item_id)
    )""",
    """CREATE TABLE IF NOT EXISTS events (
        user_id BIGINT NOT NULL,
        name TEXT NOT NULL,
        meta TEXT NOT NULL DEFAULT '',
        day TEXT NOT NULL,
        created_at BIGINT NOT NULL
    )""",
    "CREATE INDEX IF NOT EXISTS idx_events_day ON events (day, name)",
    """CREATE TABLE IF NOT EXISTS centers (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        teacher_code TEXT NOT NULL UNIQUE,
        created_by BIGINT NOT NULL,
        created_at BIGINT NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS center_members (
        center_id TEXT NOT NULL,
        user_id BIGINT NOT NULL,
        role TEXT NOT NULL,
        joined_at BIGINT NOT NULL,
        PRIMARY KEY (center_id, user_id)
    )""",
    "CREATE INDEX IF NOT EXISTS idx_center_members_user ON center_members (user_id)",
    """CREATE TABLE IF NOT EXISTS exam_sessions (
        code TEXT PRIMARY KEY,
        center_id TEXT,
        created_by BIGINT NOT NULL,
        title TEXT NOT NULL,
        kind TEXT NOT NULL,
        ref TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'open',
        created_at BIGINT NOT NULL,
        closed_at BIGINT
    )""",
    "CREATE INDEX IF NOT EXISTS idx_sessions_center ON exam_sessions (center_id, created_at)",
]

_current_conn: contextvars.ContextVar[Any] = contextvars.ContextVar("db_conn", default=None)
_PLACEHOLDER = re.compile(r"\?")


# Hosts such as Neon add these libpq options to their URLs. asyncpg would pass them to the server
# as settings, and the server would refuse the connection.
LIBPQ_ONLY_OPTIONS = {"channel_binding", "connect_timeout", "gssencmode", "pgbouncer"}


def asyncpg_url(url: str) -> str:
    parts = urlsplit(url)
    query = [(key, value) for key, value in parse_qsl(parts.query) if key not in LIBPQ_ONLY_OPTIONS]
    return urlunsplit(parts._replace(query=urlencode(query)))


def _to_postgres(sql: str) -> str:
    counter = iter(range(1, 1000))
    return _PLACEHOLDER.sub(lambda _: f"${next(counter)}", sql)


class Database:
    def __init__(self, url: str = DATABASE_URL, sqlite_path: str = SQLITE_PATH):
        self.url = url
        self.sqlite_path = sqlite_path
        self._pool = None
        self._sqlite = None
        self._sqlite_lock = asyncio.Lock()

    @property
    def kind(self) -> str:
        return "postgres" if self.url else "sqlite"

    async def connect(self) -> None:
        if self.url:
            import asyncpg

            # statement_cache_size=0 keeps the pool usable behind pgbouncer-style poolers (Neon, Supabase).
            self._pool = await asyncpg.create_pool(
                asyncpg_url(self.url), min_size=1, max_size=5, command_timeout=30,
                statement_cache_size=0, max_inactive_connection_lifetime=240,
            )
        else:
            import aiosqlite

            if self.sqlite_path != ":memory:":
                Path(self.sqlite_path).parent.mkdir(parents=True, exist_ok=True)
            self._sqlite = await aiosqlite.connect(self.sqlite_path)
            self._sqlite.row_factory = aiosqlite.Row
            await self._sqlite.execute("PRAGMA journal_mode=WAL")
            await self._sqlite.execute("PRAGMA synchronous=NORMAL")
        for statement in SCHEMA:
            await self.execute(statement)
        logger.info("Database ready: %s", self.kind)

    async def close(self) -> None:
        if self._pool is not None:
            await self._pool.close()
            self._pool = None
        if self._sqlite is not None:
            await self._sqlite.close()
            self._sqlite = None

    async def ping(self) -> bool:
        try:
            return await self.fetchval("SELECT 1") == 1
        except Exception as e:
            logger.warning("Database ping failed: %s", e)
            return False

    @asynccontextmanager
    async def transaction(self):
        """Statements awaited inside this block run in one transaction on one connection."""
        if self._pool is not None:
            async with self._pool.acquire() as conn:
                async with conn.transaction():
                    token = _current_conn.set(conn)
                    try:
                        yield
                    finally:
                        _current_conn.reset(token)
            return
        async with self._sqlite_lock:
            await self._sqlite.execute("BEGIN")
            token = _current_conn.set(self._sqlite)
            try:
                yield
            except BaseException:
                await self._sqlite.rollback()
                raise
            else:
                await self._sqlite.commit()
            finally:
                _current_conn.reset(token)

    async def execute(self, sql: str, *args: Any) -> None:
        if self._pool is not None:
            conn = _current_conn.get()
            await (conn or self._pool).execute(_to_postgres(sql), *args)
            return
        if _current_conn.get() is not None:
            await self._sqlite.execute(sql, args)
            return
        async with self._sqlite_lock:
            await self._sqlite.execute(sql, args)
            await self._sqlite.commit()

    async def executemany(self, sql: str, rows: list[tuple]) -> None:
        if not rows:
            return
        if self._pool is not None:
            conn = _current_conn.get()
            await (conn or self._pool).executemany(_to_postgres(sql), rows)
            return
        if _current_conn.get() is not None:
            await self._sqlite.executemany(sql, rows)
            return
        async with self._sqlite_lock:
            await self._sqlite.executemany(sql, rows)
            await self._sqlite.commit()

    async def fetch(self, sql: str, *args: Any) -> list[dict[str, Any]]:
        if self._pool is not None:
            conn = _current_conn.get()
            rows = await (conn or self._pool).fetch(_to_postgres(sql), *args)
            return [dict(row) for row in rows]
        if _current_conn.get() is not None:
            async with self._sqlite.execute(sql, args) as cursor:
                return [dict(row) for row in await cursor.fetchall()]
        async with self._sqlite_lock:
            async with self._sqlite.execute(sql, args) as cursor:
                return [dict(row) for row in await cursor.fetchall()]

    async def fetchrow(self, sql: str, *args: Any) -> dict[str, Any] | None:
        rows = await self.fetch(sql, *args)
        return rows[0] if rows else None

    async def fetchval(self, sql: str, *args: Any) -> Any:
        row = await self.fetchrow(sql, *args)
        return next(iter(row.values())) if row else None


db = Database()
