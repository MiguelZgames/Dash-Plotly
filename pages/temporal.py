import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

# Registrar página
dash.register_page(__name__, path="/temporal")

# Cargar datos
df = pd.read_excel("data/Simulacion_NHPP_Franja_Turno.xlsx", parse_dates=["Fecha"])
available_franjas = sorted(df['Franja Turno'].unique())

# --- Layout Mejorado con Filtro Interactivo ---
layout = dbc.Container([
    dbc.Row(
        dbc.Col(
            dbc.Card([
                dbc.CardHeader(html.H4("📈 Evolución Diaria por Franja Horaria")),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Label("Seleccionar Franjas Horarias a Comparar:"),
                            dcc.Dropdown(
                                id='franja-selector-dropdown',
                                options=[{'label': franja, 'value': franja} for franja in available_franjas],
                                value=['Turno A', 'Turno D'], 
                                multi=True,
                                placeholder="Seleccione una o más franjas..."
                            )
                        ], width=12)
                    ], className="mb-4"),

                    # Contenedor del gráfico
                    html.Div(
                        # --- PUNTO 1: DEFINICIÓN DEL ID ---
                        # Aquí, el ID del componente del gráfico se define como "fig-temporal-filtrado"
                        dcc.Graph(id="fig-temporal-filtrado"), # <-- ID DEFINITION
                        className="border rounded"
                    )
                ])
            ]),
            width=12
        ),
        className="mt-4"
    )
], fluid=True)


# --- Callback con la CORRECCIÓN ---
@dash.callback(
    # --- PUNTO 2: USO DEL ID ---
    # El Output AHORA apunta al ID correcto "fig-temporal-filtrado", que coincide con el del layout.
    Output("fig-temporal-filtrado", "figure"), # <-- ID USAGE (CORRECTED)
    Input("franja-selector-dropdown", "value")
)
def actualizar_evolucion_filtrada(selected_franjas):
    if not selected_franjas:
        fig = go.Figure()
        fig.update_layout(
            template="plotly_white",
            annotations=[dict(text="Por favor, seleccione una o más franjas horarias.", showarrow=False)],
            xaxis=dict(visible=False), yaxis=dict(visible=False)
        )
        return fig

    dff = df[df['Franja Turno'].isin(selected_franjas)]
    fig = go.Figure()

    for franja in selected_franjas:
        datos_franja = dff[dff['Franja Turno'] == franja].sort_values("Fecha")
        fig.add_trace(go.Scatter(
            x=datos_franja['Fecha'], y=datos_franja['P95'],
            mode='lines', line=dict(width=0), showlegend=False, hoverinfo='none'
        ))
        fig.add_trace(go.Scatter(
            x=datos_franja['Fecha'], y=datos_franja['P5'],
            mode='lines', line=dict(width=0), fill='tonexty',
            fillcolor='rgba(100, 100, 100, 0.1)', showlegend=False, hoverinfo='none'
        ))
        fig.add_trace(go.Scatter(
            x=datos_franja['Fecha'], y=datos_franja['Media'],
            mode='lines+markers', name=franja,
            marker=dict(size=5), line=dict(width=2.5)
        ))

    fig.update_layout(
        title_text="Evolución Diaria con Intervalos de Confianza (P5-P95)",
        title_x=0.5,
        yaxis_title="Promedio de Transacciones",
        xaxis_title="Fecha",
        template="plotly_white",
        legend_title_text='Franja Horaria',
        hovermode="x unified",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=60, b=20, l=20, r=20)
    )

    return fig