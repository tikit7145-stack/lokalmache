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


def create_order_status_card(status_label, count, color, status_key):
    """Kriye kat estati kòmand"""
    return html.Div(
        className="status-card",
        style={'borderLeft': f'4px solid {color}', 'borderRadius': '8px'},
        children=[
            html.Div(
                className="status-header",
                children=[
                    html.Span(status_label, className="status-label"),
                    html.Span(str(count), className="status-count", style={'color': color})
                ]
            ),
        ]
    )


def create_order_timeline():
    """Kriye timeline pou suiv kòmand"""
    return html.Div(
        className="order-timeline",
        children=[
            html.Div(
                className="timeline-step",
                children=[
                    html.Div(className="timeline-marker pending"),
                    html.Span("⏳ Atant")
                ]
            ),
            html.Div(className="timeline-line"),
            html.Div(
                className="timeline-step",
                children=[
                    html.Div(className="timeline-marker confirmed"),
                    html.Span("✅ Konfime")
                ]
            ),
            html.Div(className="timeline-line"),
            html.Div(
                className="timeline-step",
                children=[
                    html.Div(className="timeline-marker transit"),
                    html.Span("🚚 Nan Wout")
                ]
            ),
            html.Div(className="timeline-line"),
            html.Div(
                className="timeline-step",
                children=[
                    html.Div(className="timeline-marker delivered"),
                    html.Span("📦 Rive")
                ]
            ),
        ]
    )


def create_order_status_badge(status):
    """Kriye badge pou estati kòmand"""
    status_colors = {
        'pending': '#FFA500',
        'confirmed': '#4CAF50',
        'in_transit': '#2196F3',
        'delivered': '#673AB7',
    }
    
    status_labels = {
        'pending': '⏳ Atant',
        'confirmed': '✅ Konfime',
        'in_transit': '🚚 Nan Wout',
        'delivered': '📦 Rive',
    }
    
    return html.Span(
        status_labels.get(status, status),
        style={
            'backgroundColor': status_colors.get(status, '#999'),
            'color': 'white',
            'padding': '4px 12px',
            'borderRadius': '20px',
            'fontSize': '0.85rem',
            'fontWeight': 'bold'
        }
    )

