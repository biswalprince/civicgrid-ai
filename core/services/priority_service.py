def calculate_base_priority(details):
    return (
        details["severity"] * 4
        + details["affected_population"] * 3
        + details["infrastructure_gap"] * 2
        + details["vulnerability"]
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

    multiplier = 1.0 + (rural_ratio * 0.1) + (literacy_disadvantage * 0.05)

    return round(multiplier, 2)


def get_priority_breakdown(details, district=None):
    severity_score = details["severity"] * 4
    affected_population_score = details["affected_population"] * 3
    infrastructure_gap_score = details["infrastructure_gap"] * 2
    vulnerability_score = details["vulnerability"]

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