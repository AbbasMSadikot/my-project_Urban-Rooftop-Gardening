"""Defensively parse user input for the solar panel estimate exercise."""

from decimal import Decimal, InvalidOperation
import re


def clean_site_name(name):
    """Trim a site name, remove ``#`` and ``@``, and title-case it.

    Non-string values and strings with no usable characters produce an empty
    string, so callers can safely display the result without an exception.
    """
    if not isinstance(name, str):
        return ""

    cleaned = name.strip().replace("#", "").replace("@", "").strip()
    return cleaned.title()


def parse_monthly_units(text):
    """Parse a non-negative whole kWh reading, returning ``None`` if invalid."""
    if isinstance(text, bool):
        return None
    if isinstance(text, int):
        return text if text >= 0 else None
    if not isinstance(text, str):
        return None

    value = text.strip()
    match = re.fullmatch(r"\+?(\d{1,3}(?:,\d{3})+|\d+)\s*(?:kwh)?", value, re.IGNORECASE)
    if not match:
        return None

    try:
        return int(match.group(1).replace(",", ""))
    except (ValueError, OverflowError):
        return None


def panels_for_roof(text):
    """Return the count of 18 sq ft panels fitting a roof, or zero if invalid."""
    if not isinstance(text, str) or len(text) > 256:
        return 0

    number = r"(?:\d+(?:\.\d*)?|\.\d+)"
    match = re.fullmatch(
        rf"\s*({number})\s*(?:ft)?\s*[x×]\s*({number})\s*(?:ft)?\s*",
        text,
        re.IGNORECASE,
    )
    if not match:
        return 0

    try:
        length = Decimal(match.group(1))
        width = Decimal(match.group(2))
        if not length.is_finite() or not width.is_finite():
            return 0
        if length <= 0 or width <= 0:
            return 0
        return int((length * width) // Decimal(18))
    except (InvalidOperation, ValueError, OverflowError):
        return 0


def main():
    print("==== Running clean_site_name ====")
    value = input("Enter the installation site name: ")
    print("Site name:", clean_site_name(value))

    print("\n==== Running parse_monthly_units ====")
    value = input("Enter monthly electricity use (e.g. 320 kWh): ")
    parsed_units = parse_monthly_units(value)
    print("Monthly units:", parsed_units if parsed_units is not None else "Invalid input")

    print("\n==== Running panels_for_roof ====")
    value = input("Enter roof size as LENGTHft x WIDTHft (e.g. 20ft x 15ft): ")
    print("Panels that fit:", panels_for_roof(value))


if __name__ == "__main__":
    main()
