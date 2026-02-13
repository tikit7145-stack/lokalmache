"""
Komponan Ritilijab pou Dashboard
"""

from dash import html


def create_card(title, content, className=""):
    """Kriye yon kat glassmorphism"""
    return html.Div(
        className=f"card-glassmorphism {className}",
        children=[
            html.H3(title, className="card-title"),
            html.Div(content, className="card-content"),
        ]
    )


def create_metric_card(label, value, subtitle, card_id):
    """Kriye yon kat metrik"""
    return html.Div(
        className=f"metric-card {card_id}",
        children=[
            html.Div(
                className="metric-header",
                children=[html.H4(label, className="metric-label")]
            ),
            html.Div(
                className="metric-value",
                children=[html.H2(value)]
            ),
            html.Div(
                className="metric-subtitle",
                children=[html.P(subtitle)]
            ),
        ]
    )


def create_stat_box(icon, title, value, trend=""):
    """Kriye yon bwat estatistik"""
    trend_color = "positive" if "+" in trend else "negative" if "-" in trend else ""
    
    return html.Div(
        className="stat-box-glassmorphism",
        children=[
            html.Div(
                className="stat-icon",
                children=[html.Span(icon, className="icon-text")]
            ),
            html.Div(
                className="stat-content",
                children=[
                    html.H4(title, className="stat-title"),
                    html.H3(value, className="stat-value"),
                    html.P(trend, className=f"stat-trend {trend_color}") if trend else html.P(),
                ]
            ),
        ]
    )
