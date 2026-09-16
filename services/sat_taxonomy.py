"""
EduTest Pro - Digital SAT Official Taxonomy
Standardized 4 Math Domains and 4 Reading/Writing Domains with granular skill mapping,
aligned 100% with the official Digital SAT specification.
"""

from typing import Any

# ==================== DIGITAL SAT TAXONOMY MAP ====================

SAT_TAXONOMY: dict[str, dict[str, list[str]]] = {
    "math": {
        "Algebra": [
            "Linear equations in one variable",
            "Linear equations in two variables",
            "Linear functions and graphing (slopes, intercepts)",
            "Systems of two linear equations in two variables",
            "Linear inequalities in one or two variables"
        ],
        "Advanced Math": [
            "Equivalent expressions (factoring, polynomial arithmetic)",
            "Nonlinear equations in one variable (quadratic, radical, absolute value)",
            "Systems of equations in two variables (linear-quadratic systems)",
            "Nonlinear functions (quadratic vertex/standard form, exponential models, polynomials)"
        ],
        "Problem-Solving and Data Analysis": [
            "Ratios, rates, proportional relationships, and unit conversion",
            "Percentages (increase, decrease, markups, successive changes)",
            "One-variable data: distributions, mean, median, and spread",
            "Two-variable data: models and scatterplots",
            "Probability and conditional probability from two-way tables",
            "Inference from sample statistics and margin of error"
        ],
        "Geometry and Trigonometry": [
            "Area and volume formulas (circles, cylinders, prisms)",
            "Lines, angles, and triangles (congruence, similarity, Pythagorean theorem, special triangles)",
            "Right triangle trigonometry (sine, cosine, tangent, complementary angles)",
            "Circles (equations, radius, arc length, sector area)"
        ]
    },
    "reading": {
        "Craft and Structure": [
            "Words in Context (tier-2 academic vocabulary in sentence context)",
            "Text Structure and Purpose (overall structure, function of underlined portion)",
            "Cross-Text Connections (comparing viewpoints in paired texts)"
        ],
        "Information and Ideas": [
            "Central Ideas and Details (main themes and specific stated claims)",
            "Command of Evidence: Textual (finding passage evidence to support/weaken a claim)",
            "Command of Evidence: Quantitative (interpreting informational tables/graphs)",
            "Inferences (drawing logical conclusions from passage premises)"
        ]
    },
    "writing": {
        "Standard English Conventions": [
            "Boundaries (sentence boundaries: comma splices, run-ons, semicolons, colons, dashes)",
            "Form, Structure, and Sense (subject-verb agreement, pronoun-antecedent agreement, verb tense)",
            "Modifiers and Parallelism (dangling modifiers, misplaced modifiers, parallel structures)"
        ],
        "Expression of Ideas": [
            "Transitions (contrast, cause-effect, addition, illustration connectors)",
            "Rhetorical Synthesis (synthesizing provided bullet-point research notes)"
        ]
    }
}

VALID_SECTIONS = tuple(SAT_TAXONOMY.keys())
VALID_DIFFICULTIES = ("Easy", "Medium", "Hard")
VALID_STATUSES = ("draft", "review", "published", "rejected", "pending_human_review")


def get_domains_for_section(section: str) -> list[str]:
    """Returns official domains for a given section."""
    sec = section.lower().strip()
    return list(SAT_TAXONOMY.get(sec, {}).keys())


def get_skills_for_domain(section: str, domain: str) -> list[str]:
    """Returns specific skills for a section and domain."""
    sec = section.lower().strip()
    domains = SAT_TAXONOMY.get(sec, {})
    # Match exact or partial domain
    for d_name, skills in domains.items():
        if d_name.lower() == domain.lower() or domain.lower() in d_name.lower():
            return skills
    return []


def validate_taxonomy_item(section: str, domain: str, skill: str | None = None) -> tuple[bool, str]:
    """Validates whether a section, domain, and optional skill conform to SAT standards."""
    sec = section.lower().strip()
    if sec not in SAT_TAXONOMY:
        return False, f"Invalid section '{sec}'. Must be one of {list(SAT_TAXONOMY.keys())}"

    matched_domain = None
    for d_name in SAT_TAXONOMY[sec]:
        if d_name.lower() == domain.lower() or domain.lower() in d_name.lower():
            matched_domain = d_name
            break

    if not matched_domain:
        return False, f"Domain '{domain}' does not belong to section '{sec}'. Available: {list(SAT_TAXONOMY[sec].keys())}"

    if skill:
        skills = SAT_TAXONOMY[sec][matched_domain]
        matched_skill = any(s.lower() == skill.lower() or skill.lower() in s.lower() for s in skills)
        if not matched_skill:
            return False, f"Skill '{skill}' not found in domain '{matched_domain}'"

    return True, "Valid"
