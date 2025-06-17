# pages/acumulado.py

import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

# Registrar la nueva página con una ruta y nombre únicos
dash.register_page(
    __name__, 
    path="/acumulado", 
    name="📈 Acumulado" # Este nombre aparecerá en la barra de navegación
)

# Cargar datos
df = pd.read_excel("data/Simulacion_NHPP_Franja_Turno.xlsx", parse_dates=["Fecha"])

# --- Layout profesional con dbc.Card ---
layout = dbc.Container([
    dbc.Row(
        dbc.Col(
            dbc.Card([
                dbc.CardHeader(html.H4("📈 Evolución Acumulada de Transacciones")),
                dbc.CardBody([
                    html.P(
                        "Este gráfico muestra la suma acumulada de las transacciones estimadas a lo largo del tiempo, "
                        "desglosada por cada franja horaria.",
                        className="text-muted"
                    ),
                    html.Div(
                        dcc.Graph(id="fig-acumulado"),
                        className="border rounded mt-3"
                    )
                ])
            ]),
            width=12
        ),
        className="mt-4"
    )
], fluid=True)

# Callback para el gráfico acumulado
@dash.callback(
    Output("fig-acumulado", "figure"),
    Input("fig-acumulado", "id")
)
def mostrar_evolucion_acumulada(_):
    # Lógica para calcular los datos acumulados
    line_data = df.groupby(["Fecha", "Franja Turno"])["Media"].sum().unstack(fill_value=0).cumsum().reset_index()
    df_linea = line_data.melt(id_vars="Fecha", var_name="Franja Turno", value_name="Transacciones Acumuladas")

    # Crear el gráfico
    fig = px.line(
        df_linea,
        x="Fecha",
        y="Transacciones Acumuladas",
        color="Franja Turno",
        labels={"Transacciones Acumuladas": "Total Transacciones Acumuladas", "Fecha": "Fecha"},
        template="plotly_white"
    )

    # Aplicar mejoras visuales
    fig.update_layout(
        title_text="Crecimiento Acumulado de Transacciones por Franja",
        title_x=0.5,
        xaxis_tickangle=-45,
        legend_title_text="Franja Horaria",
        hovermode="x unified",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=60, b=20, l=20, r=20)
    )

    return fig