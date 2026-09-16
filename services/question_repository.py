"""
EduTest Pro - Question Vault Repository
SQLite-backed high-performance question bank repository with lifecycle management
(draft, review, published, rejected, pending_human_review), atomic JSON synchronization,
and multi-dimensional query filters.
"""

import hashlib
import json
import logging
import os
import sqlite3
import threading
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("QuestionRepository")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "questions_vault.db")
DEFAULT_EXPORT_JSON = os.path.join(BASE_DIR, "data", "sat_question_bank.json")


def compute_stem_hash(passage: str | None, question: str) -> str:
    """Computes a deterministic hash for uniqueness checking."""
    raw = (str(passage or "").strip() + " ___ " + str(question).strip()).lower()
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


class QuestionRepository:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, db_path: str = DB_PATH, *args, **kwargs):
        with cls._lock:
            if db_path == DB_PATH:
                if cls._instance is None:
                    cls._instance = super(QuestionRepository, cls).__new__(cls)
                    cls._instance._initialized = False
                return cls._instance
            inst = super(QuestionRepository, cls).__new__(cls)
            inst._initialized = False
            return inst

    def __init__(self, db_path: str = DB_PATH):
        if getattr(self, "_initialized", False):
            return
        self.db_path = db_path
        self._local = threading.local()
        self.init_db()
        self._initialized = True

    def _get_connection(self) -> sqlite3.Connection:
        """Returns thread-local sqlite connection."""
        if not hasattr(self._local, "conn") or self._local.conn is None:
            conn = sqlite3.connect(self.db_path, timeout=30.0, check_same_thread=False)
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA journal_mode=WAL;")
            conn.execute("PRAGMA synchronous=NORMAL;")
            self._local.conn = conn
        return self._local.conn

    def init_db(self):
        """Initializes database schema and indexes."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = self._get_connection()
        with conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS questions (
                    id TEXT PRIMARY KEY,
                    version INTEGER DEFAULT 1,
                    section TEXT NOT NULL,
                    domain TEXT NOT NULL,
                    skill TEXT NOT NULL,
                    difficulty TEXT NOT NULL,
                    status TEXT NOT NULL,
                    passage TEXT,
                    question TEXT NOT NULL,
                    options_json TEXT NOT NULL,
                    correct TEXT NOT NULL,
                    explanation TEXT NOT NULL,
                    strategy_or_hack TEXT NOT NULL,
                    author TEXT DEFAULT 'internal_authoring',
                    license TEXT DEFAULT 'proprietary_original',
                    stem_hash TEXT UNIQUE,
                    rejection_reason TEXT,
                    metadata_json TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_q_status ON questions(status);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_q_section ON questions(section);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_q_domain ON questions(domain);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_q_skill ON questions(skill);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_q_difficulty ON questions(difficulty);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_q_sec_stat ON questions(section, status);")

            conn.execute("""
                CREATE TABLE IF NOT EXISTS audit_log (
                    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question_id TEXT,
                    action TEXT NOT NULL,
                    details TEXT,
                    timestamp TEXT NOT NULL
                );
            """)

    def upsert_question(self, q: dict[str, Any], status: str | None = None) -> tuple[bool, str]:
        """
        Inserts or updates a question in the vault.
        Enforces stem_hash uniqueness (rejects duplicates).
        """
        qid = str(q.get("id", "")).strip()
        if not qid:
            return False, "Missing question ID"

        section = str(q.get("section", "math")).lower().strip()
        domain = str(q.get("domain", "General")).strip()
        skill = str(q.get("skill", domain)).strip()
        difficulty = str(q.get("difficulty", "Medium")).capitalize().strip()
        cur_status = status or str(q.get("status", "draft")).lower().strip()
        passage = q.get("passage")
        if passage is not None:
            passage = str(passage).strip()
        question_text = str(q.get("question", "")).strip()
        options = q.get("options", [])
        options_json = json.dumps(options, ensure_ascii=False)
        correct = str(q.get("correct", "A")).upper().strip()
        explanation = str(q.get("explanation", "")).strip()
        strategy_or_hack = str(q.get("strategy_or_hack") or q.get("desmos_hack", "")).strip()
        author = str(q.get("author", "internal_authoring")).strip()
        license_type = str(q.get("license", "proprietary_original")).strip()
        rejection_reason = str(q.get("rejection_reason", "")).strip() if q.get("rejection_reason") else None
        
        meta = q.get("metadata", {})
        metadata_json = json.dumps(meta, ensure_ascii=False) if isinstance(meta, dict) else "{}"

        stem_hash = q.get("stem_hash") or compute_stem_hash(passage, question_text)
        now_iso = datetime.now(timezone.utc).isoformat()

        conn = self._get_connection()
        try:
            with conn:
                existing = conn.execute("SELECT id, version, stem_hash FROM questions WHERE id = ?", (qid,)).fetchone()
                if existing:
                    new_version = existing["version"] + 1
                    conn.execute("""
                        UPDATE questions SET
                            version = ?,
                            section = ?,
                            domain = ?,
                            skill = ?,
                            difficulty = ?,
                            status = ?,
                            passage = ?,
                            question = ?,
                            options_json = ?,
                            correct = ?,
                            explanation = ?,
                            strategy_or_hack = ?,
                            author = ?,
                            license = ?,
                            stem_hash = ?,
                            rejection_reason = ?,
                            metadata_json = ?,
                            updated_at = ?
                        WHERE id = ?
                    """, (
                        new_version, section, domain, skill, difficulty, cur_status,
                        passage, question_text, options_json, correct,
                        explanation, strategy_or_hack, author, license_type,
                        stem_hash, rejection_reason, metadata_json, now_iso, qid
                    ))
                    conn.execute("INSERT INTO audit_log (question_id, action, details, timestamp) VALUES (?, ?, ?, ?)",
                                 (qid, "updated", f"Status: {cur_status}, Version: {new_version}", now_iso))
                    return True, f"Updated question {qid} (v{new_version})"
                else:
                    # Check duplicate stem_hash
                    dup = conn.execute("SELECT id FROM questions WHERE stem_hash = ?", (stem_hash,)).fetchone()
                    if dup:
                        return False, f"Duplicate question content already exists with ID '{dup['id']}'"

                    conn.execute("""
                        INSERT INTO questions (
                            id, version, section, domain, skill, difficulty, status,
                            passage, question, options_json, correct, explanation,
                            strategy_or_hack, author, license, stem_hash, rejection_reason,
                            metadata_json, created_at, updated_at
                        ) VALUES (?, 1, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        qid, section, domain, skill, difficulty, cur_status,
                        passage, question_text, options_json, correct, explanation,
                        strategy_or_hack, author, license_type, stem_hash, rejection_reason,
                        metadata_json, now_iso, now_iso
                    ))
                    conn.execute("INSERT INTO audit_log (question_id, action, details, timestamp) VALUES (?, ?, ?, ?)",
                                 (qid, "created", f"Status: {cur_status}", now_iso))
                    return True, f"Created question {qid}"
        except sqlite3.IntegrityError as e:
            return False, f"Integrity error: {e}"
        except Exception as e:
            return False, f"Database error: {e}"

    def get_question(self, qid: str) -> dict[str, Any] | None:
        """Fetches an individual question by ID."""
        conn = self._get_connection()
        row = conn.execute("SELECT * FROM questions WHERE id = ?", (str(qid),)).fetchone()
        if not row:
            return None
        return self._row_to_dict(row)

    def get_published_questions(
        self,
        section: str | None = None,
        domain: str | None = None,
        skill: str | None = None,
        difficulty: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Queries ONLY PUBLISHED questions matching given criteria.
        This guarantees students and mock engines only receive 100% verified material.
        """
        conn = self._get_connection()
        query = "SELECT * FROM questions WHERE status = 'published'"
        params: list[Any] = []

        if section and section.lower() not in ("all", "mixed"):
            query += " AND LOWER(section) = ?"
            params.append(section.lower().strip())

        if domain and domain.lower() != "all":
            query += " AND (LOWER(domain) = ? OR domain LIKE ?)"
            params.append(domain.lower().strip())
            params.append(f"%{domain.strip()}%")

        if skill and skill.lower() != "all":
            query += " AND (LOWER(skill) = ? OR skill LIKE ?)"
            params.append(skill.lower().strip())
            params.append(f"%{skill.strip()}%")

        if difficulty and difficulty.capitalize() != "All":
            query += " AND difficulty = ?"
            params.append(difficulty.capitalize().strip())

        rows = conn.execute(query, params).fetchall()
        return [self._row_to_dict(r) for r in rows]

    def get_counts_by_status(self) -> dict[str, int]:
        """Returns total questions grouped by lifecycle status."""
        conn = self._get_connection()
        rows = conn.execute("SELECT status, COUNT(*) as cnt FROM questions GROUP BY status").fetchall()
        stats = {s: 0 for s in ("draft", "review", "published", "rejected", "pending_human_review")}
        for r in rows:
            st = str(r["status"]).lower()
            stats[st] = r["cnt"]
        return stats

    def get_published_counts_by_section(self) -> dict[str, int]:
        """Returns published count per section: math, reading, writing."""
        conn = self._get_connection()
        rows = conn.execute("""
            SELECT section, COUNT(*) as cnt
            FROM questions
            WHERE status = 'published'
            GROUP BY section
        """).fetchall()
        res = {"math": 0, "reading": 0, "writing": 0}
        for r in rows:
            sec = str(r["section"]).lower()
            res[sec] = r["cnt"]
        return res

    def get_breakdown_by_domain(self, section: str | None = None) -> dict[str, int]:
        """Returns breakdown of published questions by domain."""
        conn = self._get_connection()
        if section and section.lower() not in ("all", "mixed"):
            rows = conn.execute("""
                SELECT domain, COUNT(*) as cnt
                FROM questions
                WHERE status = 'published' AND LOWER(section) = ?
                GROUP BY domain ORDER BY cnt DESC
            """, (section.lower(),)).fetchall()
        else:
            rows = conn.execute("""
                SELECT domain, COUNT(*) as cnt
                FROM questions
                WHERE status = 'published'
                GROUP BY domain ORDER BY cnt DESC
            """).fetchall()
        return {r["domain"]: r["cnt"] for r in rows}

    def get_breakdown_by_skill(self, domain: str | None = None) -> dict[str, int]:
        """Returns breakdown of published questions by specific skill."""
        conn = self._get_connection()
        if domain and domain.lower() != "all":
            rows = conn.execute("""
                SELECT skill, COUNT(*) as cnt
                FROM questions
                WHERE status = 'published' AND (LOWER(domain) = ? OR domain LIKE ?)
                GROUP BY skill ORDER BY cnt DESC
            """, (domain.lower(), f"%{domain}%")).fetchall()
        else:
            rows = conn.execute("""
                SELECT skill, COUNT(*) as cnt
                FROM questions
                WHERE status = 'published'
                GROUP BY skill ORDER BY cnt DESC
            """).fetchall()
        return {r["skill"]: r["cnt"] for r in rows}

    def get_breakdown_by_difficulty(self, section: str | None = None) -> dict[str, int]:
        """Returns breakdown of published questions by difficulty."""
        conn = self._get_connection()
        if section and section.lower() not in ("all", "mixed"):
            rows = conn.execute("""
                SELECT difficulty, COUNT(*) as cnt
                FROM questions
                WHERE status = 'published' AND LOWER(section) = ?
                GROUP BY difficulty
            """, (section.lower(),)).fetchall()
        else:
            rows = conn.execute("""
                SELECT difficulty, COUNT(*) as cnt
                FROM questions
                WHERE status = 'published'
                GROUP BY difficulty
            """).fetchall()
        res = {"Easy": 0, "Medium": 0, "Hard": 0}
        for r in rows:
            diff = str(r["difficulty"]).capitalize()
            res[diff] = r["cnt"]
        return res

    def sync_to_json(self, export_path: str = DEFAULT_EXPORT_JSON) -> int:
        """
        Exports all PUBLISHED questions to target JSON file with atomic write.
        Ensures external consumers (Mini App, test suites) always see clean published data.
        """
        published = self.get_published_questions()
        temp_path = export_path + ".tmp"
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(published, f, ensure_ascii=False, indent=2)
        os.replace(temp_path, export_path)
        logger.info(f"Synchronized {len(published)} published questions to {export_path}")
        return len(published)

    def import_from_json(self, json_path: str, default_status: str = "published") -> tuple[int, int]:
        """Imports an array of questions from JSON into the vault."""
        if not os.path.exists(json_path):
            return 0, 0
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            return 0, 0

        success = 0
        failed = 0
        for item in data:
            if isinstance(item, dict):
                ok, _ = self.upsert_question(item, status=default_status)
                if ok:
                    success += 1
                else:
                    failed += 1
        return success, failed

    def _row_to_dict(self, row: sqlite3.Row) -> dict[str, Any]:
        """Converts an SQLite row to a standard Question dictionary."""
        d = dict(row)
        try:
            d["options"] = json.loads(d.pop("options_json", "[]"))
        except Exception:
            d["options"] = []
        try:
            d["metadata"] = json.loads(d.pop("metadata_json", "{}"))
        except Exception:
            d["metadata"] = {}
        return d


vault = QuestionRepository()
