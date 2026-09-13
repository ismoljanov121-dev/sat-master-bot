"""
SAT AI Bot - Database Layer (MongoDB Atlas with Local JSON Fallback)
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, Optional, Any
import motor.motor_asyncio

logger = logging.getLogger("Database")

LOCAL_DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users_db.json")

class Database:
    def __init__(self, mongo_uri: Optional[str] = None):
        self.mongo_uri = mongo_uri or os.getenv("MONGO_URI", "").strip()
        self.client = None
        self.db = None
        self.is_mongo_active = False
        self.local_cache = self._load_local_db()

    def _load_local_db(self) -> Dict[str, Any]:
        if os.path.exists(LOCAL_DB_FILE):
            try:
                with open(LOCAL_DB_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Error reading local db: {e}")
        return {"users": {}, "quizzes": []}

    def _save_local_db(self):
        try:
            with open(LOCAL_DB_FILE, "w", encoding="utf-8") as f:
                json.dump(self.local_cache, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save local db: {e}")

    async def connect(self):
        """Attempts connection to MongoDB Atlas."""
        if self.mongo_uri and "mongodb" in self.mongo_uri:
            try:
                self.client = motor.motor_asyncio.AsyncIOMotorClient(self.mongo_uri, serverSelectionTimeoutMS=5000)
                # Test ping
                await self.client.admin.command('ping')
                self.db = self.client.get_default_database("sat_master_db")
                self.is_mongo_active = True
                logger.info("✅ MongoDB Atlas connected successfully!")
                return
            except Exception as e:
                logger.warning(f"⚠️ MongoDB Atlas connection failed ({e}). Falling back to local users_db.json.")
        else:
            logger.info("ℹ️ MONGO_URI not configured. Using local users_db.json storage.")
        self.is_mongo_active = False

    async def save_user(self, user_id: int, username: str, full_name: str, referred_by: Optional[int] = None):
        user_data = {
            "user_id": user_id,
            "username": username or "",
            "full_name": full_name or "",
            "last_active": datetime.utcnow().isoformat(),
            "referred_by": referred_by
        }
        # Local save
        try:
            self.local_cache.setdefault("users", {})
            self.local_cache.setdefault("quizzes", [])
            str_id = str(user_id)
            if str_id not in self.local_cache["users"]:
                user_data["created_at"] = datetime.utcnow().isoformat()
                user_data["quizzes_taken"] = 0
                user_data["streak"] = 0
                self.local_cache["users"][str_id] = user_data
            else:
                self.local_cache["users"][str_id].update(user_data)
            self._save_local_db()
        except Exception as e:
            logger.error(f"Local save_user error: {e}")

        # MongoDB save
        if self.is_mongo_active and (self.db is not None):
            try:
                await self.db.users.update_one(
                    {"user_id": user_id},
                    {"$set": user_data, "$setOnInsert": {"created_at": datetime.utcnow().isoformat()}},
                    upsert=True
                )
            except Exception as e:
                logger.error(f"MongoDB save_user error: {e}")

    async def save_quiz_result(self, user_id: int, score: int, correct: int, total: int, weaknesses: list):
        result_entry = {
            "user_id": user_id,
            "score": score,
            "correct": correct,
            "total": total,
            "weaknesses": weaknesses,
            "timestamp": datetime.utcnow().isoformat()
        }
        # Local save
        try:
            self.local_cache.setdefault("users", {})
            self.local_cache.setdefault("quizzes", [])
            self.local_cache["quizzes"].append(result_entry)
            str_id = str(user_id)
            if str_id in self.local_cache["users"]:
                self.local_cache["users"][str_id]["last_score"] = score
                self.local_cache["users"][str_id]["quizzes_taken"] = self.local_cache["users"][str_id].get("quizzes_taken", 0) + 1
            self._save_local_db()
        except Exception as e:
            logger.error(f"Local save_quiz_result error: {e}")

        # MongoDB save
        if self.is_mongo_active and (self.db is not None):
            try:
                await self.db.quiz_results.insert_one(result_entry)
                await self.db.users.update_one(
                    {"user_id": user_id},
                    {"$set": {"last_score": score}, "$inc": {"quizzes_taken": 1}}
                )
            except Exception as e:
                logger.error(f"MongoDB save_quiz_result error: {e}")

    def record_practice_answer(self, user_id: int, question_id: str, is_correct: bool, section: str):
        """Records a user's answer in practice mode and updates streak and accuracy."""
        try:
            self.local_cache.setdefault("practice_stats", {})
            str_id = str(user_id)
            user_stats = self.local_cache["practice_stats"].setdefault(str_id, {
                "total_answered": 0,
                "correct_count": 0,
                "current_streak": 0,
                "best_streak": 0,
                "by_section": {"math": {"total": 0, "correct": 0}, "reading": {"total": 0, "correct": 0}, "writing": {"total": 0, "correct": 0}},
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

            self._save_local_db()
        except Exception as e:
            logger.error(f"Error in record_practice_answer: {e}")

    def get_user_practice_stats(self, user_id: int) -> dict:
        """Retrieves user practice statistics."""
        str_id = str(user_id)
        stats = self.local_cache.get("practice_stats", {}).get(str_id, {
            "total_answered": 0,
            "correct_count": 0,
            "current_streak": 0,
            "best_streak": 0,
            "by_section": {"math": {"total": 0, "correct": 0}, "reading": {"total": 0, "correct": 0}, "writing": {"total": 0, "correct": 0}},
            "answered_ids": []
        })
        total = stats.get("total_answered", 0)
        correct = stats.get("correct_count", 0)
        accuracy = round((correct / total) * 100) if total > 0 else 0
        stats["accuracy"] = accuracy
        return stats

    def get_answered_question_ids(self, user_id: int) -> list:
        """Returns list of question IDs answered by user."""
        str_id = str(user_id)
        return self.local_cache.get("practice_stats", {}).get(str_id, {}).get("answered_ids", [])

db = Database()

