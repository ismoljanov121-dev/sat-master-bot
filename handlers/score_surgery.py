"""
SAT AI Bot - Diagnostic Performance Analysis (Score Surgery)
Provides honest diagnostic breakdown, conceptual weakness analysis,
and actionable preparation recommendations without fake scores or ungrounded promises.
"""

import html
from typing import Any


def generate_surgery_report(
    user_name: str,
    total_q: int,
    correct_q: int,
    incorrect_items: list[dict[str, Any]]
) -> str:
    """
    Generates an honest, insightful educational diagnosis report.
    Presents exact accuracy %, conceptual domain gaps, and tailored study steps.
    """
    safe_name = html.escape(user_name or "Abituriyent")
    accuracy_percent = round((correct_q / total_q) * 100) if total_q > 0 else 0

    # Skill level assessment
    if accuracy_percent == 100:
        level_badge = "🏆 <b>A'lo daraja (Advanced)</b>"
        level_desc = "Barcha savollar to'g'ri yechildi. Asosiy e'tiborni vaqt nazorati va qiyin modullarga qarating."
    elif accuracy_percent >= 70:
        level_badge = "📈 <b>Yaxshi daraja (Proficient)</b>"
        level_desc = "Konseptual poydevor mustahkam, ammo ayrim nozik nuqtalarda ehtiyotsizlik yoki usul xatosi bor."
    elif accuracy_percent >= 40:
        level_badge = "⚠️ <b>O'rta daraja (Developing)</b>"
        level_desc = "Asosiy mavzularda bo'shliqlar mavjud. Tejamkor Desmos usullari va formulalarni chuqurroq mustahkamlash zarur."
    else:
        level_badge = "🚩 <b>Boshlang'ich daraja (Foundational)</b>"
        level_desc = "Mavzularni noldan tizimli o'rganish va asosiy qoidalarni mustahkamlab olish tavsiya etiladi."

    # Group weaknesses by topic
    topic_counts: dict[str, int] = {}
    for item in incorrect_items:
        t = item.get("topic") or item.get("domain") or "General Math"
        topic_counts[t] = topic_counts.get(t, 0) + 1

    report = [
        "🔬 <b>DIAGNOSTIKA TAHLILI VA BILIM RENTGENI</b>",
        "━━━━━━━━━━━━━━━━━━━━━━",
        f"👤 <b>O'quvchi:</b> {safe_name}",
        f"🎯 <b>Natija:</b> {correct_q} / {total_q} ta to'g'ri (<b>{accuracy_percent}%</b>)",
        f"📊 <b>Baholash:</b> {level_badge}",
        f"<i>{level_desc}</i>\n",
        "📌 <b>ANIQLANGAN ZAIF MAVZULAR:</b>"
    ]

    if not incorrect_items:
        report.append("✨ <i>Birorta ham xato aniqlanmadi! Diagnostika savollarini a'lo bajardingiz.</i>")
        report.append("\n⚡ <b>Tavsiya:</b> Endi 'Bugungi 10 daqiqalik mashq' yoki 'Pilot Mock' orqali Reading & Writing ko'nikmalarini ham sinab ko'ring.")
    else:
        for topic, count in sorted(topic_counts.items(), key=lambda x: x[1], reverse=True):
            safe_topic = html.escape(str(topic))
            report.append(f"• <b>{safe_topic}:</b> {count} ta noaniq javob")

        report.append("\n🎯 <b>FOYDALI TAVSIYALAR:</b>")
        report.append("1. Har bir xato qilgan savol ostidagi <b>[⚡ Desmos usuli]</b> va yechim tahlilini diqqat bilan o'rganing.")
        report.append("2. Ushbu savollar avtomatik ravishda <b>❌ Xatolar daftari</b>ga kiritildi. Ertaga ularni qayta yechib ko'ring.")
        report.append("3. Nazariy formulalar bilan birga grafik yordamida tezkor tekshirish odatini shakllantiring.")

    report.append("\n━━━━━━━━━━━━━━━━━━━━━━")
    report.append("ℹ️ <i>Eslatma: Bu natija rasmiy SAT balli emas; mustaqil 7 savollik diagnostika orqali tayyorgarlik darajangizni xolisona ko'rsatuvchi ko'rsatkichdir.</i>")

    return "\n".join(report)
