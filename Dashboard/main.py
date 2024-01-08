import dash
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import psycopg2
from dash import dcc, html
from dash.dependencies import Input, Output

# Configuration de la connexion à la base de données PostgreSQL
db_config = {
    'host': 'localhost',
    'database': 'ecom_db',
    'user': 'postgres',
    'password': 'mohamed',
}


# Fonction pour récupérer les données de la table sales_per_category
def fetch_sales_per_category():
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM sales_per_category;")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data


# Fonction pour récupérer les données de la table sales_per_day
def fetch_sales_per_day():
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM sales_per_day;")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data


# Fonction pour récupérer les données de la table sales_per_month
def fetch_sales_per_month():
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM sales_per_month;")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data


# Fonction pour récupérer les données de la table transactions
def fetch_order():
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM transactions;')
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data


def fetch_sales_per_currency():
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT currency, COUNT(order_id) FROM transactions GROUP BY currency;")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data


def fetch_sales_per_payment_method():
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT payment_method, COUNT(*) FROM transactions GROUP BY payment_method;")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data


def fetch_total_sales_per_year():
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT year, SUM(total_sales) FROM sales_per_month GROUP BY year;")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data


# Fonction pour récupérer le nombre total de transactions
def fetch_total_transactions():
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(order_id) FROM transactions;")
    data = cursor.fetchone()
    cursor.close()
    connection.close()
    return data[0]  # Retourne le nombre total de transactions


# Fonction pour récupérer le montant total pour chaque devise
def fetch_total_amount_per_currency():
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT currency, SUM(total_amount) FROM transactions GROUP BY currency;")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data


# Initialisation de l'application Dash
app = dash.Dash(__name__)

# Mise en page de l'application
app.layout = html.Div([
    html.Link(rel='stylesheet', href='/assets/style.css'),
    html.Nav([
        html.Div([
            html.A('Sales Dashboard', href='#', className='brand-logo'),
            html.Ul([
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
        ], className='card-container'),
        html.Div([
            dcc.Graph(id='pie-currency', className='graph-item'),
            dcc.Graph(id='pie-payment-method', className='graph-item'),
            dcc.Graph(id='pie-total-sales-per-year', className='graph-item'),
        ], className='graph-container'),
        dcc.Graph(id='bar-graph'),
        dcc.Graph(id='line-graph'),
        dcc.Graph(id='stacked-bar-graph'),
        dcc.Interval(
            id='interval-component',
            interval=3 * 1000,  # en millisecondes
            n_intervals=0
        ),
    ], className='main-container'),
])


# Callback pour actualiser le contenu de la carte du nombre total de transactions
@app.callback(
    [Output('total-transactions', 'children'),
     Output({'type': 'card', 'currency': 'total-amount-per-currency'}, 'children')],
    [Input('interval-component', 'n_intervals')]
)
def update_cards(n):
    # Récupérer le nombre total de transactions depuis la base de données à chaque intervalle
    total_transactions = fetch_total_transactions()
    # Récupérer le montant total pour chaque devise depuis la base de données à chaque intervalle
    df_total_amount_per_currency = pd.DataFrame(fetch_total_amount_per_currency(), columns=['currency', 'totalAmount'])

    # Mettre à jour le contenu de la carte avec le nombre total de transactions
    total_transactions = html.Div(html.Div([
        html.H1(f'{total_transactions}', className='number-card-number'),
        html.Div('transactions', className='number-card-dollars'),
        html.Div(className='number-card-divider'),
    ], className='number-card number-card-content-1'),
        className='basic-column w-col w-col-3')

    # Créer dynamiquement les divs pour chaque devise

    cards_total_amount_per_currency = []
    for index, row in df_total_amount_per_currency.iterrows():
        currency_card = html.Div([
            html.H1(f'{row["totalAmount"]}', className='number-card-number'),
            html.Div(f'{row["currency"]}', className='number-card-dollars'),
            html.Div(className='number-card-divider'),
        ], className=f'number-card number-card-content{index + 2}')
        cards_total_amount_per_currency.append(html.Div(currency_card, className='basic-column w-col w-col-3'))
    return total_transactions, cards_total_amount_per_currency


# Callbacks pour actualiser les graphiques à intervalles réguliers
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
    # Récupérer de nouvelles données depuis la base de données à chaque intervalle
    df_sales_per_category = pd.DataFrame(fetch_sales_per_category(), columns=['orderDate', 'category', 'totalSales'])
    df_sales_per_day = pd.DataFrame(fetch_sales_per_day(), columns=['orderDate', 'totalSales'])
    df_sales_per_month = pd.DataFrame(fetch_sales_per_month(), columns=['year', 'month', 'totalSales'])
    df_sales_per_currency = pd.DataFrame(fetch_sales_per_currency(), columns=['currency', 'totalSales'])
    df_sales_per_payment_method = pd.DataFrame(fetch_sales_per_payment_method(),
                                               columns=['paymentMethod', 'totalCount'])
    df_total_sales_per_year = pd.DataFrame(fetch_total_sales_per_year(), columns=['year', 'totalSales'])

    # Customizing the charts based on your specific needs
    fig_bar = px.bar(df_sales_per_category, x='category', y='totalSales', color='category',
                     labels={'totalSales': 'Total des ventes', 'category': 'Catégorie'},
                     title='Ventes par catégorie')

    fig_line = px.line(df_sales_per_day, x='orderDate', y='totalSales',
                       labels={'totalSales': 'Total des ventes', 'orderDate': 'Date'},
                       title='Ventes par jour')

    # Créez le graphique à barres empilées avec les mois sur l'axe x
    fig_stacked_bar = px.bar(df_sales_per_month, x='month', y='totalSales', color='year',
                             labels={'totalSales': 'Total des ventes', 'month': 'Mois', 'year': 'Année'},
                             title='Ventes par mois')

    fig_pie_currency = go.Figure(
        data=[go.Pie(labels=df_sales_per_currency['currency'], values=df_sales_per_currency['totalSales'])])
    fig_pie_currency.update_layout(title='Ventes par devise')

    fig_pie_payment_method = go.Figure(data=[
        go.Pie(labels=df_sales_per_payment_method['paymentMethod'], values=df_sales_per_payment_method['totalCount'])])
    fig_pie_payment_method.update_layout(title='Ventes par méthode de paiement')

    fig_total_sales_per_year = px.bar(df_total_sales_per_year, x='year', y='totalSales',
                                      labels={'totalSales': 'Total des ventes', 'year': 'Année'},
                                      title='Total de ventes par année')

    # Changer les palettes de couleurs
    palette_currency = ['#19d3f3', '#e15ca6', 'darkorange', 'lightgreen', 'lightskyblue']
    palette_payment_method = ['orange', '#00cc96', '#19d3f3', 'dodgerblue', 'tomato', 'darkcyan']
    palette_total_sales_per_year = ['#FF5733', '#33FF57', '#5733FF', '#33A2FF', '#FF33A2']

    # Appliquer les palettes aux graphiques
    fig_pie_currency.update_traces(marker=dict(colors=palette_currency))
    fig_pie_payment_method.update_traces(marker=dict(colors=palette_payment_method))
    fig_total_sales_per_year.update_traces(marker=dict(color=palette_total_sales_per_year))

    return fig_bar, fig_line, fig_stacked_bar, fig_pie_currency, fig_pie_payment_method, fig_total_sales_per_year


# Exécution de l'application Dash
if __name__ == '__main__':
    app.run_server(debug=True)
