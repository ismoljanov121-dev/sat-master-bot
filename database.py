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

db = Database()
