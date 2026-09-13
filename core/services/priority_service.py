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


def calculate_priority_score(details, district=None):
    base_score = calculate_base_priority(details)
    context_multiplier = calculate_context_multiplier(district)

    final_score = base_score * context_multiplier

    return round(final_score)