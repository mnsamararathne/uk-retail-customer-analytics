# ============================================================
# FORMATTING UTILITIES
# UK RETAIL CUSTOMER ANALYTICS
# ============================================================


def format_currency(value):
    """
    Convert numeric values into compact GBP notation.

    Examples:
    950        -> £950
    12500      -> £12.5K
    2500000    -> £2.5M
    """

    if value is None:
        return "N/A"

    value = float(value)

    if abs(value) >= 1_000_000:
        return f"£{value / 1_000_000:.1f}M"

    if abs(value) >= 1_000:
        return f"£{value / 1_000:.1f}K"

    return f"£{value:,.0f}"


def format_number(value):
    """
    Format large numbers using compact notation.
    """

    if value is None:
        return "N/A"

    value = float(value)

    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"

    if abs(value) >= 1_000:
        return f"{value / 1_000:.1f}K"

    return f"{value:,.0f}"


def format_percentage(
    value,
    decimals=1
):
    """
    Format an already-calculated percentage.
    """

    if value is None:
        return "N/A"

    return f"{float(value):.{decimals}f}%"


def format_decimal(
    value,
    decimals=2
):
    """
    Format a decimal value consistently.
    """

    if value is None:
        return "N/A"

    return f"{float(value):,.{decimals}f}"