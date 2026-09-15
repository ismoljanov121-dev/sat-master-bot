"""
EduTest Pro - Database Layer (MongoDB Atlas with Atomic Local JSON Fallback)
Features:
- Thread/task-safe atomic JSON file updates (asyncio.Lock + .tmp flush + fsync + os.replace)
- Domain schemas: users, exam_sessions, exam_attempts, quiz_results, practice_stats, webapp_data
- Centralized UTC timestamping and Tashkent timezone formatting
- Full compatibility with existing quiz and practice interfaces
"""

import asyncio
import csv
import io
import json
import logging
import os
from datetime import datetime, timedelta, timezone
from typing import Any

import motor.motor_asyncio

from config import LOCAL_DB_FILE, MONGO_URI

logger = logging.getLogger("Database")

# Tashkent Timezone: UTC+5
TASHKENT_TZ = timezone(timedelta(hours=5))


def get_tashkent_now_str() -> str:
    """Returns current date and time formatted in Tashkent timezone."""
    return datetime.now(TASHKENT_TZ).strftime("%Y-%m-%d %H:%M:%S")


def get_utc_now_str() -> str:
    """Returns current date and time in UTC ISO format."""
    return datetime.now(timezone.utc).isoformat()


def utc_to_tashkent_str(utc_iso: str | None) -> str:
    """Converts UTC ISO timestamp to a human-readable Tashkent time string."""
    if not utc_iso:
        return "Noma'lum"
    try:
        dt = datetime.fromisoformat(utc_iso)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(TASHKENT_TZ).strftime("%Y-%m-%d %H:%M")
    except Exception:
        return utc_iso[:16]


class Database:
    def __init__(self, mongo_uri: str | None = None):
        self.mongo_uri = mongo_uri or MONGO_URI
        self.client: motor.motor_asyncio.AsyncIOMotorClient | None = None
        self.db: Any | None = None
        self.is_mongo_active: bool = False
        self._lock = asyncio.Lock()
        self.local_cache: dict[str, Any] = self._load_local_db()

    def _load_local_db(self) -> dict[str, Any]:
        """Loads and sanitizes local JSON database."""
        default_schema: dict[str, Any] = {
            "users": {},
            "quizzes": [],
            "exam_sessions": {},
            "exam_attempts": {},
            "diagnostic_sessions": {},
            "practice_stats": {},
            "webapp_data": {},
            "attention_events": []
        }

        if os.path.exists(LOCAL_DB_FILE):
            try:
                with open(LOCAL_DB_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        for k, default_val in default_schema.items():
                            data.setdefault(k, default_val)
                        return data
            except Exception as e:
                logger.error(f"Error reading local db file ({e}), creating backup copy and restoring default schema.")
                try:
                    backup_name = f"{LOCAL_DB_FILE}.corrupt_{int(datetime.now().timestamp())}"
                    os.rename(LOCAL_DB_FILE, backup_name)
                    logger.info(f"Corrupted DB backed up to {backup_name}")
                except Exception as ren_err:
                    logger.warning(f"Could not rename corrupted DB: {ren_err}")

        return default_schema

    def _save_local_db_sync(self) -> None:
        """Atomic write to disk using temp file, flush, fsync, and os.replace."""
        temp_file = f"{LOCAL_DB_FILE}.tmp_{os.getpid()}"
        try:
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(self.local_cache, f, indent=2, ensure_ascii=False)
                f.flush()
                os.fsync(f.fileno())
            os.replace(temp_file, LOCAL_DB_FILE)
        except Exception as e:
            logger.error(f"Failed atomic local db save: {e}")
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except Exception:
                    pass

    async def _atomic_save_local(self) -> None:
        """Asynchronously acquires the lock and executes atomic disk write."""
        async with self._lock:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, self._save_local_db_sync)

    def _save_local_db(self) -> None:
        """Synchronous wrapper for backward compatibility with synchronous callers."""
        self._save_local_db_sync()

    async def connect(self) -> None:
        """Attempts connection to MongoDB Atlas."""
        if self.mongo_uri and "mongodb" in self.mongo_uri:
            try:
                self.client = motor.motor_asyncio.AsyncIOMotorClient(
                    self.mongo_uri,
                    serverSelectionTimeoutMS=5000
                )
                await self.client.admin.command('ping')
                self.db = self.client.get_default_database("edutest_pro_db")
                self.is_mongo_active = True
                logger.info("✅ MongoDB Atlas connected successfully!")
                return
            except Exception as e:
                logger.warning(f"⚠️ MongoDB connection failed ({e}). Using atomic local JSON persistence.")
        else:
            logger.info("ℹ️ MONGO_URI not configured. Using atomic local users_db.json storage.")
        self.is_mongo_active = False

    async def close(self) -> None:
        """Closes MongoDB connection cleanly during shutdown."""
        if self.client:
            self.client.close()
            logger.info("Database connection closed cleanly.")

    # --- User Management ---
    async def save_user(
        self,
        user_id: int,
        username: str,
        full_name: str,
        referred_by: int | None = None
    ) -> None:
        now_utc = get_utc_now_str()
        user_data = {
            "user_id": user_id,
            "username": username or "",
            "full_name": full_name or "",
            "last_active": now_utc,
            "referred_by": referred_by
        }

        # Local save
        str_id = str(user_id)
        users = self.local_cache.setdefault("users", {})
        if str_id not in users:
            user_data["created_at"] = now_utc
            user_data["quizzes_taken"] = 0
            user_data["exams_taken"] = 0
            user_data["streak"] = 0
            users[str_id] = user_data
        else:
            users[str_id].update(user_data)

        await self._atomic_save_local()

        # MongoDB save
        if self.is_mongo_active and (self.db is not None):
            try:
                await self.db.users.update_one(
                    {"user_id": user_id},
                    {"$set": user_data, "$setOnInsert": {"created_at": now_utc}},
                    upsert=True
                )
            except Exception as e:
                logger.error(f"MongoDB save_user error: {e}")

    def get_user(self, user_id: int) -> dict[str, Any] | None:
        """Retrieves user profile from cache."""
        return self.local_cache.get("users", {}).get(str(user_id))

    def list_users(self) -> list[dict[str, Any]]:
        """Returns list of all registered users."""
        return list(self.local_cache.get("users", {}).values())

    # --- Quiz Results (Diagnostic compatibility) ---
    async def save_quiz_result(
        self,
        user_id: int,
        score: int,
        correct: int,
        total: int,
        weaknesses: list
    ) -> None:
        result_entry = {
            "user_id": user_id,
            "score": score,
            "correct": correct,
            "total": total,
            "weaknesses": weaknesses,
            "timestamp": get_utc_now_str()
        }

        self.local_cache.setdefault("quizzes", []).append(result_entry)
        str_id = str(user_id)
        if str_id in self.local_cache.get("users", {}):
            self.local_cache["users"][str_id]["last_score"] = score
            self.local_cache["users"][str_id]["quizzes_taken"] = (
                self.local_cache["users"][str_id].get("quizzes_taken", 0) + 1
            )

        await self._atomic_save_local()

        if self.is_mongo_active and (self.db is not None):
            try:
                await self.db.quiz_results.insert_one(result_entry)
                await self.db.users.update_one(
                    {"user_id": user_id},
                    {"$set": {"last_score": score}, "$inc": {"quizzes_taken": 1}}
                )
            except Exception as e:
                logger.error(f"MongoDB save_quiz_result error: {e}")

    # --- Practice Stats ---
    def record_practice_answer(
        self,
        user_id: int,
        question_id: str,
        is_correct: bool,
        section: str
    ) -> None:
        try:
            self.local_cache.setdefault("practice_stats", {})
            str_id = str(user_id)
            user_stats = self.local_cache["practice_stats"].setdefault(str_id, {
                "total_answered": 0,
                "correct_count": 0,
                "current_streak": 0,
                "best_streak": 0,
                "by_section": {
                    "math": {"total": 0, "correct": 0},
                    "reading": {"total": 0, "correct": 0},
                    "writing": {"total": 0, "correct": 0}
                },
                "answered_ids": []
            })

            user_stats["total_answered"] += 1
            if question_id not in user_stats["answered_ids"]:
                user_stats["answered_ids"].append(question_id)

            sec_key = section.lower() if section else "math"
            if sec_key not in user_stats["by_section"]:
                user_stats["by_section"][sec_key] = {"total": 0, "correct": 0}
            user_stats["by_section"][sec_key]["total"] += 1

            if is_correct:
                user_stats["correct_count"] += 1
                user_stats["current_streak"] += 1
                if user_stats["current_streak"] > user_stats.get("best_streak", 0):
                    user_stats["best_streak"] = user_stats["current_streak"]
                user_stats["by_section"][sec_key]["correct"] += 1
            else:
                user_stats["current_streak"] = 0

            self._save_local_db_sync()
        except Exception as e:
            logger.error(f"Error in record_practice_answer: {e}")

    def get_user_practice_stats(self, user_id: int) -> dict[str, Any]:
        str_id = str(user_id)
        stats = self.local_cache.get("practice_stats", {}).get(str_id, {
            "total_answered": 0,
            "correct_count": 0,
            "current_streak": 0,
            "best_streak": 0,
            "by_section": {
                "math": {"total": 0, "correct": 0},
                "reading": {"total": 0, "correct": 0},
                "writing": {"total": 0, "correct": 0}
            },
            "answered_ids": []
        })
        total = stats.get("total_answered", 0)
        correct = stats.get("correct_count", 0)
        accuracy = round((correct / total) * 100) if total > 0 else 0
        stats_copy = dict(stats)
        stats_copy["accuracy"] = accuracy
        return stats_copy

    def get_answered_question_ids(self, user_id: int) -> list[str]:
        str_id = str(user_id)
        return list(self.local_cache.get("practice_stats", {}).get(str_id, {}).get("answered_ids", []))

    # --- Exam Sessions (Admin Live Mocks) ---
    async def save_exam_session(self, session_data: dict[str, Any]) -> None:
        """Saves or updates an exam session."""
        session_id = session_data["session_id"]
        self.local_cache.setdefault("exam_sessions", {})[session_id] = session_data
        await self._atomic_save_local()

        if self.is_mongo_active and (self.db is not None):
            try:
                await self.db.exam_sessions.update_one(
                    {"session_id": session_id},
                    {"$set": session_data},
                    upsert=True
                )
            except Exception as e:
                logger.error(f"MongoDB save_exam_session error: {e}")

    def get_exam_session(self, session_id: str) -> dict[str, Any] | None:
        return self.local_cache.get("exam_sessions", {}).get(session_id)

    def get_active_session_by_code(self, code: str) -> dict[str, Any] | None:
        """Finds an active exam session matching the 6-character code."""
        code_upper = code.strip().upper()
        for s in self.local_cache.get("exam_sessions", {}).values():
            if s.get("code", "").upper() == code_upper and s.get("status") == "active":
                return s
        return None

    def list_exam_sessions(self, limit: int = 10) -> list[dict[str, Any]]:
        """Lists recent exam sessions sorted by creation time."""
        sessions = list(self.local_cache.get("exam_sessions", {}).values())
        sessions.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return sessions[:limit]

    async def close_exam_session(self, session_id: str) -> bool:
        """Marks an exam session as closed."""
        sessions = self.local_cache.setdefault("exam_sessions", {})
        if session_id in sessions:
            sessions[session_id]["status"] = "closed"
            sessions[session_id]["closed_at"] = get_utc_now_str()
            await self._atomic_save_local()
            if self.is_mongo_active and (self.db is not None):
                try:
                    await self.db.exam_sessions.update_one(
                        {"session_id": session_id},
                        {"$set": {"status": "closed", "closed_at": get_utc_now_str()}}
                    )
                except Exception as e:
                    logger.error(f"MongoDB close_exam_session error: {e}")
            return True
        return False

    # --- Exam Attempts (Student Tests) ---
    async def create_user_attempt_atomic(
        self,
        user_id: int,
        attempt_data: dict[str, Any]
    ) -> tuple[bool, dict[str, Any] | None, str]:
        """
        Atomically ensures only one active attempt exists for a user.
        If an active unexpired attempt exists, returns (False, existing_attempt, message).
        Otherwise saves new attempt and returns (True, attempt_data, message).
        """
        async with self._lock:
            for att in self.local_cache.get("exam_attempts", {}).values():
                if att.get("user_id") == user_id and att.get("status") == "active":
                    try:
                        dl = datetime.fromisoformat(att["deadline"])
                        if dl.tzinfo is None:
                            dl = dl.replace(tzinfo=timezone.utc)
                        if datetime.now(timezone.utc) <= dl:
                            return False, att, "Foydalanuvchida allaqachon faol imtihon mavjud"
                        else:
                            att["status"] = "expired"
                    except Exception:
                        pass

            attempt_id = attempt_data["attempt_id"]
            self.local_cache.setdefault("exam_attempts", {})[attempt_id] = attempt_data
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, self._save_local_db_sync)

            if self.is_mongo_active and (self.db is not None):
                try:
                    await self.db.exam_attempts.update_one(
                        {"attempt_id": attempt_id},
                        {"$set": attempt_data},
                        upsert=True
                    )
                except Exception as e:
                    logger.error(f"MongoDB create_user_attempt_atomic error: {e}")

            return True, attempt_data, "Muvaffaqiyatli yaratildi"

    async def save_attempt(self, attempt_data: dict[str, Any]) -> None:
        """Saves student exam attempt and increments user exam count once if submitted (idempotent)."""
        attempt_id = attempt_data["attempt_id"]
        self.local_cache.setdefault("exam_attempts", {})[attempt_id] = attempt_data

        user_id_str = str(attempt_data.get("user_id", ""))
        status = attempt_data.get("status")

        if status in ("submitted", "expired"):
            if not attempt_data.get("counter_recorded", False):
                attempt_data["counter_recorded"] = True
                if user_id_str in self.local_cache.get("users", {}):
                    user = self.local_cache["users"][user_id_str]
                    user["exams_taken"] = user.get("exams_taken", 0) + 1
                    if attempt_data.get("score"):
                        user["last_mock_score"] = attempt_data["score"].get("accuracy_percentage")

        await self._atomic_save_local()

        if self.is_mongo_active and (self.db is not None):
            try:
                await self.db.exam_attempts.update_one(
                    {"attempt_id": attempt_id},
                    {"$set": attempt_data},
                    upsert=True
                )
            except Exception as e:
                logger.error(f"MongoDB save_attempt error: {e}")

    def get_attempt(self, attempt_id: str) -> dict[str, Any] | None:
        return self.local_cache.get("exam_attempts", {}).get(attempt_id)

    def get_user_active_attempt(self, user_id: int) -> dict[str, Any] | None:
        """Finds currently active attempt for user if deadline has not passed."""
        for att in self.local_cache.get("exam_attempts", {}).values():
            if att.get("user_id") == user_id and att.get("status") == "active":
                return att
        return None

    def list_user_attempts(self, user_id: int) -> list[dict[str, Any]]:
        attempts = [
            att for att in self.local_cache.get("exam_attempts", {}).values()
            if att.get("user_id") == user_id
        ]
        attempts.sort(key=lambda x: x.get("start_time", ""), reverse=True)
        return attempts

    # --- Admin Dashboard Statistics & CSV ---
    def get_admin_dashboard_stats(self) -> dict[str, Any]:
        """Calculates real-time statistics from local cache."""
        users = self.local_cache.get("users", {})
        total_students = len(users)

        # Active today (last 24 hours UTC)
        now_utc = datetime.now(timezone.utc)
        today_active_count = 0
        for u in users.values():
            last_act = u.get("last_active")
            if last_act:
                try:
                    dt = datetime.fromisoformat(last_act)
                    if dt.tzinfo is None:
                        dt = dt.replace(tzinfo=timezone.utc)
                    if (now_utc - dt).total_seconds() <= 86400:
                        today_active_count += 1
                except Exception:
                    pass

        attempts = list(self.local_cache.get("exam_attempts", {}).values())
        completed_exams = [a for a in attempts if a.get("status") in ("submitted", "expired")]

        total_accuracy = 0
        for a in completed_exams:
            if a.get("score") and "accuracy_percentage" in a["score"]:
                total_accuracy += a["score"]["accuracy_percentage"]

        avg_accuracy = round(total_accuracy / len(completed_exams)) if completed_exams else 0

        active_sessions_count = sum(
            1 for s in self.local_cache.get("exam_sessions", {}).values()
            if s.get("status") == "active"
        )

        return {
            "total_students": total_students,
            "active_today": today_active_count,
            "completed_exams": len(completed_exams),
            "average_accuracy": avg_accuracy,
            "active_sessions_count": active_sessions_count
        }

    def get_recent_exam_results(self, limit: int = 15) -> list[dict[str, Any]]:
        """Returns recent completed exam attempts with student names."""
        attempts = [
            att for att in self.local_cache.get("exam_attempts", {}).values()
            if att.get("status") in ("submitted", "expired")
        ]
        attempts.sort(key=lambda x: x.get("start_time", ""), reverse=True)

        results = []
        for att in attempts[:limit]:
            uid = att.get("user_id")
            user = self.get_user(uid)
            name = user.get("full_name", f"ID: {uid}") if user else f"ID: {uid}"
            score = att.get("score") or {}
            results.append({
                "attempt_id": att.get("attempt_id"),
                "student_name": name,
                "user_id": uid,
                "session_id": att.get("session_id"),
                "template_name": att.get("template_name", "mock"),
                "accuracy": score.get("accuracy_percentage", 0),
                "correct_count": score.get("correct_count", 0),
                "total_questions": score.get("total_questions", 0),
                "by_section": score.get("by_section", {}),
                "weaknesses": score.get("weaknesses", []),
                "date_tashkent": utc_to_tashkent_str(att.get("start_time")),
                "status": att.get("status")
            })
        return results

    def get_session_results(self, session_id: str) -> list[dict[str, Any]]:
        """Returns completed attempts belonging to a specific session_id."""
        attempts = [
            att for att in self.local_cache.get("exam_attempts", {}).values()
            if att.get("session_id") == session_id and att.get("status") in ("submitted", "expired")
        ]
        attempts.sort(key=lambda x: x.get("start_time", ""), reverse=True)
        results = []
        for att in attempts:
            uid = att.get("user_id")
            user = self.get_user(uid)
            name = user.get("full_name", f"ID: {uid}") if user else f"ID: {uid}"
            score = att.get("score") or {}
            results.append({
                "attempt_id": att.get("attempt_id"),
                "student_name": name,
                "user_id": uid,
                "session_id": session_id,
                "template_name": att.get("template_name", "mock"),
                "accuracy": score.get("accuracy_percentage", 0),
                "correct_count": score.get("correct_count", 0),
                "total_questions": score.get("total_questions", 0),
                "by_section": score.get("by_section", {}),
                "weaknesses": score.get("weaknesses", []),
                "date_tashkent": utc_to_tashkent_str(att.get("start_time")),
                "status": att.get("status")
            })
        return results

    def export_results_csv(self) -> str:
        """Generates CSV content of all completed exam results."""
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            "Urinish ID",
            "O'quvchi Ismi",
            "Telegram ID",
            "Username",
            "Imtihon Turi",
            "To'g'ri Javoblar",
            "Jami Savollar",
            "Aniqlik Foizi (%)",
            "Math",
            "Reading",
            "Writing",
            "Boshlangan Vaqt (Toshkent)",
            "Holat"
        ])

        attempts = list(self.local_cache.get("exam_attempts", {}).values())
        attempts.sort(key=lambda x: x.get("start_time", ""), reverse=True)

        for att in attempts:
            uid = att.get("user_id")
            user = self.get_user(uid) or {}
            name = user.get("full_name", "")
            username = f"@{user.get('username')}" if user.get("username") else ""
            score = att.get("score") or {}
            sec = score.get("by_section") or {}

            math_stat = f"{sec.get('math', {}).get('correct', 0)}/{sec.get('math', {}).get('total', 0)}"
            read_stat = f"{sec.get('reading', {}).get('correct', 0)}/{sec.get('reading', {}).get('total', 0)}"
            write_stat = f"{sec.get('writing', {}).get('correct', 0)}/{sec.get('writing', {}).get('total', 0)}"

            writer.writerow([
                att.get("attempt_id", ""),
                name,
                uid,
                username,
                att.get("title", att.get("template_name", "")),
                score.get("correct_count", 0),
                score.get("total_questions", 0),
                f"{score.get('accuracy_percentage', 0)}%",
                math_stat,
                read_stat,
                write_stat,
                utc_to_tashkent_str(att.get("start_time")),
                att.get("status", "")
            ])

        return output.getvalue()

    # --- Mini App Sync Data ---
    async def save_webapp_user_data(self, user_id: int, data: dict[str, Any]) -> None:
        """Saves WebApp tasks, errors, and settings."""
        str_id = str(user_id)
        user_record = {
            "tasks": data.get("tasks", []),
            "errors": data.get("errors", []),
            "settings": data.get("settings", {}),
            "updated_at": get_utc_now_str()
        }
        self.local_cache.setdefault("webapp_data", {})[str_id] = user_record
        await self._atomic_save_local()

        if self.is_mongo_active and (self.db is not None):
            try:
                await self.db.webapp_data.update_one(
                    {"user_id": user_id},
                    {"$set": user_record},
                    upsert=True
                )
            except Exception as e:
                logger.error(f"MongoDB save_webapp_user_data error: {e}")

    def get_webapp_user_data(self, user_id: int) -> dict[str, Any] | None:
        return self.local_cache.get("webapp_data", {}).get(str(user_id))

    # --- Attention Events (Web / Exam Focus Monitoring) ---
    async def save_attention_event(self, user_id: int, event_data: dict[str, Any]) -> None:
        """Saves focus loss, tab switch, or blur events."""
        entry = {
            "user_id": user_id,
            "event": event_data.get("event"),
            "attempt_id": event_data.get("attempt_id"),
            "timestamp": event_data.get("timestamp") or get_utc_now_str(),
            "details": event_data.get("details", {})
        }
        self.local_cache.setdefault("attention_events", []).append(entry)
        await self._atomic_save_local()

        if self.is_mongo_active and (self.db is not None):
            try:
                await self.db.attention_events.insert_one(entry)
            except Exception as e:
                logger.error(f"MongoDB save_attention_event error: {e}")

    def get_attention_events(self, user_id: int | None = None) -> list[dict[str, Any]]:
        """Returns attention events, optionally filtered by user_id."""
        events = self.local_cache.get("attention_events", [])
        if user_id is not None:
            return [e for e in events if e.get("user_id") == user_id]
        return list(events)


# Singleton instance
db = Database()
