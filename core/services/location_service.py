def normalize_location(location):
    """Normalize a location name for consistent aggregation."""

    if not location:
        return location

    location = location.strip()

    parts = [part.strip() for part in location.split(",")]

    if parts:
        return parts[0]

    return location