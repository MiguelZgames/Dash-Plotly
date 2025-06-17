import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

# Inicializar la app con soporte para múltiples páginas y assets
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP], assets_folder='assets')
app.title = "NHPP Dashboard"

# Layout principal con navegación mejorada
app.layout = html.Div([
    # Barra de navegación con logo y links a todas las páginas
    dbc.NavbarSimple(
        brand=html.Div([
            html.Img(src=app.get_asset_url("logo.png"), height="35px", style={"verticalAlign": "middle"}),
            html.Span(" NHPP Dashboard", style={"verticalAlign": "middle", "marginLeft": "10px", "color": "white"})
        ]),
        brand_href="/",
        color="primary",
        dark=True,
        children=[
            dbc.NavItem(dcc.Link("Inicio", href="/", className="nav-link")),
            dbc.NavItem(dcc.Link("📈 Temporal", href="/temporal", className="nav-link")),
            dbc.NavItem(dcc.Link("📈 Acumulado", href="/acumulado", className="nav-link")),
            dbc.NavItem(dcc.Link("📊 Barras", href="/barras", className="nav-link")),
            dbc.NavItem(dcc.Link("🔥 Heatmap", href="/heatmap", className="nav-link")),
            dbc.NavItem(dcc.Link("📋 Tabla", href="/tabla", className="nav-link")),
            dbc.NavItem(dcc.Link("📄 Reportes", href="/reportes", className="nav-link")), # NUEVO
        ]
    ),

    # Contenedor de páginas dinámicas
    html.Div(dash.page_container, style={"padding": "20px"})
])

# Ejecutar la app
if __name__ == "__main__":
    # El host='0.0.0.0' hace que la app sea visible en tu red local.
    # El puerto 8050 es el predeterminado, puedes cambiarlo si lo necesitas.
    app.run(host='0.0.0.0', port=8050, debug=True)

    # Para producción, necesitaremos acceder a esta variable `server`
server = app.server
