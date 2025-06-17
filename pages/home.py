import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/")

layout = html.Div([
    html.Div([
        html.Img(src="/assets/logo.png", style={
            "height": "180px", 
            "display": "block", 
            "margin": "40px auto 20px auto"
        }),
        
        html.P(
            "Visualiza la carga operativa por turno y tipo de transacción usando un modelo estadístico NHPP.",
            style={"textAlign": "center", "fontSize": "20px", "maxWidth": "700px", "margin": "0 auto"}
        ),

        html.Div([
            dbc.Button("📈 Evolución Temporal", href="/temporal", color="primary", className="me-2", size="lg"),
            dbc.Button("📊 Barras por Turno", href="/barras", color="success", className="me-2", size="lg"),
            dbc.Button("📈 Acumulado Diario", href="/acumulado", color="warning", className="me-2", size="lg"),
            dbc.Button("🔥 Ver Heatmap", href="/heatmap", color="danger", className="me-2", size="lg"),
            dbc.Button("📋 Ver Tabla", href="/tabla", color="info", size="lg")
        ], style={"textAlign": "center", "marginTop": "40px"})
    ])
])
