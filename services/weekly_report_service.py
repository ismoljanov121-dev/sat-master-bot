"""
EduTest Pro - Pragmatic Weekly Report Service
Answers 3 essential questions with empirical data:
1. "Nima yaxshilandi?" (Measurable gains in accuracy and speed)
2. "Nima hali qiyin?" (Recurring error patterns and bottlenecks)
3. "Keyingi hafta nimani qilamiz?" (3 concrete, actionable weekly tasks)
Epistemic Honesty: If sample size < 15 questions, explicitly notifies the student
that more practice data is required before drawing firm conclusions.
"""

from typing import Any
import logging

from database import db

logger = logging.getLogger("WeeklyReportService")


class WeeklyReportService:
    def generate_weekly_report(self, user_id: int) -> dict[str, Any]:
        """
        Generates the 3-question pragmatic report for the student.
        """
        history = db.get_user_pacing_history(user_id, limit=100)
        unresolved_mistakes = db.get_user_mistakes(user_id, resolved_filter=False)

        total_questions = len(history)

        # Epistemic Honesty: Sample size check
        if total_questions < 15:
            return {
                "status": "preliminary",
                "total_questions": total_questions,
                "is_confident": False,
                "notice": (
                    f"Hozircha ishlangan savollar soni {total_questions} ta. "
                    f"To'liq va ishonchli haftalik xulosaga ega bo'lish uchun kamida 15 ta savol ishlang."
                ),
                "q1_what_improved": "Dastlabki mashqlar boshlandi. Muntazamlikni saqlab qoling.",
                "q2_what_is_difficult": "Xatolar yetarli darajada to'planmagan.",
                "q3_next_week_plan": [
                    "Har kuni 10 daqiqalik mashqni bajarish",
                    "Xatolar daftarchasidagi savollarni qayta ko'rib chiqish",
                    "Kamida 15 ta savol ishlab, to'liq hisobotni ochish"
                ]
            }

        # Analyze domain performance
        domain_performance: dict[str, dict[str, int]] = {}
        for att in history:
            dom = att.get("domain", "General")
            domain_performance.setdefault(dom, {"total": 0, "correct": 0})
            domain_performance[dom]["total"] += 1
            if att.get("is_correct"):
                domain_performance[dom]["correct"] += 1

        improved_domains = []
        difficult_domains = []

        for dom, stats in domain_performance.items():
            tot = stats["total"]
            corr = stats["correct"]
            acc = int((corr / tot) * 100) if tot > 0 else 0
            if acc >= 75 and tot >= 3:
                improved_domains.append(f"{dom} ({acc}% aniqlik)")
            elif acc < 60 and tot >= 3:
                difficult_domains.append(f"{dom} ({acc}% aniqlik, {tot - corr} ta xato)")

        # 1. Nima yaxshilandi?
        if improved_domains:
            q1_text = f"Quyidagi sohalarda mustahkam natija qayd etildi: {', '.join(improved_domains)}."
        else:
            q1_text = f"Umumiy {total_questions} ta savol ishlandi, asosiy ko'nikmalar shakllanmoqda."

        # 2. Nima hali qiyin?
        if difficult_domains:
            q2_text = f"Quyidagi mavzularda e'tiborni oshirish kerak: {', '.join(difficult_domains)}."
        elif unresolved_mistakes:
            q2_text = f"Xatolar daftarida {len(unresolved_mistakes)} ta o'zlashtirilmagan savol mavjud."
        else:
            q2_text = "Jiddiy tizimli xatolar aniqlanmadi. Yuqori qiyinlikdagi savollarga o'tish mumkin."

        # 3. Keyingi hafta nimani qilamiz?
        top_weak = difficult_domains[0] if difficult_domains else "eng ko'p xato qilingan mavzu"
        q3_tasks = [
            f"1. {top_weak} bo'yicha 15 ta maqsadli mashq ishlash.",
            "2. Xatolar daftarchasidagi savollarni 'Xatomni tuzat' orqali yechish.",
            "3. Haftalik 1 ta to'liq mock imtihonini topshirib, vaqt taqsimotini tekshirish."
        ]

        overall_correct = sum(1 for att in history if att.get("is_correct"))
        accuracy_pct = int((overall_correct / total_questions) * 100)

        return {
            "status": "ready",
            "total_questions": total_questions,
            "overall_accuracy_pct": accuracy_pct,
            "is_confident": True,
            "q1_what_improved": q1_text,
            "q2_what_is_difficult": q2_text,
            "q3_next_week_plan": q3_tasks
        }


weekly_report_service = WeeklyReportService()
