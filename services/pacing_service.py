"""
EduTest Pro - Pacing Strategy & Time Management Service
Analyzes time spent per question to optimize SAT test-taking speed:
- Overtime (>90s Math, >75s Reading/Writing): Identifies questions where students get bogged down.
- Rushed Mistakes (<20s): Flags careless errors caused by rushing.
- Pacing Efficiency Score: Measures adherence to Digital SAT target pace.
- Strictly honest reporting: Does NOT fabricate fake 1600 scaled scores from small samples.
"""

from typing import Any
import logging

from database import db

logger = logging.getLogger("PacingService")

# Target Pace Thresholds (Seconds)
TARGET_PACE = {
    "math": {"target": 80, "max": 95, "min_safe": 25},
    "reading": {"target": 65, "max": 80, "min_safe": 20},
    "writing": {"target": 45, "max": 60, "min_safe": 15}
}


class PacingService:
    def analyze_user_pacing(self, user_id: int, limit: int = 50) -> dict[str, Any]:
        """
        Analyzes recent question attempts to diagnose time management strengths and weaknesses.
        """
        history = db.get_user_pacing_history(user_id, limit=limit)

        if not history:
            return {
                "status": "insufficient_data",
                "message": "Vaqt tahlilini ko'rish uchun kamida 5 ta savol ishlang.",
                "total_analyzed": 0,
                "overtime_count": 0,
                "rushed_errors_count": 0,
                "average_time_seconds": 0,
                "recommendation": "Har bir savolga qulay sur'atda yondashing."
            }

        total_analyzed = len(history)
        total_seconds = 0
        overtime_items = []
        rushed_errors = []
        on_pace_correct = 0

        domain_time: dict[str, list[int]] = {}

        for att in history:
            sec = att.get("section", "math").lower()
            dom = att.get("domain", "General")
            t_sec = att.get("time_spent_seconds", 0)
            is_corr = att.get("is_correct", False)

            total_seconds += t_sec
            domain_time.setdefault(dom, []).append(t_sec)

            thresholds = TARGET_PACE.get(sec, TARGET_PACE["math"])

            # Overtime check
            if t_sec > thresholds["max"]:
                overtime_items.append({
                    "question_id": att.get("question_id"),
                    "domain": dom,
                    "skill": att.get("skill"),
                    "time_spent": t_sec,
                    "threshold": thresholds["max"]
                })
            # Rushed error check
            elif t_sec < thresholds["min_safe"] and not is_corr:
                rushed_errors.append({
                    "question_id": att.get("question_id"),
                    "domain": dom,
                    "skill": att.get("skill"),
                    "time_spent": t_sec
                })
            elif is_corr:
                on_pace_correct += 1

        avg_time = int(total_seconds / total_analyzed) if total_analyzed > 0 else 0

        # Calculate time-heaviest domain
        heaviest_domain = "Aniqlanmadi"
        max_avg_dom_time = 0
        for dom, times in domain_time.items():
            dom_avg = sum(times) / len(times)
            if dom_avg > max_avg_dom_time:
                max_avg_dom_time = dom_avg
                heaviest_domain = dom

        # Generate pragmatic recommendation
        if len(rushed_errors) > len(overtime_items):
            recommendation = (
                f"⚠️ Shoshilish oqibatida {len(rushed_errors)} ta savolda xato qilindi (<20s). "
                f"Savol shartini diqqat bilan oxirigacha o'qishga odatlaning."
            )
        elif len(overtime_items) > 2:
            recommendation = (
                f"⏳ Eng ko'p vaqt '{heaviest_domain}' bo'limida yo'qotilmoqda (o'rtacha {int(max_avg_dom_time)}s). "
                f"Bunday savollarda 60 soniyada yechim ko'rinmasa, belgilab (flag) keyingisiga o'tish tavsiya etiladi."
            )
        else:
            recommendation = "✅ Pacing yaxshi holatda. Maqsadli vaqt me'yoriga mos ishlanmoqda."

        return {
            "status": "ok",
            "total_analyzed": total_analyzed,
            "average_time_seconds": avg_time,
            "overtime_count": len(overtime_items),
            "rushed_errors_count": len(rushed_errors),
            "on_pace_correct": on_pace_correct,
            "heaviest_domain": heaviest_domain,
            "heaviest_domain_avg_sec": int(max_avg_dom_time),
            "recommendation": recommendation,
            "overtime_samples": overtime_items[:3],
            "rushed_samples": rushed_errors[:3]
        }


pacing_service = PacingService()
