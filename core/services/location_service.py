def normalize_location(location):
    """Normalize a location name for consistent aggregation."""

    if not location:
        return location

    location = location.strip()

    parts = [part.strip() for part in location.split(",")]

    if parts:
        return parts[0]

    return location


LOCATION_TO_DISTRICT = {
    "Bhubaneswar": "Khordha",
    "Khordha": "Khordha",
    "Khordha district": "Khordha",
    "Cuttack": "Cuttack",
    "Puri": "Puri",
    "Berhampur": "Ganjam",
    "Sundargarh": "Sundargarh",
}


def get_district_for_location(location):
    """Return the district name for a normalized location."""

    normalized_location = normalize_location(location)

    if not normalized_location:
        return None

    normalized_location = normalized_location.strip().lower()

    for location_name, district_name in LOCATION_TO_DISTRICT.items():
        if normalized_location == location_name.lower():
            return district_name

    return None