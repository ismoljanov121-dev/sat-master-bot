"""
SAT AI Bot - Score Surgery (AI Rentgen Diagnostika Tahlili)
Calculates exact score loss, diagnoses conceptual weaknesses,
and generates actionable high-impact surgical advice.
"""

import html


def generate_surgery_report(user_name: str, total_q: int, correct_q: int, incorrect_items: list[dict]) -> str:
    """Generates the jaw-dropping surgical score breakdown report."""
    base_math_score = 800
    points_lost = sum(item.get("points_lost", 20) for item in incorrect_items)
    estimated_score = max(base_math_score - points_lost, 400)

    safe_name = html.escape(user_name or "Abituriyent")

    # Group weaknesses by topic
    topic_counts: dict[str, int] = {}
    for item in incorrect_items:
        t = item.get("topic", "General Math")
        topic_counts[t] = topic_counts.get(t, 0) + 1

    report = [
        "🔬 <b>AI RENTGEN DIAGNOSTIKA: JARROHLIK XULOSASI</b>",
        "━━━━━━━━━━━━━━━━━━━━━━",
        f"👤 <b>Abituriyent:</b> {safe_name}",
        f"🎯 <b>To'g'ri javoblar:</b> {correct_q} / {total_q}",
        f"📉 <b>Yo'qotilgan ball:</b> -{points_lost} ball",
        f"📊 <b>Taxminiy Math Ballingiz:</b> <b>{estimated_score} / 800</b>\n",
        "🚨 <b>ASOSIY TASHXIS VA 'BALL O'G'RILARI':</b>"
    ]

    if not incorrect_items:
        report.append("🌟 <b>Dahshatli natija!</b> Birorta ham xato qilmadingiz. Sizning bazangiz 780-800 ballik darajada!")
        report.append("\n⚡ <i>Tavsiya: Endi vaqt bilan ishlash va Hard Module 2 tezligini oshirish ustida ishlang.</i>")
    else:
        for topic, count in topic_counts.items():
            safe_topic = html.escape(topic)
            report.append(f"• <b>{safe_topic}:</b> {count} ta xato (-{count * 20} ball)")

        report.append("\n💡 <b>ENG MUHIM SIR:</b>")
        report.append("Siz matematikani bilmaganingizdan emas, <b>Digital SAT Desmos hiylalarini ishlatmaganingiz</b> va standart tuzoqlarga tushganingiz uchun ball yo'qotyapsiz!")
        report.append(f"\n🚀 <b>1 KUNDA +{points_lost} BALL QO'SHISH REJASI:</b>")
        report.append("1. Quyidagi har bir xato savol ostidagi <b>[⚡ Desmos Hack]</b> tugmasini bosing.")
        report.append("2. Formulani yozishni emas, grafikni 5 soniyada o'qishni o'rganing.")
        report.append("3. 60 kunlik kundalik orqali aynan shu mavzularni yoping!")

    report.append("\n━━━━━━━━━━━━━━━━━━━━━━")
    report.append("👇 <i>Xatolaringizni Desmos orqali 5 soniyada yechish yo'lini ko'rish uchun quyidagi tugmani bosing:</i>")

    return "\n".join(report)
