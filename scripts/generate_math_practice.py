"""
Builds data/sat_math_practice.json: practice-only Algebra and Advanced Math questions made from templates.

Mocks use most of the bank, so without these a few practice sets would run into mock questions. Every template
picks its numbers, then proves the question the independent way: the answer goes back into the original equation,
and every wrong option goes through the same check. A question that fails the check stops the build.

Usage: python scripts/generate_math_practice.py
"""
import json
import random
from fractions import Fraction
from itertools import cycle
from math import gcd, isqrt
from pathlib import Path

OUT_FILE = Path(__file__).resolve().parent.parent / "data" / "sat_math_practice.json"
LETTERS = "ABCD"

ALG, ADV = "Algebra", "Advanced Math"
LIN1 = "Linear equations in one variable"
LIN2 = "Linear equations in two variables"
FUNC = "Linear functions"
INEQ = "Linear inequalities in one or two variables"
SYSTEM = "Systems of two linear equations in two variables"
EQUIV = "Equivalent expressions"
NONLIN = "Nonlinear equations and systems"
NFUNC = "Nonlinear functions"


class Draw:
    """Built on random() alone, the one method Python promises to keep, so every version makes the same file."""

    def __init__(self, seed: int):
        self._next = random.Random(seed).random

    def randint(self, low: int, high: int) -> int:
        return low + int(self._next() * (high - low + 1))

    def choice(self, items):
        return items[self.randint(0, len(items) - 1)]

    def sample(self, items, count: int) -> list:
        pool = list(items)
        return [pool.pop(self.randint(0, len(pool) - 1)) for _ in range(count)]


def n(value) -> str:
    """A number as it appears inside a formula."""
    value = Fraction(value)
    if value.denominator == 1:
        return str(value.numerator)
    sign = "-" if value < 0 else ""
    return f"{sign}\\frac{{{abs(value.numerator)}}}{{{value.denominator}}}"


def t(formula: str) -> str:
    return f"\\({formula}\\)"


def signed(value) -> str:
    return f"+{n(value)}" if value >= 0 else n(value)


def mono(coefficient, var: str = "x") -> str:
    if coefficient == 1:
        return var
    if coefficient == -1:
        return f"-{var}"
    return f"{n(coefficient)}{var}"


def linear(a, b, var: str = "x") -> str:
    head = mono(a, var) if a else ""
    if not b:
        return head or "0"
    return f"{head}{signed(b)}" if head else n(b)


def quadratic(a, b, c) -> str:
    text = mono(a, "x^{2}")
    if b:
        text += ("+" if b > 0 else "") + mono(b)
    return text + (signed(c) if c else "")


def option(value) -> str:
    """Plain digits for whole positive numbers, a formula for everything else."""
    value = Fraction(value)
    return str(value) if value.denominator == 1 and value >= 0 else t(n(value))


def numeric(values, holds) -> list[tuple[str, bool]]:
    return [(option(value), bool(holds(Fraction(value)))) for value in values]


def spr_answers(value) -> list[str]:
    value = Fraction(value)
    if value.denominator == 1:
        return [str(value.numerator)]
    answers = [f"{value.numerator}/{value.denominator}"]
    decimal = float(value)
    if Fraction(str(round(decimal, 4))) == value:
        answers.append(str(round(decimal, 4)))
    return answers


def mcq(skill, dif, stem, choices, exp, strat, dom=ALG, fig=None):
    """Takes (text, passes the check) pairs. Exactly one distinct text may pass, and three others must fail."""
    right = list(dict.fromkeys(text for text, passes in choices if passes))
    wrong = list(dict.fromkeys(text for text, passes in choices if not passes and text not in right))
    if len(right) != 1 or len(wrong) < 3:
        return None
    draft = {"dom": dom, "skill": skill, "dif": dif, "type": "mcq", "q": stem, "right": right[0], "wrong": wrong[:3],
             "exp": exp, "strat": strat}
    return {**draft, "fig": fig} if fig else draft


def spr(skill, dif, stem, value, holds, exp, strat, dom=ALG):
    if not holds(Fraction(value)):
        raise SystemExit(f"The answer {value} fails its own check: {stem}")
    return {"dom": dom, "skill": skill, "dif": dif, "type": "spr", "q": stem, "ans": spr_answers(value),
            "exp": exp, "strat": strat}


# Linear equations in one variable

def two_step_equation(rng):
    a, x, b = rng.randint(2, 9), rng.randint(2, 12), rng.randint(2, 20)
    c = a * x + b
    equation, step, check = f"{a}x+{b}={c}", f"{a}x={c - b}", f"{a}\\cdot {x}+{b}={c}"
    return mcq(
        LIN1, "Easy", f"What is the value of {t('x')} if {t(equation)}?",
        numeric([x, Fraction(c + b, a), c - b, Fraction(c, a) - b, x + a], lambda v: a * v + b == c),
        f"Ikkala tomondan {b} ni ayiramiz: {t(step)}. Keyin {a} ga bo'lamiz: {t(f'x={x}')}.",
        f"Javobni tenglamaga qo'yib tekshiring: {t(check)}.",
    )


def distribute_equation(rng):
    a, c = rng.randint(2, 7), rng.randint(1, 6)
    x, b = rng.randint(-6, 9), rng.randint(1, 8)
    if a == c:
        return None
    d = a * (x + b) - c * x
    left, right = f"{a}(x{signed(b)})", linear(c, d)
    opened, moved = f"{a}x{signed(a * b)}={right}", f"{mono(a - c)}={n(d - a * b)}"
    equation = f"{left}={right}"
    return spr(
        LIN1, "Medium", f"What value of {t('x')} is the solution to the equation {t(equation)}?", x,
        lambda v: a * (v + b) == c * v + d,
        f"Qavsni ochamiz: {t(opened)}. {t('x')} li hadlarni bir tomonga, sonlarni ikkinchi tomonga o'tkazamiz: {t(moved)}. "
        f"Demak, {t(f'x={x}')}.",
        "Qavs oldidagi son qavs ichidagi har bir hadga ko'paytiriladi. Ikkinchi hadni unutish eng ko'p uchraydigan xato.",
    )


def scaled_expression(rng):
    m, p, q, value = rng.randint(2, 6), rng.randint(2, 5), rng.randint(1, 9), rng.randint(3, 15)
    total = m * value
    x = Fraction(value - q, p)
    given, asked, factored = f"{m * p}x+{m * q}={total}", f"{p}x+{q}", f"{m}({p}x+{q})={total}"
    return spr(
        LIN1, "Medium", f"If {t(given)}, what is the value of {t(asked)}?", value,
        lambda v: p * x + q == v and m * p * x + m * q == total,
        f"Chap tomonni ko'paytuvchiga ajratamiz: {t(factored)}. Ikkala tomonni {m} ga bo'lsak, {t(f'{asked}={value}')}.",
        f"SAT tuzog'i: savol {t('x')} ni emas, butun ifodani so'ragan. {t('x')} ni topish shart emas.",
    )


def fraction_equation(rng):
    a, c = rng.sample([2, 3, 4, 5, 6], 2)
    lcm = a * c // gcd(a, c)
    x = lcm * rng.randint(1, 6) * rng.choice([1, -1])
    b = rng.randint(1, 9)
    d = Fraction(x, a) + b - Fraction(x, c)
    if d == 0:
        return None
    equation = f"\\frac{{x}}{{{a}}}+{b}=\\frac{{x}}{{{c}}}{signed(d)}"
    cleared = f"{mono(lcm // a)}+{lcm * b}={mono(lcm // c)}{signed(lcm * d)}"
    moved = f"{mono(lcm // a - lcm // c)}={n(lcm * d - lcm * b)}"
    return spr(
        LIN1, "Hard", f"What value of {t('x')} satisfies the equation {t(equation)}?", x,
        lambda v: v / a + b == v / c + d,
        f"Maxrajlardan qutulish uchun ikkala tomonni {lcm} ga ko'paytiramiz: {t(cleared)}. Hadlarni jamlaymiz: {t(moved)}, "
        f"demak {t(f'x={x}')}.",
        "Kasrli tenglamada avval maxrajlarning eng kichik umumiy karralisiga ko'paytiring, shunda oddiy chiziqli tenglama qoladi.",
    )


FEE_STORIES = [
    ("A gym charges a one-time fee of ${fee} and ${rate} per month. A member has paid ${total} in all.",
     "How many months of membership has the member paid for?"),
    ("A taxi ride costs ${fee} plus ${rate} per kilometer. One ride cost ${total}.",
     "How many kilometers long was the ride?"),
    ("A print shop charges ${fee} to set up a job and ${rate} for each poster. An order cost ${total}.",
     "How many posters were in the order?"),
    ("A bike rental costs ${fee} plus ${rate} per hour. A customer paid ${total}.",
     "For how many hours was the bike rented?"),
    ("A courier charges ${fee} per order plus ${rate} per kilogram. One order cost ${total}.",
     "How many kilograms did the order weigh?"),
]


def fee_plus_rate(rng):
    story, question = rng.choice(FEE_STORIES)
    fee, rate, count = rng.randint(3, 30), rng.randint(2, 12), rng.randint(3, 15)
    total = fee + rate * count
    equation, step = f"{fee}+{rate}n={total}", f"{rate}n={total - fee}"
    return spr(
        LIN1, "Easy", f"{story.format(fee=fee, rate=rate, total=total)} {question}", count,
        lambda v: fee + rate * v == total,
        f"Noma'lumni {t('n')} deb olamiz: {t(equation)}. Bundan {t(step)}, demak {t(f'n={count}')}.",
        f"Bir martalik to'lov bir marta qo'shiladi, takrorlanadigan to'lov esa {t('n')} ga ko'paytiriladi.",
    )


# Linear equations in two variables

PRICE_STORIES = [
    ("notebooks", "pens", "daftar", "ruchka"), ("adult tickets", "child tickets", "katta chipta", "bolalar chiptasi"),
    ("small boxes", "large boxes", "kichik quti", "katta quti"), ("apples", "pears", "olma", "nok"),
    ("blue folders", "red folders", "ko'k papka", "qizil papka"),
]


def which_equation(rng):
    first, second, first_uz, second_uz = rng.choice(PRICE_STORIES)
    a, c = rng.sample(range(2, 13), 2)
    x0, y0 = rng.randint(2, 9), rng.randint(a + 1, a + 9)
    total = a * x0 + c * y0
    samples = [(x0, y0), (x0 + c, y0 - a)]

    def choice(p, q, sign=1):
        joint = "+" if sign > 0 else "-"
        return t(f"{p}x{joint}{q}y={total}"), all(p * x + sign * q * y == total for x, y in samples)

    answer = f"{a}x+{c}y={total}"
    return mcq(
        LIN2, "Medium",
        f"At a store, {first} cost ${a} each and {second} cost ${c} each. A customer spent exactly ${total} on "
        f"{t('x')} {first} and {t('y')} {second}. Which equation represents this situation?",
        [choice(a, c), choice(c, a), choice(a, c, -1),
         (t(f"{a + c}(x+y)={total}"), all((a + c) * (x + y) == total for x, y in samples))],
        f"{t('x')} ta {first_uz} {t(f'{a}x')} dollar, {t('y')} ta {second_uz} {t(f'{c}y')} dollar turadi. "
        f"Ularning yig'indisi {total} dollar: {t(answer)}.",
        "Har bir narxni o'z miqdoriga ko'paytiring. Harflar va narxlar joyini almashtirib yubormang.",
    )


def slope_of_standard_form(rng):
    a, b = rng.randint(2, 9), rng.randint(2, 9)
    if gcd(a, b) != 1:
        return None
    c = rng.randint(3, 30)
    first, second = (Fraction(0), Fraction(c, b)), (Fraction(b), Fraction(c - a * b, b))
    slope = (second[1] - first[1]) / (second[0] - first[0])
    equation, solved = f"{a}x+{b}y={c}", f"y={n(Fraction(-a, b))}x{signed(Fraction(c, b))}"
    return mcq(
        LIN2, "Medium", f"What is the slope of the line with equation {t(equation)}?",
        numeric([Fraction(-a, b), Fraction(a, b), Fraction(-b, a), Fraction(b, a), Fraction(c, b)], lambda v: v == slope),
        f"Tenglamani {t('y')} ga nisbatan yechamiz: {t(solved)}. Qiyalik {t('x')} oldidagi son, ya'ni {t(n(Fraction(-a, b)))}.",
        f"Tez usul: {t('ax+by=c')} chizig'ining qiyaligi {t('-a/b')}. Minus belgisini unutmang.",
    )


def coefficient_from_point(rng):
    a, p = rng.randint(2, 7), rng.randint(-5, 6)
    q = rng.choice([-4, -3, -2, 2, 3, 4, 5])
    k = rng.choice([-5, -4, -3, -2, 2, 3, 4, 5, 6, 7])
    c = a * p + k * q
    equation, substituted = f"{a}x+ky={c}", f"{a}({p})+k({q})={c}"
    moved = f"{n(q)}k={n(c - a * p)}"
    return spr(
        LIN2, "Hard",
        f"In the {t('xy')}-plane, the graph of {t(equation)} passes through the point {t(f'({p},{q})')}, where {t('k')} is a "
        f"constant. What is the value of {t('k')}?",
        k, lambda v: a * p + v * q == c,
        f"Nuqta chiziqda yotsa, uning koordinatalari tenglamani qanoatlantiradi: {t(substituted)}. Bundan {t(moved)}, "
        f"demak {t(f'k={k}')}.",
        "Grafikdagi nuqta haqida gap ketsa, koordinatalarni tenglamaga qo'yish birinchi qadam bo'ladi.",
    )


# Linear functions

def function_value(rng):
    m, b, k = rng.randint(2, 9), rng.randint(-9, 12), rng.randint(-4, 9)
    if b == 0 or k == 0:
        return None
    definition = f"f(x)={linear(m, b)}"
    work = f"f({k})={m}({k}){signed(b)}={m * k + b}"
    return spr(
        FUNC, "Easy", f"The function {t('f')} is defined by {t(definition)}. What is the value of {t(f'f({k})')}?",
        m * k + b, lambda v: v == m * k + b,
        f"{t('x')} o'rniga {k} ni qo'yamiz: {t(work)}.",
        "Funksiya qiymati so'ralganda, qavs ichidagi sonni har bir x o'rniga qo'ying.",
    )


def function_input(rng):
    m, b, x = rng.choice([-5, -4, -3, -2, 2, 3, 4, 5, 6]), rng.randint(-9, 12), rng.randint(-6, 9)
    if b == 0:
        return None
    value = m * x + b
    definition, equation, step = f"f(x)={linear(m, b)}", f"{linear(m, b)}={value}", f"{mono(m)}={n(value - b)}"
    return spr(
        FUNC, "Medium", f"The function {t('f')} is defined by {t(definition)}. For what value of {t('x')} is {t(f'f(x)={value}')}?",
        x, lambda v: m * v + b == value,
        f"Tenglama tuzamiz: {t(equation)}. Bundan {t(step)}, demak {t(f'x={x}')}.",
        f"{t('f(x)')} berilganda, u {t('x')} ning o'zi emas. Qiymatni funksiyaga tenglab, {t('x')} ni toping.",
    )


def function_from_table(rng):
    m, b = rng.choice([-4, -3, -2, 2, 3, 4, 5]), rng.randint(-6, 9)
    xs = sorted(rng.sample(range(-2, 8), 3))
    if b == 0:
        return None
    rows = [[str(x), str(m * x + b)] for x in xs]

    def choice(slope, intercept):
        return t(f"f(x)={linear(slope, intercept)}"), all(slope * x + intercept == m * x + b for x in xs)

    rise, run = (m * xs[1] + b) - (m * xs[0] + b), xs[1] - xs[0]
    slope_work = f"\\frac{{{rise}}}{{{run}}}={m}"
    answer = f"f(x)={linear(m, b)}"
    return mcq(
        FUNC, "Medium", f"The table shows some values of the linear function {t('f')}. Which equation defines {t('f')}?",
        [choice(m, b), choice(-m, b), choice(m, -b), choice(m, b + m), choice(b or 1, m)],
        f"Ikki nuqtadan qiyalikni topamiz: {t(slope_work)}. Keyin bitta nuqtani qo'yib, ozod hadni aniqlaymiz: {t(answer)}.",
        "Variantlarni tekshirishning eng tez yo'li: jadvaldagi ikki qatorni variantga qo'yib ko'ring.",
        fig={"t": "table", "head": ["x", "f(x)"], "rows": rows},
    )


def intercept_from_points(rng):
    m, b = rng.choice([-4, -3, -2, 2, 3, 4, 5]), rng.randint(-9, 12)
    x1, x2 = rng.sample(range(-4, 9), 2)
    if b == 0:
        return None
    y1, y2 = m * x1 + b, m * x2 + b
    slope_work = f"m=\\frac{{{y2}-({y1})}}{{{x2}-({x1})}}={m}"
    substituted = f"{y1}={m}({x1})+b"
    return spr(
        FUNC, "Hard",
        f"A line in the {t('xy')}-plane passes through the points {t(f'({x1},{y1})')} and {t(f'({x2},{y2})')}. "
        f"What is the {t('y')}-coordinate of the {t('y')}-intercept of the line?",
        b, lambda v: m * x1 + v == y1 and m * x2 + v == y2,
        f"Avval qiyalikni topamiz: {t(slope_work)}. Keyin bitta nuqtani {t('y=mx+b')} ga qo'yamiz: {t(substituted)}, "
        f"demak {t(f'b={b}')}.",
        f"{t('y')}-kesishish chiziqning {t('x=0')} dagi qiymati. Qiyalik topilgach, bitta nuqta yetarli.",
    )


def draining_tank(rng):
    volume, rate = rng.randint(6, 40) * 10, rng.randint(2, 9)
    samples = [(0, volume), (1, volume - rate), (5, volume - 5 * rate)]

    def choice(start, change):
        return t(f"V(t)={linear(change, start, 't')}"), all(start + change * m == v for m, v in samples)

    answer = f"V(t)={volume}-{rate}t"
    return mcq(
        FUNC, "Medium",
        f"A tank holds {volume} liters of water. Water drains from the tank at a constant rate of {rate} liters per minute. "
        f"Which function gives the volume {t('V(t)')}, in liters, after {t('t')} minutes?",
        [choice(volume, -rate), choice(volume, rate), choice(rate, -volume), choice(rate, volume)],
        f"Boshlang'ich hajm {volume} litr. Har daqiqada {rate} litr kamayadi, shuning uchun {t(answer)}.",
        f"Boshlang'ich qiymat ozod had bo'ladi. Kamayish bo'lsa, {t('t')} oldida minus turadi.",
    )


# Linear inequalities

def flip_inequality(rng):
    a, b, k = rng.randint(2, 7), rng.randint(5, 30), rng.randint(-5, 9)
    c = b - a * k
    inequality, step, answer = f"{b}-{a}x\\ge {c}", f"-{a}x\\ge {c - b}", f"x\\le {k}"
    grid = [Fraction(k) + Fraction(step_, 2) for step_ in range(-6, 7)]
    truth = {v: b - a * v >= c for v in grid}
    relations = {"\\le": lambda v, w: v <= w, "\\ge": lambda v, w: v >= w, "<": lambda v, w: v < w, ">": lambda v, w: v > w}

    def choice(sign, bound):
        return t(f"x{sign} {n(bound)}"), all(relations[sign](v, bound) == truth[v] for v in grid)

    return mcq(
        INEQ, "Medium", f"Which of the following is the solution to the inequality {t(inequality)}?",
        [choice("\\le", k), choice("\\ge", k), choice(">", k), choice("\\ge", -k), choice("\\le", -k)],
        f"Ikkala tomondan {b} ni ayiramiz: {t(step)}. Manfiy {t(f'-{a}')} ga bo'lganda tengsizlik belgisi teskari aylanadi: "
        f"{t(answer)}.",
        "Tengsizlikni manfiy songa ko'paytirsangiz yoki bo'lsangiz, belgi albatta teskari bo'ladi.",
    )


CAPACITY_STORIES = [
    ("An elevator can carry at most {limit} kilograms. A worker who weighs {base} kilograms rides with boxes that weigh "
     "{each} kilograms each.", "What is the greatest number of boxes the worker can take in one trip?"),
    ("A van can carry at most {limit} kilograms. The driver and tools weigh {base} kilograms, and each bag of cement "
     "weighs {each} kilograms.", "What is the greatest number of bags the van can carry?"),
    ("A student has {limit} dollars. After paying a {base}-dollar entry fee, the student buys tickets that cost {each} "
     "dollars each.", "What is the greatest number of tickets the student can buy?"),
]


def capacity_limit(rng):
    story, question = rng.choice(CAPACITY_STORIES)
    base, each = rng.randint(40, 120), rng.randint(7, 25)
    count = rng.randint(4, 18)
    limit = base + each * count + rng.randint(1, each - 1)
    inequality, step = f"{base}+{each}n\\le {limit}", f"n\\le {n(Fraction(limit - base, each))}"
    return spr(
        INEQ, "Medium", f"{story.format(limit=limit, base=base, each=each)} {question}", count,
        lambda v: v.denominator == 1 and base + each * v <= limit < base + each * (v + 1),
        f"Tengsizlik tuzamiz: {t(inequality)}. Bundan {t(step)}. {t('n')} butun son bo'lishi kerak, shuning uchun eng kattasi "
        f"{count}.",
        "Bo'lish natijasi kasr chiqsa, narsalar soni uchun pastga yaxlitlanadi, chunki chegaradan oshib bo'lmaydi.",
    )


def at_least_model(rng):
    have, each, need = rng.randint(10, 40), rng.randint(3, 9), rng.randint(60, 120)
    sample = range(0, 40)
    needed = {x: have + each * x >= need for x in sample}

    def choice(text, test):
        return t(text), all(test(x) == needed[x] for x in sample)

    answer = f"{have}+{each}x\\ge {need}"
    return mcq(
        INEQ, "Medium",
        f"A student has {have} points and earns {each} more points for each task completed. The student needs at least "
        f"{need} points to pass. Which inequality shows the number of tasks, {t('x')}, the student must complete?",
        [choice(answer, lambda x: have + each * x >= need),
         choice(f"{have}+{each}x\\le {need}", lambda x: have + each * x <= need),
         choice(f"{have}x+{each}\\ge {need}", lambda x: have * x + each >= need),
         choice(f"{each}x\\ge {need}+{have}", lambda x: each * x >= need + have)],
        f"Boshlang'ich ball {have}, {t('x')} ta vazifadan keyin {t(f'{have}+{each}x')} ball bo'ladi. \"At least\" iborasi "
        f"\"kamida\" degani, shuning uchun {t(answer)}.",
        "\"At least\" belgisi \\(\\ge\\), \"at most\" belgisi \\(\\le\\). Bu ikkisini adashtirmang.",
    )


# Systems of linear equations

def sum_and_difference(rng):
    x, y = rng.randint(4, 30), rng.randint(1, 20)
    first, second = f"x+y={x + y}", f"x-y={x - y}"
    added = f"2x={2 * x}"
    return spr(
        SYSTEM, "Easy",
        f"The system of equations below has solution {t('(x,y)')}.\n{t(first)}\n{t(second)}\nWhat is the value of {t('x')}?",
        x, lambda v: v + y == x + y and v - y == x - y,
        f"Tenglamalarni qo'shamiz, {t('y')} qisqaradi: {t(added)}. Demak {t(f'x={x}')}.",
        "Bir xil koeffitsiyent qarama-qarshi ishorada tursa, tenglamalarni qo'shish eng tez yo'l.",
    )


def elimination(rng):
    x, y = rng.randint(-5, 8), rng.randint(-5, 8)
    a, b, d, e = rng.randint(1, 6), rng.randint(1, 6), rng.randint(1, 6), rng.randint(-6, -1)
    if a * e - b * d == 0 or x == 0 or y == 0:
        return None
    c, f = a * x + b * y, d * x + e * y
    first, second = f"{mono(a)}+{mono(b, 'y')}={c}", f"{mono(d)}{mono(e, 'y')}={f}"
    asked, value = rng.choice([("x", x), ("y", y)])
    other = y if asked == "x" else x
    scaled_first, scaled_second = f"{mono(a * -e)}+{mono(b * -e, 'y')}={c * -e}", f"{mono(d * b)}{mono(e * b, 'y')}={f * b}"
    added = f"{mono(a * -e + d * b)}={n(c * -e + f * b)}"
    return spr(
        SYSTEM, "Medium",
        f"The solution to the system of equations below is {t('(x,y)')}.\n{t(first)}\n{t(second)}\nWhat is the value of {t(asked)}?",
        value,
        lambda v: (a * v + b * other == c and d * v + e * other == f) if asked == "x" else (a * other + b * v == c and d * other + e * v == f),
        f"{t('y')} ni yo'qotish uchun tenglamalarni mos sonlarga ko'paytiramiz: {t(scaled_first)} va {t(scaled_second)}. Qo'shsak: "
        f"{t(added)}, demak {t(f'x={x}')}. Birinchi tenglamaga qo'yib, {t(f'y={y}')} ni topamiz.",
        "Desmos usuli: ikkala tenglamani kiriting, chiziqlar kesishgan nuqta sistemaning yechimi.",
    )


def ticket_system(rng):
    high, low = rng.sample(range(4, 16), 2)
    if high < low:
        high, low = low, high
    adults, kids = rng.randint(8, 40), rng.randint(8, 40)
    count, money = adults + kids, high * adults + low * kids
    first, second = f"a+s={count}", f"{high}a+{low}s={money}"
    substituted = f"{high}a+{low}({count}-a)={money}"
    step = f"{high - low}a={money - low * count}"
    return spr(
        SYSTEM, "Medium",
        f"A theater sold {count} tickets for a total of ${money}. Adult tickets cost ${high} each and student tickets cost "
        f"${low} each. How many adult tickets were sold?",
        adults, lambda v: high * v + low * (count - v) == money,
        f"Katta chiptalar {t('a')}, talaba chiptalari {t('s')} bo'lsin: {t(first)} va {t(second)}. {t(f's={count}-a')} ni qo'yamiz: "
        f"{t(substituted)}. Bundan {t(step)}, demak {t(f'a={adults}')}.",
        "Soni va puli berilgan masalada ikki tenglama tuziladi: biri chiptalar soni, ikkinchisi umumiy pul uchun.",
    )


def no_solution(rng):
    a, b, m = rng.randint(2, 6), rng.randint(2, 7), rng.randint(2, 4)
    c = rng.randint(3, 20)
    d, e = m * b, m * c + rng.choice([-6, -4, -2, 2, 4, 6])
    k = m * a
    first, second = f"{a}x+{b}y={c}", f"kx+{d}y={e}"
    scaled = f"{k}x+{d}y={m * c}"
    return mcq(
        SYSTEM, "Hard",
        f"In the system of equations below, {t('k')} is a constant. For what value of {t('k')} does the system have no solution?\n"
        f"{t(first)}\n{t(second)}",
        numeric([k, k + a, a, k - 1, d, m * c], lambda v: v * b == a * d and e * b != c * d),
        f"Birinchi tenglamani {m} ga ko'paytiramiz: {t(scaled)}. Chiziqlar parallel bo'lishi uchun {t('x')} oldidagi sonlar ham teng "
        f"bo'lishi kerak: {t(f'k={k}')}. O'ng tomonlar {m * c} va {e} har xil, shuning uchun yechim yo'q.",
        "Yechim yo'q degani chiziqlar parallel: koeffitsiyentlar nisbati teng, ozod hadlar nisbati esa boshqacha.",
    )


def infinite_solutions(rng):
    a, b, c, m = rng.randint(2, 7), rng.randint(2, 7), rng.randint(3, 15), rng.randint(2, 5)
    first, second = f"{a}x+{b}y={c}", f"{m * a}x+{m * b}y=k"
    return spr(
        SYSTEM, "Hard",
        f"The system of equations below has infinitely many solutions, where {t('k')} is a constant.\n{t(first)}\n{t(second)}\n"
        f"What is the value of {t('k')}?",
        m * c, lambda v: v * a == m * a * c and v * b == m * b * c,
        f"Ikkinchi tenglamaning koeffitsiyentlari birinchisidan {m} marta katta. Cheksiz ko'p yechim uchun ozod had ham {m} marta "
        f"katta bo'lishi kerak: {t(f'k={m}({c})={m * c}')}.",
        "Cheksiz ko'p yechim degani ikki tenglama aslida bitta chiziq. Bittasini songa ko'paytirsangiz, ikkinchisi chiqadi.",
    )


# Equivalent expressions

def expand_product(rng):
    a, b = rng.choice([-7, -5, -4, -3, -2, 2, 3, 4, 5, 6]), rng.choice([-6, -3, -2, 1, 2, 3, 4, 7])
    if a + b == 0 or a == b:
        return None
    sample = range(-3, 5)

    def choice(p, q):
        return t(quadratic(1, p, q)), all(x * x + p * x + q == (x + a) * (x + b) for x in sample)

    product, answer = f"(x{signed(a)})(x{signed(b)})", quadratic(1, a + b, a * b)
    work = f"x^{{2}}{signed(b)}x{signed(a)}x{signed(a * b)}"
    return mcq(
        EQUIV, "Easy", f"Which expression is equivalent to {t(product)}?",
        [choice(a + b, a * b), choice(a * b, a + b), choice(0, a * b), choice(a + b, -a * b), choice(a - b, a * b)],
        f"Har bir hadni har biriga ko'paytiramiz: {t(work)}. O'xshash hadlarni jamlasak: {t(answer)}.",
        f"Tekshirish: {t('x=1')} ni berilgan ifodaga va variantga qo'yib solishtiring.",
        dom=ADV,
    )


def factor_quadratic(rng):
    p, q = rng.sample([-8, -6, -5, -4, -3, -2, 2, 3, 4, 5, 6, 7], 2)
    if p + q == 0:
        return None
    sample = range(-3, 5)

    def choice(r, s):
        return t(f"(x{signed(r)})(x{signed(s)})"), all((x + r) * (x + s) == x * x + (p + q) * x + p * q for x in sample)

    expression = quadratic(1, p + q, p * q)
    return mcq(
        EQUIV, "Medium", f"Which of the following is equivalent to {t(expression)}?",
        [choice(p, q), choice(-p, -q), choice(p, -q), choice(-p, q), choice(p + q, 1)],
        f"Ko'paytmasi {p * q} va yig'indisi {p + q} bo'lgan ikki son kerak. Bu sonlar {p} va {q}, shuning uchun javob "
        f"{t(f'(x{signed(p)})(x{signed(q)})')}.",
        "Variantlarda ishoralar aralashgan bo'ladi. Ko'paytmaning ishorasiga qarab, juftlikni tez tanlang.",
        dom=ADV,
    )


def square_binomial(rng):
    a, b = rng.randint(2, 6), rng.choice([-7, -5, -3, -2, 2, 3, 4, 5, 6])
    sample = range(-3, 5)

    def choice(p, q, r):
        return t(quadratic(p, q, r)), all(p * x * x + q * x + r == (a * x + b) ** 2 for x in sample)

    binomial, answer = f"({a}x{signed(b)})^{{2}}", quadratic(a * a, 2 * a * b, b * b)
    work = f"({a}x)^{{2}}+2({a}x)({b})+({b})^{{2}}"
    return mcq(
        EQUIV, "Medium", f"Which expression is equivalent to {t(binomial)}?",
        [choice(a * a, 2 * a * b, b * b), choice(a * a, 0, b * b), choice(a * a, a * b, b * b), choice(a, 2 * a * b, b * b),
         choice(a * a, -2 * a * b, b * b)],
        f"Kvadrat formulasi: {t('(p+q)^{2}=p^{2}+2pq+q^{2}')}. Bu yerda {t(work)}, ya'ni {t(answer)}.",
        f"Eng ko'p xato o'rtadagi {t('2pq')} hadni tashlab ketish. Uni albatta yozing.",
        dom=ADV,
    )


def exponent_rules(rng):
    a, b, c = rng.randint(2, 9), rng.randint(2, 9), rng.randint(2, 6)
    power = a + b - c
    if power < 2:
        return None
    expression = f"\\frac{{x^{{{a}}}\\cdot x^{{{b}}}}}{{x^{{{c}}}}}"
    truth = Fraction(2) ** a * Fraction(2) ** b / Fraction(2) ** c

    def choice(exponent):
        return t(f"x^{{{exponent}}}"), Fraction(2) ** exponent == truth

    work = f"x^{{{a}+{b}-{c}}}=x^{{{power}}}"
    return mcq(
        EQUIV, "Medium", f"For {t('x>0')}, which expression is equivalent to {t(expression)}?",
        [choice(power), choice(a * b - c), choice(a + b + c), choice(a * b + c), choice(power + 1)],
        f"Asoslari bir xil darajalarni ko'paytirganda daraja ko'rsatkichlari qo'shiladi, bo'lganda ayiriladi: {t(work)}.",
        "Ko'paytirishda qo'shing, bo'lishda ayiring. Ko'rsatkichlarni ko'paytirish faqat darajaning darajasida bo'ladi.",
        dom=ADV,
    )


# Nonlinear equations

def positive_root(rng):
    r, s = rng.randint(1, 12), rng.randint(1, 12)
    if r == s:
        return None
    b, c = s - r, -r * s
    equation, factored = f"{quadratic(1, b, c)}=0", f"(x-{r})(x+{s})=0"
    return spr(
        NONLIN, "Medium", f"What is the positive solution to the equation {t(equation)}?",
        r, lambda v: v > 0 and v * v + b * v + c == 0,
        f"Ko'paytuvchilarga ajratamiz: {t(factored)}. Yechimlar {t(f'x={r}')} va {t(f'x=-{s}')}. Musbati {r}.",
        f"Desmos usuli: {t(f'y={quadratic(1, b, c)}')} ni kiriting va grafik {t('x')} o'qini kesgan musbat nuqtani o'qing.",
        dom=ADV,
    )


ONE_SOLUTION_PAIRS = [(1, 9), (1, 16), (1, 25), (1, 36), (2, 8), (2, 18), (3, 12), (3, 27), (4, 9), (4, 25), (9, 4), (5, 20)]


def one_solution(rng):
    a, c = rng.choice(ONE_SOLUTION_PAIRS)
    k = isqrt(4 * a * c)
    equation = f"{mono(a, 'x^{2}')}+kx+{c}=0"
    work = f"k^{{2}}-4({a})({c})=0"
    return spr(
        NONLIN, "Hard",
        f"In the equation {t(equation)}, {t('k')} is a positive constant. The equation has exactly one real solution. "
        f"What is the value of {t('k')}?",
        k, lambda v: v > 0 and v * v == 4 * a * c,
        f"Yagona yechim uchun diskriminant nol bo'ladi: {t(work)}, ya'ni {t(f'k^{{2}}={4 * a * c}')}. {t('k')} musbat, demak {t(f'k={k}')}.",
        "\"Exactly one solution\" iborasini ko'rsangiz, darhol diskriminantni nolga tenglang.",
        dom=ADV,
    )


def line_meets_parabola(rng):
    r, s = rng.randint(1, 9), rng.randint(1, 9)
    m, d = rng.randint(-4, 5), rng.randint(-6, 9)
    if r == s or m == 0 or d == 0:
        return None
    b, c = m + s - r, d - r * s
    if b == 0 or c == 0:
        return None
    parabola, line = f"y={quadratic(1, b, c)}", f"y={linear(m, d)}"
    equal, reduced = f"{quadratic(1, b, c)}={linear(m, d)}", f"{quadratic(1, s - r, -r * s)}=0"
    return spr(
        NONLIN, "Hard",
        f"The graphs of the equations below intersect at two points in the {t('xy')}-plane.\n{t(parabola)}\n{t(line)}\n"
        f"What is the positive {t('x')}-coordinate of an intersection point?",
        r, lambda v: v > 0 and v * v + b * v + c == m * v + d,
        f"Kesishish nuqtasida {t('y')} qiymatlari teng: {t(equal)}. Hammasini bir tomonga o'tkazamiz: {t(reduced)}. "
        f"Bu {t(f'(x-{r})(x+{s})=0')} bo'ladi, musbat yechim {r}.",
        "Desmos usuli: ikkala tenglamani kiriting va kesishish nuqtalarini bosing.",
        dom=ADV,
    )


# Nonlinear functions

def exponential_value(rng):
    start, base, power = rng.choice([50, 80, 100, 120, 200, 250, 300, 500]), rng.choice([2, 3]), rng.randint(2, 5)
    definition = f"A(t)={start}({base})^{{t}}"
    work = f"A({power})={start}({base})^{{{power}}}={start}\\cdot {base ** power}={start * base ** power}"
    return spr(
        NFUNC, "Medium",
        f"The function {t(definition)} gives the size of a population after {t('t')} years. What is the value of {t(f'A({power})')}?",
        start * base ** power, lambda v: v == start * base ** power,
        f"{t('t')} o'rniga {power} ni qo'yamiz: {t(work)}.",
        "Avval darajani hisoblang, keyin boshlang'ich qiymatga ko'paytiring.",
        dom=ADV,
    )


def doubling_model(rng):
    start, period = rng.choice([100, 150, 200, 300, 400, 500]), rng.randint(2, 8)
    samples = [(0, start), (period, 2 * start), (2 * period, 4 * start)]

    def choice(text, formula):
        return t(text), all(formula(moment) == value for moment, value in samples)

    answer = f"f(t)={start}(2)^{{t/{period}}}"
    return mcq(
        NFUNC, "Medium",
        f"A culture starts with {start} bacteria, and the number of bacteria doubles every {period} hours. Which function gives "
        f"the number of bacteria after {t('t')} hours?",
        [choice(answer, lambda m: start * Fraction(2) ** (m // period)),
         choice(f"f(t)={start}(2)^{{{period}t}}", lambda m: start * Fraction(2) ** (period * m)),
         choice(f"f(t)=2({start})^{{t/{period}}}", lambda m: 2 * Fraction(start) ** (m // period)),
         choice(f"f(t)={start}(\\frac{{1}}{{2}})^{{t/{period}}}", lambda m: start * Fraction(1, 2) ** (m // period))],
        f"Boshlang'ich qiymat {start}. {period} soatda bir marta 2 ga ko'payadi, shuning uchun daraja {t(f't/{period}')} bo'ladi: {t(answer)}.",
        f"Tekshirish: {t(f't={period}')} bo'lganda natija {2 * start} chiqishi kerak.",
        dom=ADV,
    )


def minimum_value(rng):
    half, c = rng.choice([-6, -5, -4, -3, -2, 2, 3, 4, 5, 6]), rng.randint(-5, 30)
    b = 2 * half
    if c == 0:
        return None
    lowest = c - half * half
    definition, square = f"f(x)={quadratic(1, b, c)}", f"f(x)=(x{signed(half)})^{{2}}{signed(lowest)}"

    def value(x):
        return x * x + b * x + c

    return spr(
        NFUNC, "Medium", f"The function {t('f')} is defined by {t(definition)}. What is the minimum value of {t('f(x)')}?",
        lowest, lambda v: v == value(-half) and all(value(x) >= v for x in range(-20, 21)),
        f"To'la kvadrat ajratamiz: {t(square)}. Kvadrat eng kamida 0 bo'ladi, shuning uchun eng kichik qiymat {lowest}.",
        "Desmos usuli: funksiyani kiriting va parabolaning eng pastki nuqtasini bosing. Javob uning y koordinatasi.",
        dom=ADV,
    )


def vertex_form_coefficient(rng):
    h, k, a = rng.randint(-4, 5), rng.randint(-6, 8), rng.choice([-3, -2, 2, 3, 4, 5])
    p = h + rng.choice([-3, -2, -1, 1, 2, 3])
    q = a * (p - h) ** 2 + k
    definition = f"f(x)=a(x{signed(-h)})^{{2}}{signed(k)}"
    work = f"{q}=a({p}{signed(-h)})^{{2}}{signed(k)}"
    step = f"{(p - h) ** 2}a={q - k}"
    return spr(
        NFUNC, "Hard",
        f"The function {t('f')} is defined by {t(definition)}, where {t('a')} is a constant. The graph of {t('f')} passes through "
        f"the point {t(f'({p},{q})')}. What is the value of {t('a')}?",
        a, lambda v: v * (p - h) ** 2 + k == q,
        f"Nuqtani funksiyaga qo'yamiz: {t(work)}. Bundan {t(step)}, demak {t(f'a={a}')}.",
        "Cho'qqi ko'rinishida faqat bitta noma'lum qolganda, grafikdagi bitta nuqta uni topishga yetadi.",
        dom=ADV,
    )


TEMPLATES = [
    (two_step_equation, 8), (distribute_equation, 8), (scaled_expression, 6), (fraction_equation, 6), (fee_plus_rate, 8),
    (which_equation, 8), (slope_of_standard_form, 6), (coefficient_from_point, 6),
    (function_value, 6), (function_input, 6), (function_from_table, 8), (intercept_from_points, 6), (draining_tank, 6),
    (flip_inequality, 8), (capacity_limit, 6), (at_least_model, 6),
    (sum_and_difference, 6), (elimination, 8), (ticket_system, 6), (no_solution, 6), (infinite_solutions, 6),
    (expand_product, 8), (factor_quadratic, 8), (square_binomial, 6), (exponent_rules, 6),
    (positive_root, 8), (one_solution, 8), (line_meets_parabola, 6),
    (exponential_value, 6), (doubling_model, 6), (minimum_value, 6), (vertex_form_coefficient, 6),
]


def finish(draft: dict, number: str, letters) -> dict:
    question = {"id": number, "sec": "m", "dom": draft["dom"], "skill": draft["skill"], "dif": draft["dif"],
                "type": draft["type"], "pas": "", "q": draft["q"], "mock": False}
    if draft["type"] == "mcq":
        position = next(letters)
        question["opts"] = [*draft["wrong"][:position], draft["right"], *draft["wrong"][position:]]
        question["cor"] = LETTERS[position]
    else:
        question["ans"] = draft["ans"]
    if "fig" in draft:
        question["fig"] = draft["fig"]
    question["exp"], question["strat"] = draft["exp"], draft["strat"]
    return question


def build() -> list[dict]:
    rng = Draw(1600)
    letters = cycle(range(4))
    questions, seen = [], set()
    for template, count in TEMPLATES:
        made = 0
        for _ in range(5000):
            draft = template(rng)
            key = draft and draft["q"] + str(draft.get("fig"))
            if draft is None or key in seen:
                continue
            seen.add(key)
            made += 1
            questions.append(finish(draft, f"g_{template.__name__}_{made:02d}", letters))
            if made == count:
                break
        else:
            raise SystemExit(f"{template.__name__} made only {made} of {count} questions")
    return questions


def main() -> None:
    questions = build()
    OUT_FILE.write_text(json.dumps(questions, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    print(f"{len(questions)} questions written to {OUT_FILE.name}")


if __name__ == "__main__":
    main()
