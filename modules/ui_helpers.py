def kpi_card(label: str, value: str) -> str:
    """Return HTML for a single KPI card used in the hospital dashboard.

    Args:
        label: The KPI label (e.g., "Total Patients").
        value: The formatted value to display.
    """
    return f'''<div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
    </div>'''
