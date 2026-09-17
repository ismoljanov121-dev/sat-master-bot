"""
EduTest Pro - Tiered Scaffolding Hint Service
Delivers progressive hints without immediately revealing the final answer:
- Level 1: Conceptual Pointer (Guiding principle or formula to consider).
- Level 2: Methodological / Tactical Hint (Desmos shortcut for Math, Elimination rule for Reading/Writing).
Operates entirely on pre-verified vault content (Zero expensive AI API dependencies).
"""

from typing import Any
import logging

from services.question_repository import vault

logger = logging.getLogger("HintScaffoldingService")


class HintScaffoldingService:
    def get_hints_for_question(self, question_id: str) -> dict[str, Any]:
        """
        Extracts progressive hints for a specific question.
        """
        q = vault.get_question(question_id)
        if not q:
            return {
                "ok": False,
                "error": "Question not found",
                "question_id": question_id
            }

        section = q.get("section", "math").lower()
        domain = q.get("domain", "General")
        skill = q.get("skill", domain)
        hack = q.get("strategy_or_hack", "")
        explanation = q.get("explanation", "")

        # Generate Level 1 Hint (Guiding question / rule)
        if section == "math":
            level_1 = (
                f"💡 1-Maslahat ({skill}): "
                f"Tenglama yoki shakldagi berilgan qiymatlarni aniqlang. "
                f"Izlanayotgan noma'lumni yolg'iz qoldirish yoki burchak/koordinatalar bog'lanishini eslang."
            )
            # Level 2 Hint: Desmos or tactical hack
            if hack:
                level_2 = f"⚡ 2-Maslahat (Desmos / Taktika): {hack}"
            else:
                level_2 = (
                    f"⚡ 2-Maslahat: Variantlarni to'g'ridan-to'g'ri tekshiring (Backsolving) "
                    f"yoki ifodani soddalashtirib ko'ring."
                )
        elif section == "writing":
            level_1 = (
                f"💡 1-Maslahat ({skill}): "
                f"Bo'sh joy atrofidagi mustaqil (independent) va ergash (dependent) gaplar chegarasini aniqlang."
            )
            if hack:
                level_2 = f"⚡ 2-Maslahat (Qoida): {hack}"
            else:
                level_2 = (
                    f"⚡ 2-Maslahat: Ega va kesim mosligini tekshiring, ortiqcha tinish belgilarini chiqarib tashlang."
                )
        else:  # reading
            level_1 = (
                f"💡 1-Maslahat ({skill}): "
                f"Matndagi kalit so'zlarga e'tibor bering. Muallifning asosiy fikri qaysi jumlada ifodalangan?"
            )
            if hack:
                level_2 = f"⚡ 2-Maslahat (Taktika): {hack}"
            else:
                level_2 = (
                    f"⚡ 2-Maslahat: Matnda to'g'ridan-to'g'ri aytilmagan yoki haddan tashqari mutlaq (extreme) "
                    f"so'zlar ('always', 'never') qatnashgan variantlarni istisno qiling."
                )

        return {
            "ok": True,
            "question_id": question_id,
            "section": section,
            "domain": domain,
            "skill": skill,
            "hint_level_1": level_1,
            "hint_level_2": level_2,
            "desmos_available": bool(section == "math" and "desmos" in hack.lower())
        }


hint_service = HintScaffoldingService()
