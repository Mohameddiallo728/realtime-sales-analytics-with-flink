import dash
from dash.dependencies import Input, Output

from callbacks import *
from model import *
from view import layout

# Initialisation de l'application Dash avec suppress_callback_exceptions=True
app = dash.Dash(__name__, suppress_callback_exceptions=True)


# Mise en page de l'application
app.layout = layout


# Callbacks
@app.callback(
    [Output('total-transactions', 'children'),
     Output({'type': 'card', 'currency': 'total-amount-per-currency'}, 'children')],
    [Input('interval-component', 'n_intervals')]
)
def update_cards(n):
    return update_cards_callback(n, fetch_total_transactions, fetch_total_amount_per_currency)


@app.callback(
    [Output('bar-graph', 'figure'),
     Output('line-graph', 'figure'),
     Output('stacked-bar-graph', 'figure'),
     Output('pie-currency', 'figure'),
     Output('pie-payment-method', 'figure'),
     Output('pie-total-sales-per-year', 'figure')],
    [Input('interval-component', 'n_intervals')]
)
def update_graphs(n):
    return update_graphs_callback(n, fetch_sales_per_category, fetch_sales_per_day, fetch_sales_per_month,
                                  fetch_sales_per_currency, fetch_sales_per_payment_method,
                                  fetch_total_sales_per_year)


@app.callback(
    Output('table-sales-per-category', 'data'),
    [Input('pagination-sales-per-category', 'page_current'),
     Input('pagination-sales-per-category', 'page_size')]
)
def update_sales_per_category_table(page, size):
    return update_tables_callback(fetch_sales_per_category, page, size, columns_category)


# Callback pour la table sales_per_day
@app.callback(
    Output('table-sales-per-day', 'data'),
    [Input('pagination-sales-per-day', 'page_current'),
     Input('pagination-sales-per-day', 'page_size')]
)
def update_sales_per_day_table(page, size):
    return update_tables_callback(fetch_sales_per_day, page, size, columns_day)


# Callback pour la table sales_per_month
@app.callback(
    Output('table-sales-per-month', 'data'),
    [Input('pagination-sales-per-month', 'page_current'),
     Input('pagination-sales-per-month', 'page_size')]
)
def update_sales_per_month_table(page, size):
    return update_tables_callback(fetch_sales_per_month, page, size, columns_month)


# Exécution de l'application Dash
if __name__ == '__main__':
    app.run_server(debug=True)
