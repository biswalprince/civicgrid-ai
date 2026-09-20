CATEGORY_WEIGHTS = {
    "water": {
        "severity": 4,
        "affected_population": 3,
        "infrastructure_gap": 3,
        "vulnerability": 2,
    },
    "roads": {
        "severity": 4,
        "affected_population": 4,
        "infrastructure_gap": 2,
        "vulnerability": 1,
    },
    "sanitation": {
        "severity": 4,
        "affected_population": 3,
        "infrastructure_gap": 3,
        "vulnerability": 2,
    },
}

DEFAULT_WEIGHTS = {
    "severity": 4,
    "affected_population": 3,
    "infrastructure_gap": 2,
    "vulnerability": 1,
}


def get_category_weights(category):
    if not category:
        return DEFAULT_WEIGHTS

    return CATEGORY_WEIGHTS.get(
        category.lower(),
        DEFAULT_WEIGHTS,
    )


def calculate_base_priority(details):
    weights = get_category_weights(details.get("category"))

    return (
        details["severity"] * weights["severity"]
        + details["affected_population"] * weights["affected_population"]
        + details["infrastructure_gap"] * weights["infrastructure_gap"]
        + details["vulnerability"] * weights["vulnerability"]
    )


def calculate_context_multiplier(district):
    if not district:
        return 1.0

    rural_ratio = 0

    if district.population > 0:
        rural_ratio = district.rural_population / district.population

    literacy_disadvantage = max(
        0,
        (80 - district.literacy_rate) / 20,
    )

    multiplier = (
        1.0
        + (rural_ratio * 0.1)
        + (literacy_disadvantage * 0.05)
    )

    return round(multiplier, 2)


def get_priority_breakdown(details, district=None):
    weights = get_category_weights(details.get("category"))

    severity_score = details["severity"] * weights["severity"]
    affected_population_score = (
        details["affected_population"]
        * weights["affected_population"]
    )
    infrastructure_gap_score = (
        details["infrastructure_gap"]
        * weights["infrastructure_gap"]
    )
    vulnerability_score = (
        details["vulnerability"]
        * weights["vulnerability"]
    )

    base_score = (
        severity_score
        + affected_population_score
        + infrastructure_gap_score
        + vulnerability_score
    )

    context_multiplier = calculate_context_multiplier(district)
    final_score = round(base_score * context_multiplier)

    if final_score < 30:
        priority_level = "LOW"
    elif final_score < 60:
        priority_level = "MEDIUM"
    else:
        priority_level = "HIGH"

    return {
        "category": details.get("category"),
        "weights": weights,
        "severity": severity_score,
        "affected_population": affected_population_score,
        "infrastructure_gap": infrastructure_gap_score,
        "vulnerability": vulnerability_score,
        "base_score": base_score,
        "context_multiplier": context_multiplier,
        "final_score": final_score,
        "priority_level": priority_level,
    }


def calculate_priority_score(details, district=None):
    breakdown = get_priority_breakdown(
        details=details,
        district=district,
    )

    return breakdown["final_score"]