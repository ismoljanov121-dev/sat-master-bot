"""
Builds data/channel/sat_math.json: short SAT Math questions for the channel's quiz polls.

Every answer is computed here and every wrong option comes from a typical mistake, so no number in the
file is typed by hand. Each template has its own random stream, so adding a template leaves the others as
they were. Run it again after changing a template:

    python scripts/generate_channel_math.py
"""

import json
import random
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable, Optional

OUT = Path(__file__).resolve().parent.parent / "data" / "channel" / "sat_math.json"
PER_TEMPLATE = 15
SEED = 20261107


def fmt(value: Any) -> str:
    """Integers as they are, fractions as a/b, thousands with commas like the SAT prints them."""
    value = Fraction(value)
    if value.denominator != 1:
        return f"{value.numerator}/{value.denominator}"
    number = value.numerator
    return f"{number:,}" if abs(number) >= 10000 else str(number)


def par(value: int) -> str:
    return f"({value})" if value < 0 else str(value)


def signed(value: int) -> str:
    return f"+ {value}" if value >= 0 else f"- {-value}"


def poly(*coefficients: int) -> str:
    """poly(2, -3, 1) is '2x² - 3x + 1'. Zero terms are left out and a coefficient of 1 is not written."""
    names = {2: "x²", 1: "x", 0: ""}
    degree = len(coefficients) - 1
    text = ""
    for power, coefficient in zip(range(degree, -1, -1), coefficients):
        if coefficient == 0:
            continue
        size = abs(coefficient)
        body = ("" if size == 1 and names[power] else str(size)) + names[power]
        if not text:
            text = ("-" if coefficient < 0 else "") + body
        else:
            text += f" {'-' if coefficient < 0 else '+'} {body}"
    return text or "0"


# ---------------------------------------------------------------- Algebra

def linear_equation(rng: random.Random) -> dict:
    a, x, b = rng.randint(2, 9), rng.randint(2, 15), rng.randint(1, 30)
    c = a * x + b
    return {"t": "Algebra", "q": f"If {a}x + {b} = {c}, what is the value of x?", "answer": fmt(x),
            "wrong": [fmt(Fraction(c + b, a)), fmt(c - b), fmt(x + 1), fmt(x - 1)],
            "e": f"{a}x = {c} - {b} = {c - b}, demak x = {c - b}/{a} = {x}."}


def expression_value(rng: random.Random) -> dict:
    a, x, b = rng.randint(2, 6), rng.randint(2, 12), rng.randint(1, 20)
    m, n = rng.randint(2, 5), rng.randint(1, 15)
    c, value = a * x - b, m * x + n
    return {"t": "Algebra", "q": f"If {a}x - {b} = {c}, what is the value of {m}x + {n}?", "answer": fmt(value),
            "wrong": [fmt(x), fmt(m * x), fmt(value + m), fmt(value + b)],
            "e": f"{a}x = {par(c)} + {b} = {a * x}, demak x = {x}. Keyin {m}·{x} + {n} = {value}."}


def slope(rng: random.Random) -> dict:
    m = rng.choice([-4, -3, -2, 2, 3, 4, 5])
    x1, y1, d = rng.randint(-5, 5), rng.randint(-6, 6), rng.randint(2, 6)
    x2, y2 = x1 + d, y1 + m * d
    return {"t": "Algebra",
            "q": f"What is the slope of the line that passes through the points ({x1}, {y1}) and ({x2}, {y2})?",
            "answer": fmt(m), "wrong": [fmt(-m), fmt(Fraction(1, m)), fmt(m + 1), fmt(d)],
            "e": f"Qiyalik = (y₂ - y₁)/(x₂ - x₁) = ({y2} - {par(y1)})/({x2} - {par(x1)}) = {m * d}/{d} = {m}."}


def line_value(rng: random.Random) -> dict:
    m, b, k = rng.choice([-3, -2, 2, 3, 4, 5]), rng.randint(-9, 12), rng.randint(2, 9)
    y = m * k + b
    return {"t": "Algebra",
            "q": f"A line in the xy-plane has a slope of {m} and a y-intercept of {b}. What is the value of y when x = {k}?",
            "answer": fmt(y), "wrong": [fmt(m + b * k), fmt(m * k - b), fmt(m * (k + b)), fmt(y + m)],
            "e": f"Tenglama: y = {poly(m, b)}. x = {k} bo'lganda y = {m}·{k} {signed(b)} = {y}."}


def system_sum(rng: random.Random) -> dict:
    x, y = rng.randint(2, 15), rng.randint(1, 12)
    s, d = x + y, x - y
    return {"t": "Algebra", "q": f"If x + y = {s} and x - y = {d}, what is the value of x?", "answer": fmt(x),
            "wrong": [fmt(y), fmt(s + d), fmt(s - d), fmt(d)],
            "e": f"Tenglamalarni qo'shing: 2x = {s} + {par(d)} = {2 * x}, demak x = {x}."}


def system_elimination(rng: random.Random) -> dict:
    x, y = rng.randint(1, 9), rng.randint(1, 9)
    a, b = 2 * x + y, x - y
    return {"t": "Algebra", "q": f"If 2x + y = {a} and x - y = {b}, what is the value of x?", "answer": fmt(x),
            "wrong": [fmt(y), fmt(a + b), fmt(x + y), fmt(Fraction(a - b, 3))],
            "e": f"Tenglamalarni qo'shsak, y yo'qoladi: 3x = {a} + {par(b)} = {3 * x}, demak x = {x}."}


def absolute_sum(rng: random.Random) -> dict:
    a, b = rng.randint(-8, 9), rng.randint(2, 12)
    inside = poly(1, -a)
    return {"t": "Algebra", "q": f"What is the sum of all solutions to the equation |{inside}| = {b}?",
            "answer": fmt(2 * a), "wrong": [fmt(a + b), fmt(2 * b), fmt(a - b), fmt(a)],
            "e": f"{inside} = {b} yoki {inside} = -{b}, ya'ni x = {a + b} yoki x = {a - b}. Yig'indi: {2 * a}."}


def least_integer(rng: random.Random) -> dict:
    a, b, bound = rng.randint(2, 7), rng.randint(1, 20), rng.randint(2, 12)
    c = a * bound - b
    return {"t": "Algebra", "q": f"What is the least integer value of x that satisfies {a}x - {b} > {c}?",
            "answer": fmt(bound + 1), "wrong": [fmt(bound), fmt(bound - 1), fmt(bound + 2), fmt(c)],
            "e": f"{a}x > {par(c)} + {b} = {a * bound}, demak x > {bound}. Eng kichik butun son: {bound + 1}."}


JOBS = [("plumber", "visit fee"), ("electrician", "service fee"), ("tutor", "registration fee"),
        ("mechanic", "inspection fee"), ("photographer", "booking fee")]


def linear_cost(rng: random.Random) -> dict:
    job, fee_name = rng.choice(JOBS)
    fee = rng.choice([20, 25, 30, 35, 40, 45, 50, 60, 75])
    rate = rng.choice([15, 20, 25, 30, 35, 40, 45, 50, 60])
    hours = rng.randint(2, 8)
    total = fee + rate * hours
    return {"t": "Algebra",
            "q": f"A {job} charges a ${fee} {fee_name} plus ${rate} per hour of work. What is the total cost, in dollars, of a {hours}-hour job?",
            "answer": fmt(total), "wrong": [fmt((fee + rate) * hours), fmt(fee * hours + rate), fmt(rate * hours), fmt(total + rate)],
            "e": f"Jami: {fee} + {rate}·{hours} = {fee} + {rate * hours} = {total} dollar."}


# ---------------------------------------------------------------- Advanced Math

def quadratic_value(rng: random.Random) -> dict:
    a, b, c = rng.randint(1, 4), rng.randint(-6, 6), rng.randint(-9, 9)
    k = rng.choice([-4, -3, -2, -1, 2, 3])
    value = a * k * k + b * k + c
    steps = [f"{a}·{par(k)}²"] + ([f"{signed(b)}·{par(k)}"] if b else []) + ([signed(c)] if c else [])
    return {"t": "Advanced Math", "q": f"If f(x) = {poly(a, b, c)}, what is the value of f({k})?", "answer": fmt(value),
            "wrong": [fmt(a * k * k - b * k + c), fmt((a * k) ** 2 + b * k + c), fmt(a * k * k + b * k), fmt(value + 2 * a)],
            "e": f"f({k}) = {' '.join(steps)} = {value}."}


def composition(rng: random.Random) -> dict:
    a, b, c = rng.randint(2, 5), rng.randint(-6, 8), rng.randint(-5, 6)
    k = rng.randint(1, 4) * rng.choice([1, -1])
    g_k, f_k = k * k + c, a * k + b
    answer = a * g_k + b
    return {"t": "Advanced Math",
            "q": f"If f(x) = {poly(a, b)} and g(x) = {poly(1, 0, c)}, what is the value of f(g({k}))?",
            "answer": fmt(answer), "wrong": [fmt(f_k * f_k + c), fmt(f_k + g_k), fmt(f_k * g_k), fmt(answer + a)],
            "e": f"Avval g({k}) = {par(k)}² {signed(c)} = {g_k}. Keyin f({g_k}) = {a}·{par(g_k)} {signed(b)} = {answer}."}


def root_sum(rng: random.Random) -> dict:
    r, s = rng.sample([-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8], 2)
    b, c = -(r + s), r * s
    return {"t": "Advanced Math", "q": f"What is the sum of the solutions to the equation {poly(1, b, c)} = 0?",
            "answer": fmt(r + s), "wrong": [fmt(c), fmt(-(r + s)), fmt(max(r, s)), fmt(abs(r) + abs(s) + 1)],
            "e": f"{poly(1, b, c)} = ({poly(1, -r)})({poly(1, -s)}), yechimlar {r} va {s}. Yig'indi: {r + s}."}


def positive_root(rng: random.Random) -> Optional[dict]:
    p, q = rng.randint(1, 9), rng.randint(1, 9)
    if p == q:
        return None
    b, c = q - p, -p * q
    return {"t": "Advanced Math", "q": f"What is the positive solution to the equation {poly(1, b, c)} = 0?",
            "answer": fmt(p), "wrong": [fmt(q), fmt(p * q), fmt(p + q), fmt(-q)],
            "e": f"{poly(1, b, c)} = (x - {p})(x + {q}), yechimlar {p} va -{q}. Musbat yechim: {p}."}


def exponent_equation(rng: random.Random) -> dict:
    base = rng.choice([2, 3, 5])
    k = rng.randint(3, {2: 7, 3: 5, 5: 4}[base])
    s = rng.randint(1, k - 1)
    value = base ** k
    return {"t": "Advanced Math", "q": f"If {base}^(x + {s}) = {value}, what is the value of x?", "answer": fmt(k - s),
            "wrong": [fmt(k), fmt(k + s), fmt(Fraction(value, base * s)), fmt(k - s + 2)],
            "e": f"{value} = {base}^{k}, demak x + {s} = {k} va x = {k - s}."}


def doubling(rng: random.Random) -> dict:
    start = rng.choice([100, 150, 200, 250, 300, 400, 500, 800, 1000, 1500])
    period, times = rng.choice([2, 3, 4, 5, 6, 10]), rng.randint(2, 4)
    total = start * 2 ** times
    return {"t": "Advanced Math",
            "q": f"A colony of {start} bacteria doubles in size every {period} hours. How many bacteria will there be after {period * times} hours?",
            "answer": fmt(total), "wrong": [fmt(start * 2 * times), fmt(start * times), fmt(start * 2 ** (times + 1)), fmt(start + 2 ** times)],
            "e": f"{period * times} soatda koloniya {times} marta ikki baravar o'sadi: {start}·2^{times} = {start}·{2 ** times} = {total}."}


# ---------------------------------------------------------------- Problem-Solving and Data Analysis

ITEMS = ["jacket", "pair of sneakers", "backpack", "desk lamp", "pair of headphones", "bicycle helmet"]


def sale_price(rng: random.Random) -> dict:
    item = rng.choice(ITEMS)
    price, percent = rng.choice(range(40, 401, 20)), rng.choice([10, 15, 20, 25, 30, 35, 40, 45, 50])
    discount = price * percent // 100
    answer = price - discount
    return {"t": "Problem-Solving and Data Analysis",
            "q": f"A {item} originally costs ${price}. It is on sale for {percent}% off. What is the sale price, in dollars?",
            "answer": fmt(answer), "wrong": [fmt(discount), fmt(price - percent), fmt(price + discount), fmt(answer - percent)],
            "e": f"Chegirma: {price}·{percent}/100 = {discount}. Yangi narx: {price} - {discount} = {answer} dollar."}


def percent_increase(rng: random.Random) -> Optional[dict]:
    item = rng.choice(ITEMS)
    old, percent = rng.choice([20, 25, 40, 50, 60, 80, 120, 160, 200, 250, 400]), rng.choice([10, 15, 20, 25, 30, 40, 50, 60, 75])
    if old * percent % 100:
        return None
    new = old + old * percent // 100
    of_new = round((new - old) / new * 100, 1)
    return {"t": "Problem-Solving and Data Analysis",
            "q": f"The price of a {item} increased from ${old} to ${new}. By what percent did the price increase?",
            "answer": f"{percent}%", "wrong": [f"{new - old}%", f"{of_new:g}%", f"{percent + 10}%", f"{100 + percent}%"],
            "e": f"O'sish: {new} - {old} = {new - old}. Foiz eski narxdan olinadi: {new - old}/{old}·100 = {percent}%."}


GROUPS = [("red marbles", "blue marbles", "marbles in a bag"), ("boys", "girls", "students in a club"),
          ("fiction books", "nonfiction books", "books on a shelf"), ("cats", "dogs", "pets at a shelter")]


def ratio_part(rng: random.Random) -> dict:
    first, second, whole = rng.choice(GROUPS)
    r, b = rng.sample(range(1, 9), 2)
    unit = rng.randint(3, 12)
    total = (r + b) * unit
    return {"t": "Problem-Solving and Data Analysis",
            "q": f"The ratio of {first} to {second} among the {whole} is {r}:{b}. If there are {total} in all, how many are {second}?",
            "answer": fmt(b * unit), "wrong": [fmt(r * unit), fmt(unit), fmt(total - unit), fmt(Fraction(total * b, r))],
            "e": f"Jami {r} + {b} = {r + b} qism, bir qism = {total}/{r + b} = {unit}. Javob: {b}·{unit} = {b * unit}."}


def unit_rate(rng: random.Random) -> Optional[dict]:
    speed, hours, other = rng.randint(4, 15) * 5, rng.randint(2, 5), rng.randint(2, 8)
    if hours == other:
        return None
    distance = speed * hours
    return {"t": "Problem-Solving and Data Analysis",
            "q": f"A car travels {distance} miles in {hours} hours. At this rate, how many miles will it travel in {other} hours?",
            "answer": fmt(speed * other), "wrong": [fmt(distance + other), fmt(distance * other), fmt(speed), fmt(Fraction(distance * hours, other))],
            "e": f"Tezlik: {distance}/{hours} = {speed} mil/soat. {other} soatda: {speed}·{other} = {speed * other} mil."}


def missing_value(rng: random.Random) -> Optional[dict]:
    mean = rng.randint(8, 30)
    known = [rng.randint(mean - 6, mean + 6) for _ in range(4)]
    fifth = 5 * mean - sum(known)
    if fifth <= 0:
        return None
    wrong = [value for value in (mean, 4 * mean - sum(known), round(sum(known) / 4), fifth + 5) if value > 0]
    return {"t": "Problem-Solving and Data Analysis",
            "q": f"The mean of five numbers is {mean}. Four of the numbers are {', '.join(map(str, known))}. What is the fifth number?",
            "answer": fmt(fifth), "wrong": [fmt(value) for value in wrong],
            "e": f"Beshta sonning yig'indisi: 5·{mean} = {5 * mean}. Beshinchi son: {5 * mean} - {sum(known)} = {fifth}."}


def median(rng: random.Random) -> Optional[dict]:
    values = rng.sample(range(1, 40), 7)
    ordered = sorted(values)
    middle = ordered[3]
    if values[3] == middle:
        return None
    return {"t": "Problem-Solving and Data Analysis",
            "q": f"What is the median of the data set {', '.join(map(str, values))}?",
            "answer": fmt(middle), "wrong": [fmt(values[3]), f"{round(sum(values) / 7, 1):g}", fmt(ordered[2]), fmt(ordered[4])],
            "e": f"Avval tartiblang: {', '.join(map(str, ordered))}. O'rtadagi, ya'ni 4-qiymat: {middle}."}


def probability(rng: random.Random) -> dict:
    red, blue, green = rng.randint(2, 9), rng.randint(2, 9), rng.randint(2, 6)
    total = red + blue + green
    answer = Fraction(blue, total)
    shown = f"{blue}/{total}" + (f" = {fmt(answer)}" if answer.denominator != total else "")
    return {"t": "Problem-Solving and Data Analysis",
            "q": f"A bag contains {red} red, {blue} blue, and {green} green marbles. If one marble is chosen at random, what is the probability that it is blue?",
            "answer": fmt(answer), "wrong": [fmt(Fraction(red, total)), fmt(Fraction(blue, total - blue)), fmt(Fraction(1, total)), fmt(Fraction(blue, red))],
            "e": f"Ko'k sharlar: {blue} ta, jami: {total} ta. Ehtimollik: {shown}."}


# ---------------------------------------------------------------- Geometry and Trigonometry

def rectangle_area(rng: random.Random) -> Optional[dict]:
    length, width = rng.randint(5, 20), rng.randint(2, 15)
    if length == width:
        return None
    perimeter = 2 * (length + width)
    return {"t": "Geometry and Trigonometry",
            "q": f"A rectangle has a perimeter of {perimeter} centimeters and a length of {length} centimeters. What is the area of the rectangle, in square centimeters?",
            "answer": fmt(length * width), "wrong": [fmt(length * (perimeter - length)), fmt(length + width), fmt(2 * length * width), fmt(perimeter * length // 4)],
            "e": f"Eni: {perimeter}/2 - {length} = {width}. Yuzasi: {length}·{width} = {length * width} kv. sm."}


TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29)]


def hypotenuse(rng: random.Random) -> dict:
    a0, b0, c0 = rng.choice(TRIPLES)
    k = rng.randint(1, 3)
    a, b, c = a0 * k, b0 * k, c0 * k
    return {"t": "Geometry and Trigonometry",
            "q": f"A right triangle has legs of lengths {a} and {b}. What is the length of the hypotenuse?",
            "answer": fmt(c), "wrong": [fmt(a + b), fmt(c * c), fmt(c + k), fmt(b + 1)],
            "e": f"Pifagor teoremasi: {a}² + {b}² = {a * a} + {b * b} = {c * c}. Gipotenuza: √{c * c} = {c}."}


def circle_circumference(rng: random.Random) -> dict:
    r = rng.randint(2, 20)
    return {"t": "Geometry and Trigonometry",
            "q": f"A circle has an area of {r * r}π square units. What is the circumference of the circle?",
            "answer": f"{2 * r}π", "wrong": [f"{r}π", f"{r * r}π", f"{2 * r * r}π", f"{4 * r}π"],
            "e": f"πr² = {r * r}π, demak r = {r}. Aylana uzunligi: 2πr = {2 * r}π."}


def third_angle(rng: random.Random) -> Optional[dict]:
    a, b = rng.randint(25, 90), rng.randint(20, 80)
    if a + b >= 170:
        return None
    c = 180 - a - b
    return {"t": "Geometry and Trigonometry",
            "q": f"In a triangle, two of the angles measure {a}° and {b}°. What is the measure of the third angle?",
            "answer": f"{c}°", "wrong": [f"{360 - a - b}°", f"{a + b}°", f"{c + 10}°", f"{abs(90 - c)}°"],
            "e": f"Uchburchak burchaklari yig'indisi 180°: 180 - {a} - {b} = {c}°."}


TEMPLATES: list[Callable[[random.Random], Optional[dict]]] = [
    linear_equation, expression_value, slope, line_value, system_sum, system_elimination, absolute_sum,
    least_integer, linear_cost, quadratic_value, composition, root_sum, positive_root, exponent_equation,
    doubling, sale_price, percent_increase, ratio_part, unit_rate, missing_value, median, probability,
    rectangle_area, hypotenuse, circle_circumference, third_angle,
]


def build() -> list[dict]:
    items: list[dict] = []
    for index, template in enumerate(TEMPLATES):
        rng = random.Random(SEED + index)
        seen: set[str] = set()
        made, attempts = 0, 0
        while made < PER_TEMPLATE:
            attempts += 1
            if attempts > 2000:
                raise RuntimeError(f"{template.__name__} cannot make {PER_TEMPLATE} different questions")
            raw = template(rng)
            if raw is None or raw["q"] in seen:
                continue
            wrong: list[str] = []
            for option in raw["wrong"]:
                if option != raw["answer"] and option not in wrong:
                    wrong.append(option)
            if len(wrong) < 3:
                continue
            options = [raw["answer"], *wrong[:3]]
            rng.shuffle(options)
            seen.add(raw["q"])
            items.append({"t": raw["t"], "q": raw["q"], "o": options, "a": options.index(raw["answer"]), "e": raw["e"]})
            made += 1
    return items


def main() -> None:
    items = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(items, ensure_ascii=False, indent=0) + "\n", encoding="utf-8")
    print(f"{len(items)} questions written to {OUT}")


if __name__ == "__main__":
    main()
