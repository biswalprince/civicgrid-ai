from ..models import InfrastructureIndicator


def calculate_infrastructure_gap(district, category):
    """
    Calculate a 0-10 infrastructure gap score from
    an available percentage-based coverage indicator.
    """

    if not district:
        return None

    indicator = (
        InfrastructureIndicator.objects
        .filter(
            district=district,
            category__iexact=category,
            indicator__iexact="coverage",
        )
        .first()
    )

    if not indicator:
        return None

    if indicator.unit.lower() != "percent":
        return None

    coverage = max(0, min(100, indicator.value))

    gap_percent = 100 - coverage

    gap_score = round(gap_percent / 10)

    return max(0, min(10, gap_score))