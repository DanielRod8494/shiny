import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import json

# Cargar la base de datos
# Asegúrate de reemplazar 'ruta_a_tu_base.csv' con la ruta real a tu archivo
df = pd.read_csv('/Users/danielrodriguez/Desktop/PROGRA/Investigacion_CD/sa_shiny.csv')

est_osig = pd.read_csv('/Users/danielrodriguez/Desktop/PROGRA/Investigacion_CD/bases_shiny/t_osig_ent_p1.csv')

p1 = pd.read_csv('/Users/danielrodriguez/Desktop/PROGRA/Investigacion_CD/bases_shiny/i_osig_gen.csv')

entidades_mexico = est_osig['Estado'].unique()
subgrupos = est_osig['OSIG'].unique()

nacional = est_osig[est_osig['Estado']=='Nacional']

with open('/Users/danielrodriguez/Desktop/PROGRA/Investigacion_CD/mexicoHigh.json', 'r') as geojson_file:
    mexico_geojson = json.load(geojson_file)

# Calcular las métricas necesarias
#df['ISR_per_capita'] = df['ISR'] / df['n_personas']
#df['IVA_per_capita'] = df['IVA'] / df['n_personas']
#df['Total_per_capita'] = df['Total aportacion'] / df['n_personas']

# Inicializar la app con un tema de Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

# Layout de la app
app.layout = dbc.Container([
    # Barra de navegación
    dbc.NavbarSimple(
        brand="Análisis de Aportaciones Fiscales",
        color="primary",
        dark=True,
    ),
    html.Br(),
    # Indicadores clave de rendimiento (KPIs)
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Total de impuestos recaudados", className="card-title"),
                    html.H2(id='total-impuestos', className="card-text")
                ])
            ], color="info", inverse=True)
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Promedio de aportación per cápita", className="card-title"),
                    html.H2(id='promedio-aportacion', className="card-text")
                ])
            ], color="success", inverse=True)
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Número de contribuyentes", className="card-title"),
                    html.H2(id='numero-contribuyentes', className="card-text")
                ])
            ], color="warning", inverse=True)
        ], width=4),
    ]),
    html.Br(),
    dbc.Tabs([
        # Pestaña 1: Gráfica de barras
        dbc.Tab(label='Aportación per cápita', children=[
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Selecciona el impuesto:"),
                    dbc.Checklist(
                        id='tax-checklist-bar',
                        options=[
                            {'label': 'ISR', 'value': 'ISR_per_capita'},
                            {'label': 'IVA', 'value': 'IVA_per_capita'},
                            {'label': 'Total', 'value': 'aportacion_total_per_capita'}
                        ],
                        value=['aportacion_total_per_capita'],
                        labelStyle={'display': 'inline-block'}
                    ),
            ], width=6),
                dbc.Col([
                    dbc.Label("Selecciona comunidad:"),
                    dcc.Dropdown(
                        id='subgrupo-dropdown-bar',
                        options=[{'label': subgrupo, 'value': subgrupo} for subgrupo in p1['OSIG'].unique()],
                        value=list(p1['OSIG'].unique()),
                        multi=True
                    ),
                ], width=6)
            ]),
            html.Br(),
            dcc.Graph(id='bar-chart')
        ]),
        # Pestaña del gráfico de pastel (Pie Chart)
        dbc.Tab(label='Aportación total por comunidad', children=[
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Selecciona la entidad federativa o 'Nacional':"),
                    dcc.Dropdown(
                        id='entidad-dropdown',
                        options=[{'label': entidad, 'value': entidad} for entidad in entidades_mexico],
                        value='Nacional',  # Valor por defecto
                        placeholder="Selecciona una entidad"
                    )
                ], width=6),
            ]),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Selecciona el impuesto:"),
                    dbc.Checklist(
                        id='tax-checklist-pie',
                        options=[
                            {'label': 'ISR', 'value': 'ISR'},
                            {'label': 'IVA', 'value': 'IVA'},
                            {'label': 'Total', 'value': 'Total aportacion'}
                        ],
                        value=['Total aportacion'],
                        inline=True
                    )
                ], width=6),
                dbc.Col([
                    dbc.Label("Selecciona la comunidad:"),
                    dcc.Dropdown(
                        id='subgrupo-dropdown-pie',
                        options=[{'label': subgrupo, 'value': subgrupo} for subgrupo in subgrupos],
                        value=subgrupos.tolist(),
                        multi=True
                    )
                ], width=6),
            ]),
            html.Br(),
            dcc.Graph(id='pie-chart'),
            html.Br(),
            html.Div(id='total-values', style={'font-size': '25px', 'font-weight': 'bold', 'text-align': 'center'})
        ]),
        # Pestaña 3: Tabla interactiva
        dbc.Tab(label='Tabla de aportaciones detallada', children=[
            html.Br(),
            html.Label("Selecciona la comunidad:"),
            dcc.Dropdown(
                id='subgrupo-dropdown-table',
                options=[{'label': subgrupo, 'value': subgrupo} for subgrupo in est_osig['OSIG'].unique()],
                value=list(est_osig['OSIG'].unique()),
                multi=True
            ),
            html.Br(),
            dash_table.DataTable(
                id='data-table',
                columns=[
                    {'name': 'Entidad', 'id': 'Estado'},
                    {'name': 'Subgrupo', 'id': 'OSIG'},
                    {'name': 'Ingreso Laboral', 'id': 'ingreso_laboral', 'type': 'numeric'},
                    {'name': 'Consumo', 'id': 'consumo', 'type': 'numeric'},
                    {'name': 'ISR', 'id': 'ISR', 'type': 'numeric'},
                    {'name': 'IVA', 'id': 'IVA', 'type': 'numeric'},
                    {'name': 'Aportación Total', 'id': 'Total aportacion', 'type': 'numeric'}
                ],
                data=[],  # Se actualizará con el callback
                filter_action='native',
                sort_action='native',
                page_size=20,
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'left'},
            )
        ]),
         # Pestaña 4: Histograma
        dbc.Tab(label='Distribución de aportaciones', children=[
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Selecciona el impuesto:"),
                    dbc.Checklist(
                        id='tax-checklist-histogram',
                        options=[
                            {'label': 'ISR', 'value': 'ISR'},
                            {'label': 'IVA', 'value': 'IVA'},
                            {'label': 'Total', 'value': 'Total aportacion'}
                        ],
                        value=['ISR'],
                        labelStyle={'display': 'inline-block'}
                    ),
                ], width=6),
                dbc.Col([
                    dbc.Label("Selecciona la comunidad:"),
                    dcc.Dropdown(
                        id='subgrupo-dropdown-histogram',
                        options=[{'label': subgrupo, 'value': subgrupo} for subgrupo in df['OSIG'].unique()],
                        value=list(df['OSIG'].unique()),
                        multi=True
                    ),
                ], width=6)
            ]),
            html.Br(),
            dcc.Graph(id='histogram')
        ]),
        
        # Pestaña 5: Mapa de calor
        dbc.Tab(label='Mapa de calor de los Estados', children=[
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Selecciona la comunidad:"),
                    dcc.Dropdown(
                        id='comunidad-dropdown',
                        options=[{'label': subgrupo, 'value': subgrupo} for subgrupo in est_osig['OSIG'].unique()],
                        value=est_osig['OSIG'].unique()[0],  # Selecciona la primera comunidad por defecto
                        placeholder="Selecciona una comunidad"
                    )
                ], width=6),
                dbc.Col([
                    dbc.Label("Selecciona el tipo de impuesto:"),
                    dbc.RadioItems(
                        id='impuesto-radio',
                        options=[
                            {'label': 'ISR', 'value': 'ISR'},
                            {'label': 'IVA', 'value': 'IVA'},
                            {'label': 'Total', 'value': 'Total aportacion'}
                        ],
                        value='Total aportacion',  # Valor por defecto
                        inline=True
                    )
                ], width=6),
            ]),
            html.Br(),
            dcc.Graph(id='mapa-calor')
        ])
    ])
])

# Callbacks para actualizar las gráficas y tablas se mantienen similares
@app.callback(
    [Output('total-impuestos', 'children'),
     Output('promedio-aportacion', 'children'),
     Output('numero-contribuyentes', 'children')],
    [Input('subgrupo-dropdown-bar', 'value')]
)

def update_kpis(selected_subgrupos):
    if not selected_subgrupos:
        return "N/A", "N/A", "N/A"
    
    # Filtrar por los subgrupos seleccionados
    filtered_df = nacional[nacional['OSIG'].isin(selected_subgrupos)].copy()
    
    # Calcular Total de nuevo si no está predefinido
    filtered_df['Total'] = filtered_df['ISR'] + filtered_df['IVA']
    
    # Calcular métricas
    total_impuestos = (filtered_df['Total aportacion'].sum())/1000000
    promedio_aportacion = filtered_df['Total aportacion'].sum()/filtered_df['n_personas'].sum()
    numero_contribuyentes = filtered_df['n_personas'].sum()

    return f"${total_impuestos:,.2f} M", f"${promedio_aportacion:,.2f}", f"{numero_contribuyentes:,.0f}"

@app.callback(
    Output('bar-chart', 'figure'),
    [Input('tax-checklist-bar', 'value'),
     Input('subgrupo-dropdown-bar', 'value')]
)

def update_bar_chart(selected_taxes, selected_subgrupos):
    if not selected_taxes or not selected_subgrupos:
        return {}
    filtered_p1 = p1[p1['OSIG'].isin(selected_subgrupos)].copy()
    filtered_p1['ISR'] = filtered_p1['ISR_per_capita']
    filtered_p1['IVA'] = filtered_p1['IVA_per_capita']
    filtered_p1['Total'] = filtered_p1['aportacion_total_per_capita']
    # Promedio por subgrupo
    avg_df = filtered_p1.groupby('OSIG')[selected_taxes].mean().reset_index()
    # Crear gráfica de barras
    fig = px.bar(
        avg_df,
        x='OSIG',
        y=selected_taxes,
        barmode='group',
        title='<b>Aportación per cápita promedio por comunidad<b>',
        text_auto='.2f'
    )
    return fig

@app.callback(
    [
    Output('pie-chart', 'figure'), # Actualizar el gráfico de pastel
    Output('total-values', 'children')  # Totales de aportación
    ],
    [
        Input('entidad-dropdown', 'value'),    # Entidad seleccionada
        Input('tax-checklist-pie', 'value'),  # Impuestos seleccionados
        Input('subgrupo-dropdown-pie', 'value')  # Subgrupos seleccionados
    ]
)
def update_pie_chart(entidad, selected_taxes, selected_subgrupos):
    # Filtrar datos por subgrupos seleccionados
    filtered_df = est_osig[est_osig['OSIG'].isin(selected_subgrupos)].copy()  # Cambia 'OSIG' según tu columna de subgrupos

    # Filtrar por entidad (incluyendo Nacional si se selecciona)
    if entidad:  # Si se selecciona una entidad (incluyendo 'Nacional')
        filtered_df = filtered_df[filtered_df['Estado'] == entidad]  # Cambia 'entidad' según tu columna

    # Sumar valores por subgrupo
    total_df = filtered_df.groupby('OSIG')[selected_taxes].sum().reset_index()  # Cambia 'OSIG' según tu columna
    # Calcular totales por cada impuesto seleccionado
    totals = filtered_df[selected_taxes].sum()

    # Crear texto para los totales
    totals_text = [
        html.Div(f"{tax}: ${totals[tax]:,.2f}", style={'margin-bottom': '100px'}) for tax in selected_taxes
    ]
    totals_text.insert(0, html.Div(f"Aportación total para {entidad}:"))
    
    # Crear gráfico de pastel
    fig = px.pie(
        total_df,
        names='OSIG',  # Cambia 'OSIG' según tu columna de subgrupos
        values=selected_taxes[0],  # Usar el primer impuesto seleccionado
        title=f"<b>Aportación total por comunidad<br>en {entidad}<b>",
        hole=0.4  # Para crear un gráfico de dona
    )

    return fig,totals_text

@app.callback(
    Output('data-table', 'data'),
    [Input('subgrupo-dropdown-table', 'value')]
)
def update_table(selected_subgrupos):
    if not selected_subgrupos:
        return []
    filtered_estado = est_osig[est_osig['OSIG'].isin(selected_subgrupos)].copy()
    filtered_estado['ISR'] = filtered_estado['ISR']
    filtered_estado['IVA'] = filtered_estado['IVA']
    filtered_estado['Total'] = filtered_estado['Total aportacion']
    return filtered_estado.to_dict('records')

@app.callback(
    Output('histogram', 'figure'),
    [Input('tax-checklist-histogram', 'value'),
     Input('subgrupo-dropdown-histogram', 'value')]
)

def update_histogram(selected_taxes, selected_subgrupos):
    if not selected_taxes or not selected_subgrupos:
        return {}
    filtered_df = df[df['OSIG'].isin(selected_subgrupos)].copy()
    filtered_df['ISR'] = filtered_df['ISR']
    filtered_df['IVA'] = filtered_df['IVA']
    filtered_df['Total'] = filtered_df['Total aportacion']
    # Crear histograma
    fig = px.histogram(
        filtered_df,
        x=selected_taxes[0],
        nbins=30,
        title='Distribución de aportaciones',
        color='OSIG'
    )
    return fig

@app.callback(
    Output('mapa-calor', 'figure'),  # Actualizar el mapa
    [
        Input('comunidad-dropdown', 'value'),  # Comunidad seleccionada
        Input('impuesto-radio', 'value')      # Tipo de impuesto seleccionado
    ]
)
def update_heatmap(comunidad, impuesto):
    # Filtrar datos por la comunidad seleccionada
    filtered_df = est_osig[est_osig['OSIG'] == comunidad]

    # Calcular aportación per cápita por entidad
    aportacion_per_capita = (
        filtered_df.groupby('Estado')[impuesto].sum() / filtered_df.groupby('Estado')['n_personas'].sum()
    ).reset_index()

    aportacion_per_capita.columns = ['entidad', 'aporte_per_capita']

    # Crear el mapa de calor
    fig = px.choropleth(
        aportacion_per_capita,
        geojson=mexico_geojson,  # GeoJSON de las entidades federativas
        locations='entidad',    # Columna de las entidades en el DataFrame
        featureidkey='properties.name',  # Llave en el GeoJSON que coincide con los nombres de las entidades
        color='aporte_per_capita',
        color_continuous_scale='RdBu_r',
        title=f"<b>Aportación per cápita para {comunidad} ({impuesto})<b>",
        labels={'aporte_per_capita': 'Aportación per cápita'}
    )

    # Ajustar los límites del mapa
    fig.update_geos(
        visible=False,
        fitbounds="locations"  # Ajustar a los datos
    )

    return fig

# Ejecutar la app
if __name__ == '__main__':
    app.run_server(debug=True)