import psycopg2

# Configuration de la connexion à la base de données PostgreSQL
db_config = {
    'host': 'localhost',
    'database': 'ecom_db',
    'user': 'postgres',
    'password': 'mohamed',
}

columns_category = ['orderDate', 'category', 'totalSales']
columns_day = ['orderDate', 'totalSales']
columns_month = ['year', 'month', 'totalSales']
page_current = 0
page_size = 10


# Fonction pour récupérer les données de la table sales_per_category
def fetch_sales_per_category():
    """
    Fonction pour récupérer les données de la table sales_per_category depuis la base de données.

    Retourne :
    - List : Liste des données de la table sales_per_category.
    """
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM sales_per_category ORDER BY order_date DESC ;")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data


# Fonction pour récupérer les données de la table sales_per_day
def fetch_sales_per_day():
    """
    Fonction pour récupérer les données de la table sales_per_day depuis la base de données.

    Retourne :
    - List : Liste des données de la table sales_per_day.
    """
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM sales_per_day ORDER BY order_date DESC ;")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data


# Fonction pour récupérer les données de la table sales_per_month
def fetch_sales_per_month():
    """
    Fonction pour récupérer les données de la table sales_per_month depuis la base de données.

    Retourne :
    - List : Liste des données de la table sales_per_month.
    """
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM sales_per_month ORDER BY year, month DESC;")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data


# Fonction pour récupérer les données de la table transactions
def fetch_order():
    """
    Fonction pour récupérer les données de la table transactions depuis la base de données.

    Retourne :
    - List : Liste des données de la table transactions.
    """
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM transactions;')
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data


def fetch_sales_per_currency():
    """
    Fonction pour récupérer les données de ventes par devise depuis la base de données.

    Retourne :
    - List : Liste des données de ventes par devise.
    """
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT currency, COUNT(order_id) FROM transactions GROUP BY currency;")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data


def fetch_sales_per_payment_method():
    """
    Fonction pour récupérer les données de ventes par méthode de paiement depuis la base de données.

    Retourne :
    - List : Liste des données de ventes par méthode de paiement.
    """
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT payment_method, COUNT(*) FROM transactions GROUP BY payment_method;")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data


def fetch_total_sales_per_year():
    """
    Fonction pour récupérer les données de ventes totales par année depuis la base de données.

    Retourne :
    - List : Liste des données de ventes totales par année.
    """
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT year, SUM(total_sales) FROM sales_per_month GROUP BY year;")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data


# Fonction pour récupérer le nombre total de transactions
def fetch_total_transactions():
    """
    Fonction pour récupérer le nombre total de transactions depuis la base de données.

    Retourne :
    - int : Nombre total de transactions.
    """
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(order_id) FROM transactions;")
    data = cursor.fetchone()
    cursor.close()
    connection.close()
    return data[0]  # Retourne le nombre total de transactions


# Fonction pour récupérer le montant total pour chaque devise
def fetch_total_amount_per_currency():
    """
    Fonction pour récupérer le montant total pour chaque devise depuis la base de données.

    Retourne :
    - List : Liste des données du montant total par devise.
    """
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT currency, SUM(total_amount) FROM transactions GROUP BY currency;")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data
