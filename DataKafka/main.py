import json
import random
import time
from datetime import datetime, timedelta

from confluent_kafka import SerializingProducer
from faker import Faker

fake = Faker()

# Mapping of product categories to lists of possible product names and product brands
category_to_products = {
    'Electronic': {
        'names': ['MacBook pro 16', 'Iphone 13', 'Samsung S22 ultra', 'Smart watch T500', 'Souris laser', 'Microphone'],
        'brands': ['Apple', 'Samsung', 'Xaoming', 'Boat', 'Sony']
    },
    'Fashion': {
        'names': ['T-Shirt', 'Pentalon', 'Jupe', 'Robe', 'Costar'],
        'brands': ['Nike', 'Addidas', 'Zara', 'H&M']
    },
    'Grocery': {
        'names': ['Franboise', 'Tarte au pommes', 'Mikado', 'Fraise', 'Viande', 'Maïs'],
        'brands': ['Local Farmer', 'Bakery Co.', 'SnackCo']
    },
    'Home': {
        'names': ['Aspirateur ', 'Mixeur', 'Micro-ondes'],
        'brands': ['Dayson', 'Philips', 'Sony']
    },
    'Beauty': {
        'names': ['Perfume', 'Makeup kit', 'Hair straightener'],
        'brands': ['Chanel', 'Maybelline', 'Philips']
    },
    'Sports': {
        'names': ['Snicker', 'Basketball', 'Yoga mat', 'Baseball', 'Real Madrid kit'],
        'brands': ['Nike', 'Adidas', 'Decathlon', 'Real Madrid CF']
    }
}


def generate_sales():
    # Generate fake user profile data
    user = fake.simple_profile()

    # Generate a random date within the current decade
    order_date = fake.date_time_this_decade(tzinfo=None)

    # Add a random number of days to the order date
    order_date += timedelta(days=random.randint(1, 365))

    #order_date = datetime.utcnow()

    # Convert the order date to a string
    order_date = order_date.strftime('%Y-%m-%dT%H:%M:%S.%f%z')

    # Generate a random product category
    category = random.choice(['Electronic', 'Fashion', 'Grocery', 'Home', 'Beauty', 'Sports'])

    # Choose a product name and brand based on the product category
    product_info = category_to_products[category]
    product_name = random.choice(product_info['names'])
    product_brand = random.choice(product_info['brands'])

    # Generate a random product price as an integer
    product_price = round(random.uniform(10, 1000))
    product_quantity = random.randint(1, 10)

    # Check if the currency is FCFA and adjust the product price accordingly
    currency = random.choice(['FCFA', 'USD', 'EUR'])
    if currency == 'FCFA':
        product_price *= 10

    # Return a json representing a simulated sales transaction
    return {
        "orderId": fake.uuid4(),
        "productId": fake.uuid4(),
        "productName": product_name,
        "productCategory": category,
        "productPrice": product_price,
        "productQuantity": product_quantity,
        "productBrand": product_brand,
        "currency": currency,
        "customerId": user['username'],
        "orderDate": order_date,
        "paymentMethod": random.choice(['CREDIT_CARD', 'CASH_ON_DELIVERY', 'ORANGE_MONEY']),
        "totalAmount": product_price * product_quantity
    }


def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f"Message delivered to {msg.topic} [{msg.partition()}]")


def main():
    topic = 'product_sold'
    producer = SerializingProducer({
        'bootstrap.servers': 'localhost:9092'
    })

    # The time when transaction started
    start_time = datetime.now()
    total_sales = 0

    while (datetime.now() - start_time).seconds < 120:
        try:
            order = generate_sales()
            print(order)
            producer.produce(
                topic,
                key=order['orderId'],
                value=json.dumps(order),
                on_delivery=delivery_report
            )
            producer.poll(0)

            total_sales += 1

            # wait for 2 seconds before sending the next transaction
            time.sleep(2)
        except BufferError:
            print("Buffer full! Waiting...")
            time.sleep(1)
        except Exception as e:
            print(e)

    print(f"Total number of sales generated: {total_sales}")


if __name__ == "__main__":
    main()
