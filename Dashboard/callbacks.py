import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash import html


# Fonction de rappel pour mettre à jour les cartes affichant les informations sur les transactions.
def update_cards_callback(n, fetch_total_transactions, fetch_total_amount_per_currency):
    """
    Fonction de rappel pour mettre à jour les cartes affichant les informations sur les transactions.

    Paramètres :
    - n : Nombre d'intervalles (non utilisé dans la fonction mais requis pour le rappel Dash).
    - fetch_total_transactions : Une fonction qui récupère le nombre total de transactions.
    - fetch_total_amount_per_currency : Une fonction qui récupère le montant total pour chaque devise.

    Retourne :
    - total_transactions_card : Div HTML contenant la carte des transactions totales.
    - cards_total_amount_per_currency : Liste de divs HTML, chacune représentant une carte pour une devise spécifique.
    """
    total_transactions = fetch_total_transactions()
    df_total_amount_per_currency = pd.DataFrame(fetch_total_amount_per_currency(), columns=['currency', 'totalAmount'])

    # Mettre à jour la carte des transactions totales
    total_transactions_card = html.Div(html.Div([
        html.H1(f'{total_transactions}', className='number-card-number'),
        html.Div('transactions', className='number-card-dollars'),
        html.Div(className='number-card-divider'),
    ], className='number-card number-card-content-1'), className='basic-column w-col w-col-3')

    # Mettre à jour les cartes de devise
    cards_total_amount_per_currency = []
    for index, row in df_total_amount_per_currency.iterrows():
        currency_card = html.Div([
            html.H1(f'{row["totalAmount"]}', className='number-card-number'),
            html.Div(f'{row["currency"]}', className='number-card-dollars'),
            html.Div(className='number-card-divider'),
        ], className=f'number-card number-card-content{index + 2}')
        cards_total_amount_per_currency.append(html.Div(currency_card, className='basic-column w-col w-col-3'))

    return total_transactions_card, cards_total_amount_per_currency


# Fonction de rappel pour mettre à jour divers graphiques dans l'application Dash.
def update_graphs_callback(n, fetch_sales_per_category, fetch_sales_per_day, fetch_sales_per_month,
                           fetch_sales_per_currency, fetch_sales_per_payment_method, fetch_total_sales_per_year):
    """
    Fonction de rappel pour mettre à jour divers graphiques dans l'application Dash.

    Paramètres :
    - n : Nombre d'intervalles (non utilisé dans la fonction mais requis pour le rappel Dash).
    - fetch_sales_per_category : Fonction qui récupère les données des ventes par catégorie.
    - fetch_sales_per_day : Fonction qui récupère les données de ventes quotidiennes.
    - fetch_sales_per_month : Fonction qui récupère les données de ventes mensuelles.
    - fetch_sales_per_currency : Fonction qui récupère les données de ventes par devise.
    - fetch_sales_per_payment_method : Fonction qui récupère les données de ventes par méthode de paiement.
    - fetch_total_sales_per_year : Fonction qui récupère les données de ventes totales par année.

    Retourne :
    Six figures Plotly (Diagramme à barres, Diagramme linéaire, Diagramme à barres empilées,
    Diagramme circulaire pour la devise, Diagramme circulaire pour la méthode de paiement, Diagramme à barres pour les ventes totales par année).
    """
    df_sales_per_category = pd.DataFrame(fetch_sales_per_category(), columns=['orderDate', 'category', 'totalSales'])
    df_sales_per_day = pd.DataFrame(fetch_sales_per_day(), columns=['orderDate', 'totalSales'])
    df_sales_per_month = pd.DataFrame(fetch_sales_per_month(), columns=['year', 'month', 'totalSales'])
    df_sales_per_currency = pd.DataFrame(fetch_sales_per_currency(), columns=['currency', 'totalSales'])
    df_sales_per_payment_method = pd.DataFrame(fetch_sales_per_payment_method(),
                                               columns=['paymentMethod', 'totalCount'])
    df_total_sales_per_year = pd.DataFrame(fetch_total_sales_per_year(), columns=['year', 'totalSales'])

    fig_bar = px.bar(df_sales_per_category, x='category', y='totalSales', color='category',
                     labels={'totalSales': 'Total des ventes', 'category': 'Catégorie'},
                     title='Ventes par catégorie')

    fig_line = px.line(df_sales_per_day, x='orderDate', y='totalSales',
                       labels={'totalSales': 'Total des ventes', 'orderDate': 'Date'},
                       title='Ventes par jour')

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

    palette_currency = ['#19d3f3', '#e15ca6', 'darkorange', 'lightgreen', 'lightskyblue']
    palette_payment_method = ['orange', '#00cc96', '#19d3f3', 'dodgerblue', 'tomato', 'darkcyan']
    palette_total_sales_per_year = ['#FF5733', '#33FF57', '#5733FF', '#33A2FF', '#FF33A2']

    fig_pie_currency.update_traces(marker=dict(colors=palette_currency))
    fig_pie_payment_method.update_traces(marker=dict(colors=palette_payment_method))
    fig_total_sales_per_year.update_traces(marker=dict(color=palette_total_sales_per_year))

    return fig_bar, fig_line, fig_stacked_bar, fig_pie_currency, fig_pie_payment_method, fig_total_sales_per_year


# Fonction de rappel pour mettre à jour les DataTables avec des données paginées.
def update_tables_callback(fetch_function, page_current, page_size, columns):
    """
    Callback function to update DataTable with paginated data.

    Parameters:
    - fetch_function: The function to fetch data from the database.
    - page_current: The current page number.
    - page_size: The number of rows per page.
    - columns: List of column names.

    Returns:
    - List of dictionaries representing the data for DataTable.
    """
    data = fetch_function()
    start_index = page_current * page_size
    end_index = (page_current + 1) * page_size

    # Format the data as a list of dictionaries
    formatted_data = []
    for row in data[start_index:end_index]:
        formatted_row = {column: value for column, value in zip(columns, row)}
        formatted_data.append(formatted_row)

    return formatted_data
