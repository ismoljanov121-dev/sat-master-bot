import hashlib, random, re

# Standalone option letter in an explanation: "B", "(B)", "B varianti", "C va D", "javob: B".
# Skips formulas ("D = b^2", "x = C"), points ("C(3, 4)"), units ("35°C") and percents ("A%").
OPTION_REF = re.compile(r"(?<![\w'’ʻ=+*/^°-])(?<!=\s)([A-D])(?![\w'’ʻ%])(?!\s*=)(?!\()")
# "A student ..." is the English article, "A varianti" is an option.
ARTICLE = re.compile(r"\s+(?!variant|va\b|da\b|ni\b|dagi\b|esa\b|ham\b|yoki\b|dir\b|javob|faqat\b|to'g'ri|noto'g'ri|ga\b|dan\b|is\b|are\b|and\b|or\b)[a-z]")
CHOICE_WORD = re.compile(r"(?:choice|option|variant)\s+$", re.I)
NAME_WORD = re.compile(r"(?:vitamin|hepatitis|type|class|grade|group|plan|point|angle|section|company)\s+$", re.I)
GENERIC = re.compile(r"(neither A nor B|offers A but lacks B, Y excels at B at the cost of A)", re.I)
# The stem uses capital letters as names ("Plan A", "Company B"), so its explanation stays as written.
ENTITY_LETTER = re.compile(r"(?<![\w'’ʻ])(?:[B-D]|(?<=\s)A(?=\s+(?:and|or|is|are|has|have|costs?|charges?|to|va)\b))(?![\w'’ʻ])")


def swap_letters(text, remap):
    def swap_part(part):
        def repl(m):
            before = part[:m.start()]
            article = m.group(1) == "A" and ARTICLE.match(part, m.end()) and not CHOICE_WORD.search(before)
            return m.group(0) if article or NAME_WORD.search(before) else remap[m.group(1)]
        return OPTION_REF.sub(repl, part)
    return "".join(p if i % 2 else swap_part(p) for i, p in enumerate(GENERIC.split(text)))


def rebalance_options(q):
    """Stable shuffle: the key stops being always A, and stays the same between builds."""
    if ENTITY_LETTER.search(f"{q['q']} {q['pas']}"):
        return q
    opts = q["opts"]
    letters = [o["key"] for o in opts]
    order = list(range(len(opts)))
    random.Random(hashlib.sha256(q["id"].encode()).digest()).shuffle(order)
    remap = {opts[i]["key"]: letters[pos] for pos, i in enumerate(order)}
    q["opts"] = [{"key": letters[pos], "text": opts[i]["text"]} for pos, i in enumerate(order)]
    q["cor"] = remap[q["cor"]]
    q["exp"], q["strat"] = swap_letters(q["exp"], remap), swap_letters(q["strat"], remap)
    return q
