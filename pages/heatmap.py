import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

# Registrar página
dash.register_page(__name__, path="/heatmap")

# Cargar datos
df = pd.read_excel("data/Simulacion_NHPP_Franja_Turno.xlsx", parse_dates=["Fecha"])
available_dates = sorted(df['Fecha'].dt.date.unique())

# --- Layout Profesional con Filtro de Fecha ---
layout = dbc.Container([
    dbc.Row(
        dbc.Col(
            dbc.Card([
                dbc.CardHeader(html.H4("🔥 Distribución de Carga por Tipo y Franja Horaria")),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Label("Seleccionar Fecha:"),
                            dcc.Dropdown(
                                id='heatmap-date-dropdown',
                                options=[{'label': 'Todos los días (Agregado)', 'value': 'all'}] + 
                                        [{'label': str(d), 'value': str(d)} for d in available_dates],
                                value='all',
                                clearable=False
                            )
                        ], width=12, md=6, lg=4)
                    ], justify="center", className="mb-4"),

                    html.Div(
                        dcc.Graph(id="fig-heatmap-filtrado"),
                        className="border rounded"
                    )
                ])
            ]),
            width=12
        ),
        className="mt-4"
    )
], fluid=True)

# --- Callback con la nueva escala de color CLARA ---
@dash.callback(
    Output("fig-heatmap-filtrado", "figure"),
    Input("heatmap-date-dropdown", "value")
)
def generar_heatmap_filtrado(selected_date):
    
    if selected_date == 'all':
        dff = df.copy()
        title_date_part = "Total Agregado"
    else:
        dff = df[df['Fecha'].dt.date == pd.to_datetime(selected_date).date()]
        title_date_part = f"para la fecha {selected_date}"
        
    heatmap_data = dff.pivot_table(
        index="Franja Turno",
        columns="Tipo",
        values="Media",
        aggfunc="sum",
        fill_value=0
    )

    sorted_franjas = sorted(heatmap_data.index)
    heatmap_data = heatmap_data.reindex(sorted_franjas)

    fig = px.imshow(
        heatmap_data,
        text_auto=True, 
        aspect="auto",
        labels=dict(x="Tipo de Proceso", y="Franja Horaria", color="Carga Total"),
        # --- LÍNEA MODIFICADA ---
        color_continuous_scale='Blues' # MEJORA: Escala de color clara, suave y profesional.
    )

    fig.update_layout(
        title_text=f"Heatmap de Carga Estimada {title_date_part}",
        title_x=0.5,
        template="plotly_white",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=60, b=20, l=20, r=20)
    )
    
    return fig