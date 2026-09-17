"""
EduTest Pro - Adaptive Study Plan Service
Generates, tracks, and dynamically rebalances personal SAT prep schedules based on:
- Target exam date (e.g. 2026-11-01)
- Daily allocated time (15, 30, 45, 60 minutes)
- Diagnostic baseline score
- Live attempt accuracy across the 4 Math and 4 Reading/Writing domains
Includes transparent pedagogical rationale for every recommended study topic.
"""

from datetime import datetime, timedelta, timezone
import logging
from typing import Any

from database import TASHKENT_TZ, db, get_tashkent_now_str, get_utc_now_str
from services.question_repository import vault

logger = logging.getLogger("StudyPlanService")

# Official Domain Architecture
DOMAINS = {
    "math": [
        "Algebra",
        "Advanced Math",
        "Problem-Solving and Data Analysis",
        "Geometry and Trigonometry"
    ],
    "reading_writing": [
        "Craft and Structure",
        "Information and Ideas",
        "Standard English Conventions",
        "Expression of Ideas"
    ]
}


class AdaptiveStudyPlanService:
    def create_or_update_plan(
        self,
        user_id: int,
        target_exam_date: str | None = None,
        daily_minutes: int = 30,
        target_score: int = 1400
    ) -> dict[str, Any]:
        """Creates a customized weekly study plan for the student."""
        now = datetime.now(TASHKENT_TZ)
        if not target_exam_date:
            # Default target: 6 weeks from today
            target_dt = now + timedelta(days=42)
            target_exam_date = target_dt.strftime("%Y-%m-%d")
        else:
            try:
                target_dt = datetime.strptime(target_exam_date, "%Y-%m-%d").replace(tzinfo=TASHKENT_TZ)
            except Exception:
                target_dt = now + timedelta(days=42)
                target_exam_date = target_dt.strftime("%Y-%m-%d")

        days_remaining = max(1, (target_dt.date() - now.date()).days)
        weeks_remaining = max(1, (days_remaining + 6) // 7)

        # Calculate daily question quota based on study minutes (approx 1.5 - 2 min/question)
        suggested_daily_q = max(10, min(50, int(daily_minutes / 1.5)))

        # Diagnose weak domains from user's past attempts
        weak_domains = self._identify_weak_domains(user_id)

        # Generate weekly milestones
        weekly_focus = []
        for w in range(1, min(7, weeks_remaining + 1)):
            focus_domain = weak_domains[(w - 1) % len(weak_domains)]
            weekly_focus.append({
                "week_number": w,
                "focus_domain": focus_domain["domain"],
                "section": focus_domain["section"],
                "target_accuracy": "80%",
                "recommended_drills": f"Kunlik {suggested_daily_q} ta savol + 1 ta xatolar tahlili"
            })

        plan = {
            "user_id": user_id,
            "target_exam_date": target_exam_date,
            "days_remaining": days_remaining,
            "weeks_remaining": weeks_remaining,
            "daily_minutes": daily_minutes,
            "daily_question_goal": suggested_daily_q,
            "target_score": target_score,
            "current_focus_domain": weak_domains[0]["domain"],
            "current_focus_section": weak_domains[0]["section"],
            "recommendation_rationale": weak_domains[0]["rationale"],
            "weekly_schedule": weekly_focus,
            "created_at": get_utc_now_str(),
            "updated_at": get_utc_now_str()
        }

        db.local_cache.setdefault("study_plans", {})[str(user_id)] = plan
        db._save_local_db_sync()
        return plan

    def get_plan(self, user_id: int) -> dict[str, Any]:
        """Retrieves or lazily initializes the user's study plan."""
        plan = db.get_user_study_plan(user_id)
        if not plan:
            plan = self.create_or_update_plan(user_id)
        return plan

    def rebalance_plan(self, user_id: int) -> dict[str, Any]:
        """
        Dynamically adjusts plan when student misses days or shows significant mastery / struggles.
        """
        plan = self.get_plan(user_id)
        weak_domains = self._identify_weak_domains(user_id)

        # Update primary focus and rationale
        primary = weak_domains[0]
        plan["current_focus_domain"] = primary["domain"]
        plan["current_focus_section"] = primary["section"]
        plan["recommendation_rationale"] = (
            f"🔄 Reja yangilandi: {primary['rationale']} "
            f"Haftalik mashqlar ushbu ko'nikmani mustahkamlashga qaratildi."
        )
        plan["updated_at"] = get_utc_now_str()

        db.local_cache.setdefault("study_plans", {})[str(user_id)] = plan
        db._save_local_db_sync()
        return plan

    def _identify_weak_domains(self, user_id: int) -> list[dict[str, Any]]:
        """Analyzes attempts history and error notebook to rank weak areas."""
        history = db.get_user_pacing_history(user_id, limit=200)
        unresolved_mistakes = db.get_user_mistakes(user_id, resolved_filter=False)

        domain_stats: dict[str, dict[str, int]] = {}

        # Register all domains
        for sec, dom_list in DOMAINS.items():
            for dom in dom_list:
                domain_stats[dom] = {"total": 0, "correct": 0, "section": sec}

        for att in history:
            dom = att.get("domain")
            if dom in domain_stats:
                domain_stats[dom]["total"] += 1
                if att.get("is_correct"):
                    domain_stats[dom]["correct"] += 1

        # Penalize domains with unresolved mistakes
        for m in unresolved_mistakes:
            dom = m.get("domain")
            if dom in domain_stats:
                domain_stats[dom]["total"] += 2  # Weight unresolved mistakes heavier

        # Rank domains by accuracy (lowest first)
        ranked = []
        for dom, stats in domain_stats.items():
            tot = stats["total"]
            corr = stats["correct"]
            acc = (corr / tot) if tot > 0 else 0.5  # default 50% if unattempted
            ranked.append({
                "domain": dom,
                "section": stats["section"],
                "total_attempts": tot,
                "accuracy": acc
            })

        ranked.sort(key=lambda x: x["accuracy"])

        result = []
        for item in ranked:
            dom = item["domain"]
            tot = item["total_attempts"]
            acc_pct = int(item["accuracy"] * 100)
            if tot == 0:
                rationale = f"'{dom}' mavzusida hali mashq bajarilmadi. Asosiy ko'nikmalarni tekshirib olish zarur."
            elif acc_pct < 65:
                rationale = f"'{dom}' bo'limida aniqlik {acc_pct}% bo'lib, eng ko'p ball yo'qotilgan soha hisoblanadi."
            else:
                rationale = f"'{dom}' bo'limida aniqlik {acc_pct}%. Mavzuni mustahkamlash tavsiya etiladi."

            result.append({
                "domain": dom,
                "section": item["section"],
                "rationale": rationale,
                "accuracy_pct": acc_pct
            })

        return result


study_planner = AdaptiveStudyPlanService()
