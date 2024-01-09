from dash import dcc, dash_table

from callbacks import *
from model import *

layout = html.Div([
    html.Link(rel='stylesheet', href='/assets/style.css'),
    html.Nav([
        html.Div([
            html.A('Sales Dashboard', href='#', className='brand-logo'),
            html.Ul([
                html.Li(html.A('Résumé en chiffres', href='#stats')),
                html.Li(html.A('Ventes par catégorie', href='#bar-graph')),
                html.Li(html.A('Ventes par jour', href='#line-graph')),
                html.Li(html.A('Ventes par mois', href='#stacked-bar-graph')),
            ], className='nav-links')
        ], className='nav-wrapper')
    ], className='navbar-fixed'),
    html.Div([
        html.Div([
            html.Div(id='total-transactions'),
            html.Div(id={'type': 'card', 'currency': 'total-amount-per-currency'}),
        ], className='card-container', id='stats'),
        html.Div([
            dcc.Graph(id='pie-currency', className='graph-item'),
            dcc.Graph(id='pie-payment-method', className='graph-item'),
            dcc.Graph(id='pie-total-sales-per-year', className='graph-item'),
        ], className='graph-container'),

        html.Div([
            html.Div([
                dash_table.DataTable(
                    id='table-sales-per-category',
                    columns=[
                        {'name': col, 'id': col} for col in columns_category
                    ],
                    page_current=0,
                    page_size=10,
                    page_action='custom',
                    sort_action='custom',
                    sort_mode='single',
                    style_as_list_view=True,
                    style_cell={'padding': '5px'},
                    style_header={
                        'backgroundColor': '#0074cc',
                        'color': 'white',
                        'fontWeight': 'bold'
                    },
                    data=update_tables_callback(fetch_sales_per_category, page_current, page_size, columns_category),
                ),
                dcc.Store(id='page-sales-per-category', data=0),
            ], className='table'),

            html.Div([
                dash_table.DataTable(
                    id='table-sales-per-day',
                    columns=[
                        {'name': col, 'id': col} for col in columns_day
                    ],
                    page_current=0,
                    page_size=10,
                    page_action='custom',
                    sort_action='custom',
                    sort_mode='single',
                    style_as_list_view=True,
                    style_cell={'padding': '5px'},
                    style_header={
                        'backgroundColor': '#0074cc',
                        'color': 'white',
                        'fontWeight': 'bold'
                    },
                    data=update_tables_callback(fetch_sales_per_day, page_current, page_size, columns_day)
                    ,
                ),
                dcc.Store(id='page-sales-per-day', data=0),
            ], className='table'),

            html.Div([
                dash_table.DataTable(
                    id='table-sales-per-month',
                    columns=[
                        {'name': col, 'id': col} for col in columns_month
                    ],
                    page_current=0,
                    page_size=10,
                    page_action='custom',
                    sort_action='custom',
                    sort_mode='single',
                    style_as_list_view=True,
                    style_cell={'padding': '5px'},
                    style_header={
                        'backgroundColor': '#0074cc',
                        'color': 'white',
                        'fontWeight': 'bold'
                    },
                    data=update_tables_callback(fetch_sales_per_month, page_current, page_size, columns_month),
                ),
                dcc.Store(id='page-sales-per-month', data=0),
            ], className='table'),

        ], className='table-container'),

        dcc.Graph(id='bar-graph'),
        dcc.Graph(id='line-graph'),
        dcc.Graph(id='stacked-bar-graph'),
        dcc.Interval(
            id='interval-component',
            interval=2 * 1000,  # en millisecondes
            n_intervals=0
        ),
    ], className='main-container'),
])
