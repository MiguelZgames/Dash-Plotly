import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc # Asegúrate de que dbc esté importado

# Registrar página
dash.register_page(__name__, path="/barras")

# --- Paleta de Colores Personalizada ---
# Define colores específicos para cada tipo de proceso para consistencia visual
color_map = {
    "Cargar Saldo": "#FF6347",      # Un rojo-tomate amigable
    "Retirar Saldo": "#4682B4",     # Un azul acero profesional
    "Cargar Bono Saldo": "#32CD32"  # Un verde lima vibrante
}

# Cargar datos
df = pd.read_excel("data/Simulacion_NHPP_Franja_Turno.xlsx", parse_dates=["Fecha"])
dates = sorted(df["Fecha"].dt.date.unique())

# --- Nuevo Layout con dbc.Card para un diseño profesional ---
layout = dbc.Container([
    dbc.Row(
        dbc.Col(
            dbc.Card([
                # Título principal en el encabezado de la tarjeta
                dbc.CardHeader(html.H4("📊 Transacciones Promedio por Franja Horaria")),
                
                dbc.CardBody([
                    # Controles (selector de fecha)
                    dbc.Row([
                        dbc.Col([
                            html.Label("Seleccionar Fecha:"),
                            dcc.Dropdown(
                                id="dropdown-fecha-barras",
                                options=[{"label": str(d), "value": str(d)} for d in dates],
                                value=str(dates[-1]),
                            )
                        ], width=12, md=6, lg=4) # Controla el ancho del dropdown
                    ], justify="center", className="mb-4"), # Centra el dropdown y añade margen inferior

                    # Contenedor para el gráfico con un borde sutil
                    html.Div(
                        dcc.Graph(id="fig-barras"),
                        className="border rounded"
                    )
                ])
            ]),
            width=12 # La tarjeta ocupa todo el ancho
        ),
        className="mt-4" # Margen superior para la fila
    )
], fluid=True)


# --- Callback con el gráfico mejorado ---
@dash.callback(
    Output("fig-barras", "figure"),
    Input("dropdown-fecha-barras", "value")
)
def actualizar_barras_apiladas(fecha_str):
    fecha_sel = pd.to_datetime(fecha_str).date()

    df_filtrado = df[df["Fecha"].dt.date == fecha_sel]
    
    if df_filtrado.empty:
        return px.bar(title=f"No hay datos para la fecha {fecha_sel}")

    # Crear el gráfico usando la paleta de colores personalizada
    fig = px.bar(
        df_filtrado,
        x="Franja Turno",
        y="Media",
        color="Tipo",
        labels={"Media": "Promedio de Transacciones", "Franja Turno": "Franja Horaria"},
        barmode="stack",
        template="plotly_white",
        category_orders={"Franja Turno": sorted(df_filtrado['Franja Turno'].unique())},
        color_discrete_map=color_map # Aplicar nuestra paleta de colores
    )

    fig.update_layout(
        # Título dinámico dentro del gráfico
        title_text=f"Detalle para la fecha: {fecha_sel}",
        title_x=0.5, # Centrar el título
        xaxis_tickangle=-45,
        legend_title_text='Tipo de Proceso',
        # Fondo transparente para integrarse con la tarjeta
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=60, b=10, l=10, r=10) # Ajustar márgenes para un look más compacto
    )
    
    # Añadir un borde sutil a las barras para mejor definición
    fig.update_traces(marker_line_width=1.5, marker_line_color='white')
    
    return fig