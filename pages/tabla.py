import dash
from dash import html, dcc, dash_table, Input, Output, callback
import pandas as pd
import dash_bootstrap_components as dbc

# Registrar la página
dash.register_page(__name__, path="/tabla", name="📋 Tabla")

# Cargar NUEVOS datos desde archivo Excel
df = pd.read_excel("data/Simulacion_NHPP_Franja_Turno.xlsx", parse_dates=["Fecha"])

# Layout de la página
layout = dbc.Container([
    html.H2("📋 Tabla de Procesos Filtrables", className="mt-4"),
    html.P("Filtra los procesos por fecha. Si no seleccionas un rango, verás todos los datos."),
    
    dbc.Row([
        dbc.Col([
            dcc.DatePickerRange(
                id='date-picker-range',
                min_date_allowed=df['Fecha'].min(),
                max_date_allowed=df['Fecha'].max(),
                display_format='YYYY-MM-DD',
                start_date_placeholder_text="Fecha Inicio",
                end_date_placeholder_text="Fecha Fin"
            )
        ], width=12, md=8, lg=6),
    ], className="mb-3"),

    dash_table.DataTable(
        id='tabla-procesos',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        page_size=15,
        style_table={'overflowX': 'auto'},
        style_data={'whiteSpace': 'normal', 'height': 'auto'},
        style_header={
            'backgroundColor': '#007BFF', 
            'color': 'white', 
            'fontWeight': 'bold'
        },
        style_cell={'textAlign': 'center', 'padding': '10px'},
        sort_action="native",
        filter_action="native",
    ),

    html.Div(id='tabla-total', className="mt-4 alert alert-info")
], fluid=True)

@callback(
    Output("tabla-procesos", "data"),
    Output("tabla-total", "children"),
    Input("date-picker-range", "start_date"),
    Input("date-picker-range", "end_date")
)
def actualizar_tabla(start_date, end_date):
    df_filtrado = df.copy()

    if start_date and end_date:
        df_filtrado = df[
            (df["Fecha"] >= pd.to_datetime(start_date)) &
            (df["Fecha"] <= pd.to_datetime(end_date))
        ]

    # Calcular totales (solo columnas numéricas)
    totales = df_filtrado.select_dtypes(include='number').sum()

    total_html = html.Div([
        html.H5("Totales del Rango Seleccionado:", style={'color': '#0c5460'}),
        html.Ul([
            html.Li(f"{col}: {valor:,.2f}") for col, valor in totales.items()
        ], style={'listStyleType': 'none', 'paddingLeft': 0})
    ])

    return df_filtrado.to_dict("records"), total_html