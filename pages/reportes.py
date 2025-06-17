import dash
from dash import html, dcc, callback, Input, Output, State
import pandas as pd
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

# Registrar la página
dash.register_page(__name__, path="/reportes", name="📄 Reportes")

# Cargar NUEVOS datos
df = pd.read_excel("data/Simulacion_NHPP_Franja_Turno.xlsx")
df["Fecha"] = pd.to_datetime(df["Fecha"])
tipos_proceso = sorted(df["Tipo"].unique())

# Layout de la página
layout = dbc.Container([
    html.H2("📄 Generador de Reportes", className="mt-4"),
    html.P("Selecciona los filtros para generar y descargar un reporte en formato CSV."),
    
    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                # Filtro de Fecha
                dbc.Col([
                    html.Label("Rango de Fechas:", className="fw-bold"),
                    dcc.DatePickerRange(
                        id='report-date-picker',
                        min_date_allowed=df['Fecha'].min().date(),
                        max_date_allowed=df['Fecha'].max().date(),
                        start_date=df['Fecha'].min().date(),
                        end_date=df['Fecha'].max().date(),
                        display_format='YYYY-MM-DD',
                        className="mt-1"
                    )
                ], width=12, md=6),
                
                # Filtro de Tipo de Proceso
                dbc.Col([
                    html.Label("Tipo de Proceso:", className="fw-bold"),
                    dcc.Dropdown(
                        id="report-tipo-dropdown",
                        options=[{"label": tipo, "value": tipo} for tipo in tipos_proceso],
                        placeholder="Seleccionar todos los tipos",
                        multi=True,
                        className="mt-1"
                    )
                ], width=12, md=6),
            ], className="mb-3"),
            
            # Botón de descarga
            dbc.Button(
                "📥 Descargar Reporte CSV", 
                id="btn-download-csv", 
                color="primary", 
                className="mt-3 w-100"
            ),
            dcc.Download(id="download-csv-data")
        ])
    )
], className="mt-4")

@callback(
    Output("download-csv-data", "data"),
    Input("btn-download-csv", "n_clicks"),
    State("report-date-picker", "start_date"),
    State("report-date-picker", "end_date"),
    State("report-tipo-dropdown", "value"),
    prevent_initial_call=True
)
def generate_csv(n_clicks, start_date, end_date, tipos_sel):
    if not n_clicks:
        raise PreventUpdate

    df_filtrado = df.copy()

    # Filtrar por fecha
    if start_date and end_date:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        df_filtrado = df_filtrado[(df_filtrado["Fecha"] >= start_date) & (df_filtrado["Fecha"] <= end_date)]

    # Filtrar por tipo
    if tipos_sel: # Si la lista no está vacía
        df_filtrado = df_filtrado[df_filtrado["Tipo"].isin(tipos_sel)]

    # Generar el archivo CSV en memoria
    return dcc.send_data_frame(df_filtrado.to_csv, "reporte_nhpp_detallado.csv", index=False)