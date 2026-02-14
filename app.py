"""
Aplikasyon Dashboard E-Commerce - 2026
Dysèn: Glassmorphism Style
Tout tèks an Kreyòl Ayisyen
"""

import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime, timedelta
import os

# Importe database ak components
from src.database import get_supabase_manager
from src.components import create_card, create_metric_card, create_order_status_card, create_order_timeline
from src.order_manager import OrderStatusManager

# Inisyalize aplikasyon
app = dash.Dash(__name__, external_stylesheets=['assets/style.css'])
app.title = "LokalMache"

# Koneksyon ak database
db = get_supabase_manager()

# Chaje done reyel soti nan Supabase
def load_real_data():
    """Chaje tout done reyel soti nan Supabase"""
    try:
        orders = db.get_orders(limit=100)
        products = db.get_products(limit=100)
        customers = db.get_customers(limit=100)
        return orders, products, customers
    except Exception as e:
        print(f"❌ Erè nan chajman done: {e}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

orders_data, products_data, customers_data = load_real_data()

# ============================================================
# CHART CREATION FUNCTIONS - Defined before layout
# ============================================================

def create_sales_chart(data):
    """Kriye graf ven pa jou - done reyel soti nan Supabase"""
    if data.empty:
        return {
            'data': [go.Scatter(x=[], y=[], mode='lines+markers', name='Ven')],
            'layout': go.Layout(title="Enkatil done vann", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        }
    
    # Prepare data from orders (created_at, total_amount)
    if 'created_at' in data.columns and 'total_amount' in data.columns:
        data_copy = data.copy()
        data_copy['created_at'] = pd.to_datetime(data_copy['created_at'], errors='coerce')
        daily_sales = data_copy.groupby(data_copy['created_at'].dt.date)['total_amount'].sum()
    else:
        daily_sales = pd.Series([0], index=[datetime.now().date()])
    
    return {
        'data': [
            go.Scatter(
                x=daily_sales.index,
                y=daily_sales.values,
                mode='lines+markers',
                name='Ven',
                line=dict(color='rgba(100, 200, 255, 0.8)', width=3),
                marker=dict(size=8, color='rgba(100, 200, 255, 1)'),
                fill='tozeroy',
                fillcolor='rgba(100, 200, 255, 0.2)',
            )
        ],
        'layout': go.Layout(
            margin=dict(l=40, r=40, t=20, b=40),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                showgrid=False,
                showline=False,
                zeroline=False,
                color='rgba(200, 200, 200, 0.5)'
            ),
            yaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(100, 100, 100, 0.1)',
                zeroline=False,
                color='rgba(200, 200, 200, 0.5)'
            ),
            hovermode='x unified',
            font=dict(family="Segoe UI, sans-serif", color='rgba(200, 200, 200, 0.9)'),
        )
    }

def create_category_chart():
    """Kriye graf katègi pwodwi - done reyel soti nan Supabase"""
    try:
        category_sales = db.get_sales_by_category()
        if category_sales.empty or len(category_sales) == 0:
            categories = ['Sanble', 'Grenn', 'Divès']
            values = [1, 1, 1]
        else:
            categories = category_sales.get('category', ['Sanble', 'Grenn', 'Divès']).tolist()
            values = category_sales.get('total_sales', [1, 1, 1]).tolist()
    except:
        categories = ['Sanble', 'Grenn', 'Divès']
        values = [1, 1, 1]
    
    colors = ['rgba(100, 200, 255, 0.8)', 'rgba(255, 150, 200, 0.8)', 
              'rgba(150, 200, 100, 0.8)', 'rgba(255, 200, 100, 0.8)', 'rgba(200, 150, 255, 0.8)'][:len(categories)]
    
    return {
        'data': [
            go.Pie(
                labels=categories,
                values=values,
                hole=0.3,
                marker=dict(colors=colors, line=dict(color='rgba(255,255,255,0.1)', width=2)),
                textinfo='label+percent',
                textfont=dict(color='rgba(220, 220, 220, 0.9)'),
            )
        ],
        'layout': go.Layout(
            margin=dict(l=0, r=0, t=0, b=0),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Segoe UI, sans-serif", color='rgba(200, 200, 200, 0.9)'),
        )
    }

def create_top_products_chart(data):
    """Kriye graf top pwodwi - done reyel soti nan Supabase"""
    if data.empty:
        return {
            'data': [go.Bar(x=[], y=[])],
            'layout': go.Layout(title="Enkatil done", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        }
    
    if 'price' in data.columns:
        top_products = data.nlargest(5, 'price')
        product_names = top_products.get('name', top_products.index).tolist()
        product_prices = top_products['price'].values.tolist()
    elif 'name' in data.columns:
        top_products = data.head(5)
        product_names = top_products['name'].tolist()
        product_prices = [1] * len(top_products)
    else:
        product_names = ['Pwodwi 1', 'Pwodwi 2', 'Pwodwi 3']
        product_prices = [100, 150, 200]
    
    return {
        'data': [
            go.Bar(
                x=product_prices,
                y=product_names,
                orientation='h',
                marker=dict(
                    color='rgba(100, 200, 255, 0.8)',
                    line=dict(color='rgba(100, 200, 255, 1)', width=2)
                ),
                text=[f"${v:,.0f}" for v in product_prices],
                textposition='outside',
                textfont=dict(color='rgba(200, 200, 200, 0.9)'),
            )
        ],
        'layout': go.Layout(
            margin=dict(l=200, r=40, t=20, b=40),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(100, 100, 100, 0.1)',
                zeroline=False,
                color='rgba(200, 200, 200, 0.5)'
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                color='rgba(200, 200, 200, 0.5)'
            ),
            hovermode='y',
            font=dict(family="Segoe UI, sans-serif", color='rgba(200, 200, 200, 0.9)'),
        )
    }

def create_location_chart(data):
    """Kriye graf distribisyon kliyan - done reyel soti nan Supabase"""
    if data.empty:
        return {
            'data': [go.Bar(x=[], y=[])],
            'layout': go.Layout(title="Enkatil done", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        }
    
    if 'user_address' in data.columns:
        locations = data['user_address'].value_counts().head(6)
    elif 'user_email' in data.columns:
        locations = data['user_email'].str.split('@').str[-1].value_counts().head(6)
    else:
        locations = pd.Series([2, 1, 1], index=['Pòtoprens', 'Cap-Ayisyen', 'Jèremie'])
    
    return {
        'data': [
            go.Bar(
                x=locations.index,
                y=locations.values,
                marker=dict(
                    color='rgba(255, 150, 200, 0.8)',
                    line=dict(color='rgba(255, 150, 200, 1)', width=2)
                ),
                text=locations.values,
                textposition='outside',
                textfont=dict(color='rgba(200, 200, 200, 0.9)'),
            )
        ],
        'layout': go.Layout(
            margin=dict(l=40, r=40, t=20, b=80),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                showgrid=False,
                showline=False,
                zeroline=False,
                color='rgba(200, 200, 200, 0.5)',
                tickangle=-45
            ),
            yaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(100, 100, 100, 0.1)',
                zeroline=False,
                color='rgba(200, 200, 200, 0.5)'
            ),
            hovermode='x unified',
            font=dict(family="Segoe UI, sans-serif", color='rgba(200, 200, 200, 0.9)'),
        )
    }

# CSS stilize aplikasyon

def get_app_layout():
    return html.Div(
        className="main-container",
        children=[
            # Header Navigation
            html.Div(
                className="navbar-glassmorphism",
                children=[
                    html.Div(
                        className="navbar-content",
                        children=[
                            html.H1("🛍️ SENJIVIS KOMÈS 2026", className="navbar-title"),
                            html.Div(
                                className="navbar-menu",
                                children=[
                                    html.Button("📊 Dekamandasyon", className="nav-btn active", id="btn-dashboard"),
                                    html.Button("📦 Pwodwi", className="nav-btn", id="btn-products"),
                                    html.Button("👥 Kliyèn", className="nav-btn", id="btn-customers"),
                                    html.Button("⚙️ Paramèt", className="nav-btn", id="btn-settings"),
                                ]
                            ),
                            html.Span(f"🕐 {datetime.now().strftime('%d/%m/%Y')}", className="datetime-display")
                        ]
                    )
                ]
            ),

            # Main Content
            html.Div(
                className="content-wrapper",
                children=[
                    # Sidebar
                    html.Div(
                        className="sidebar-glassmorphism",
                        children=[
                            html.H3("🎯 FILTRE", className="sidebar-title"),
                            
                            html.Div(
                                className="filter-group",
                                children=[
                                    html.Label("Seleksyon Peryòd:", className="filter-label"),
                                    dcc.Dropdown(
                                        id="period-dropdown",
                                        options=[
                                            {"label": "📅 Jodi a", "value": "today"},
                                            {"label": "📅 Semèn sa a", "value": "week"},
                                            {"label": "📅 Mwa sa a", "value": "month"},
                                            {"label": "📅 Tri an", "value": "year"},
                                        ],
                                        value="month",
                                        className="dropdown-style"
                                    ),
                                ]
                            ),

                            html.Hr(className="divider"),

                            html.Div(
                                className="filter-group",
                                children=[
                                    html.Label("Kategori Pwodwi:", className="filter-label"),
                                    dcc.Dropdown(
                                        id="category-dropdown",
                                        options=[
                                            {"label": "🔍 Tout Kategori", "value": "all"},
                                            {"label": "💻 Teknoloji", "value": "tech"},
                                            {"label": "👗 Vètman", "value": "fashion"},
                                            {"label": "🏠 Lakay", "value": "home"},
                                            {"label": "🍔 Manje", "value": "food"},
                                        ],
                                        value="all",
                                        className="dropdown-style"
                                    ),
                                ]
                            ),

                            html.Hr(className="divider"),

                            html.Button(
                                "🔄 Rafréchi Avèk",
                                className="refresh-btn",
                                id="refresh-btn"
                            ),
                        ]
                    ),

                    # Main Dashboard Area
                    html.Div(
                        className="main-content",
                        children=[
                            # Key Metrics
                            html.Div(
                                className="metrics-container",
                                children=[
                                    create_metric_card(
                                        "💰 TOTAL VANT",
                                        f"${db.get_total_sales():,.2f}",
                                        "dola vann",
                                        "metric-card-1"
                                    ),
                                    create_metric_card(
                                        "👥 KLIYAN",
                                        f"{db.get_customer_count()}",
                                        "kliyèn reyel",
                                        "metric-card-2"
                                    ),
                                    create_metric_card(
                                        "📦 PWODWI DISPO",
                                        f"{len(products_data)}",
                                        "atik",
                                        "metric-card-3"
                                    ),
                                    create_metric_card(
                                        "⭐ EVALYASYON",
                                        "4.8/5",
                                        "sou 5 zetwal",
                                        "metric-card-4"
                                    ),
                                ]
                            ),

                            # Order Status Section
                            html.Div(
                                className="charts-row",
                                id="order-status-section",
                                children=[
                                    html.H3("📋 ESTATI KÒMAND", className="chart-title", style={"width": "100%", "marginBottom": "15px"}),
                                ]
                            ),

                            html.Div(
                                className="status-cards-container",
                                id="status-cards-container",

                                style={
                                    "display": "grid",
                                    "gridTemplateColumns": "repeat(4, 1fr)",
                                    "gap": "15px",
                                    "marginBottom": "30px",
                                    "width": "100%"
                                }
                            ),

                            # Order Status Update Controls
                            html.Div(
                                className="order-status-update-controls",
                                style={"margin": "20px 0", "padding": "20px", "background": "white", "borderRadius": "12px", "border": "1px solid #E1E8ED", "boxShadow": "0 2px 8px rgba(0,0,0,0.08)"},
                                children=[
                                    html.H4("🔄 Modifye Estati Kòmand", style={"marginBottom": "15px", "color": "#2C3E50", "fontSize": "1.1rem", "fontWeight": "700"}),
                                    html.Div([
                                        html.Div([
                                            html.Label("Chwazi Kòmand:", style={"marginBottom": "5px", "fontWeight": "600", "color": "#2C3E50", "display": "block"}),
                                            dcc.Dropdown(
                                                id="order-select-dropdown",
                                                options=[{"label": f"{row['id'][:8]} - {row.get('user_name', 'N/A')} (${row.get('total_amount', 0)})", "value": row['id']} for _, row in orders_data.iterrows()],
                                                value=orders_data['id'].iloc[0] if not orders_data.empty else None,
                                                style={"width": "100%"}
                                            ),
                                        ], style={"flex": "1", "marginRight": "15px"}),
                                        html.Div([
                                            html.Label("Nouvo Estati:", style={"marginBottom": "5px", "fontWeight": "600", "color": "#2C3E50", "display": "block"}),
                                            dcc.Dropdown(
                                                id="status-select-dropdown",
                                                options=[{"label": v['label'], "value": k} for k, v in OrderStatusManager.STATUSES.items()],
                                                value="pending",
                                                style={"width": "100%"}
                                            ),
                                        ], style={"flex": "1", "marginRight": "15px"}),
                                        html.Div([
                                            html.Button(
                                                "✅ Mete ajou", 
                                                id="update-status-btn", 
                                                n_clicks=0, 
                                                style={
                                                    "background": "linear-gradient(135deg, #FF6B35 0%, #E55A2B 100%)",
                                                    "color": "white", 
                                                    "border": "none", 
                                                    "padding": "10px 20px", 
                                                    "borderRadius": "6px", 
                                                    "fontWeight": "bold",
                                                    "cursor": "pointer",
                                                    "width": "100%",
                                                    "height": "42px",
                                                    "marginTop": "22px",
                                                    "fontSize": "0.95rem",
                                                    "boxShadow": "0 4px 12px rgba(255, 107, 53, 0.3)"
                                                }
                                            ),
                                        ], style={"flex": "0.8"}),
                                    ], style={"display": "flex", "gap": "15px", "alignItems": "flex-start"}),
                                    html.Div(id="update-status-message", style={"marginTop": "15px", "padding": "10px 12px", "borderRadius": "6px", "fontSize": "0.95rem", "fontWeight": "600"})
                                ]
                            ),

                            html.Div(
                                className="chart-container-full",
                                children=[
                                    html.H3("⏳📦 Sitèn Kòmand", className="chart-title"),
                                    dcc.Graph(
                                        id="order-status-chart",
                                        className="chart-glassmorphism",
                                    )
                                ]
                            ),

                            # Charts Row 1
                            html.Div(
                                className="charts-row",
                                children=[
                                    html.Div(
                                        className="chart-container-50",
                                        children=[
                                            html.H3("📊 Ven Pa Jou", className="chart-title"),
                                            dcc.Graph(
                                                id="sales-chart",
                                                className="chart-glassmorphism",
                                                figure=create_sales_chart(orders_data)
                                            )
                                        ]
                                    ),
                                    html.Div(
                                        className="chart-container-50",
                                        children=[
                                            html.H3("🎯 Katègi Pwodwi", className="chart-title"),
                                            dcc.Graph(
                                                id="category-chart",
                                                className="chart-glassmorphism",
                                                figure=create_category_chart()
                                            )
                                        ]
                                    ),
                                ]
                            ),

                            # Charts Row 2
                            html.Div(
                                className="charts-row",
                                children=[
                                    html.Div(
                                        className="chart-container-50",
                                        children=[
                                            html.H3("🏆 Top 5 Pwodwi", className="chart-title"),
                                            dcc.Graph(
                                                id="top-products-chart",
                                                className="chart-glassmorphism",
                                                figure=create_top_products_chart(products_data)
                                            )
                                        ]
                                    ),
                                    html.Div(
                                        className="chart-container-50",
                                        children=[
                                            html.H3("🌍 Distribisyon Kliyan", className="chart-title"),
                                            dcc.Graph(
                                                id="location-chart",
                                                className="chart-glassmorphism",
                                                figure=create_location_chart(orders_data)
                                            )
                                        ]
                                    ),
                                ]
                            ),

                            # Recent Orders Table
                            html.Div(
                                className="table-container",
                                children=[
                                    html.H3("📋 KÒMAND RESAN", className="chart-title"),
                                    html.Table(
                                        className="data-table",
                                        children=[
                                            html.Thead(
                                                html.Tr([
                                                    html.Th("ID Kòmand"),
                                                    html.Th("Kliyèn"),
                                                    html.Th("Montan"),
                                                    html.Th("Dat"),
                                                    html.Th("Estati"),
                                                ])
                                            ),
                                            html.Tbody(
                                                [
                                                    html.Tr([
                                                        html.Td(str(row['id'])[:8]),
                                                        html.Td(row.get('user_name', 'N/A')),
                                                        html.Td(f"${float(row.get('total_amount', 0)):,.2f}"),
                                                        html.Td(str(row.get('created_at', 'N/A'))[:10]),
                                                        html.Td(
                                                            html.Span(
                                                                "✅ Konplè",
                                                                className="status-complete"
                                                            ) if str(row.get('status', 'pending')).lower() == 'completed' else
                                                            html.Span(
                                                                "⏳ Pwosès",
                                                                className="status-pending"
                                                            )
                                                        ),
                                                    ])
                                                    for _, row in orders_data.head(8).iterrows()
                                                ]
                                            )
                                        ]
                                    )
                                ]
                            ),
                        ]
                    ),
                ]
            ),

            # Footer
            html.Div(
                className="footer-glassmorphism",
                children=[
                    html.P(
                        "© 2026 LOKALMACHE | Dysèn: Glassmorphism Style | Tout Dwa Rezève ✨",
                        className="footer-text"
                    )
                ]
            ),

            dcc.Interval(id="interval-component", interval=30000, n_intervals=0)  # Rafréchi chak 30 sekondi
        ]
    )

app.layout = get_app_layout()

# ============================================================
# CALLBACKS - AUTO UPDATE KI DETEKTE NOUVO VANT
# ============================================================

@callback(
    [Output('sales-chart', 'figure'),
     Output('category-chart', 'figure'),
     Output('top-products-chart', 'figure'),
     Output('location-chart', 'figure'),
     Output('status-cards-container', 'children'),
     Output('order-status-chart', 'figure')],
    Input('interval-component', 'n_intervals')
)
def update_charts_realtime(n):
    """Rafréchi tout graf yo chak fwa interval fire - detekte nouvo vant reyel"""
    # Recharge done soti nan BD
    new_orders = db.get_orders(limit=100)
    new_products = db.get_products(limit=100)
    new_customers = db.get_customers(limit=100)
    
    # Get order status data
    status_summary = OrderStatusManager.get_status_summary()
    status_cards = [
        create_order_status_card(
            status_info['label'],
            status_info['count'],
            status_info['color'],
            status_key
        )
        for status_key, status_info in status_summary.items()
    ]
    
    # Create order status chart
    chart_data = OrderStatusManager.get_order_status_chart_data()
    status_chart = {
        'data': [
            go.Pie(
                labels=chart_data['labels'],
                values=chart_data['values'],
                marker=dict(colors=chart_data['colors']),
                hovertemplate='<b>%{label}</b><br>Kòmand: %{value}<extra></extra>',
            )
        ],
        'layout': go.Layout(
            margin=dict(l=40, r=40, t=20, b=40),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Segoe UI, sans-serif", color='rgba(200, 200, 200, 0.9)'),
            hovermode='closest',
            showlegend=True,
        )
    }
    
    # Retounen graf yo avèk done ki nouvo
    return (
        create_sales_chart(new_orders),
        create_category_chart(),
        create_top_products_chart(new_products),
        create_location_chart(new_orders),
        status_cards,
        status_chart
    )

@callback(
    [Output('btn-dashboard', 'n_clicks'),],
    Input('interval-component', 'n_intervals'),
    prevent_initial_call=True
)
def refresh_metrics(n):
    """Rafréshi metrik yo - total vann, kliyan, pwodwi"""
    return [0]

# ===============================
# CALLBACK: UPDATE ORDER STATUS
# ===============================
@callback(
    Output('update-status-message', 'children'),
    Input('update-status-btn', 'n_clicks'),
    [dash.dependencies.State('order-select-dropdown', 'value'),
     dash.dependencies.State('status-select-dropdown', 'value')],
    prevent_initial_call=True
)
def update_order_status_callback(n_clicks, order_id, new_status):
    """Modifye estati kòmand an reyèl"""
    if not n_clicks or not order_id or not new_status:
        return ""
    
    try:
        # Call the database update directly
        result = db.update_order_status(order_id, new_status)
        if result:
            status_label = OrderStatusManager.STATUSES.get(new_status, {}).get('label', new_status)
            return f"✅ Estati kòmand {str(order_id)[:8]} mete ajou: {status_label}"
        else:
            return f"❌ Echèk mete ajou estati"
    except Exception as e:
        return f"❌ Erè: {str(e)}"

if __name__ == '__main__':
    print("🚀 Senjivis Komès 2026 ap demaré...")
    print("📊 Vizite: http://localhost:8051")
    app.run_server(debug=True, host='0.0.0.0', port=8051)

# Expose server for Gunicorn production deployment
server = app.server

