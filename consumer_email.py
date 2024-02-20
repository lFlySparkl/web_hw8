import pika
import json
from mongoengine import connect

# Підключення до MongoDB
connect(db='my_mongodb', host='mongodb://localhost:27017')

# Підключення до RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Оголошення черги
channel.queue_declare(queue='email_queue')

# Функція для обробки повідомлень
def callback(ch, method, properties, body):
    # Витягуємо ID з JSON
    contact_id = json.loads(body.decode('utf-8'))['contact_id']

    # Логіка обробки Email (заглушка)
    print(f"Sending Email to contact with ID: {contact_id}")

# Встановлюємо функцію зворотного виклику для обробки повідомлень
channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)

# Очікуємо повідомлень з черги
print('Waiting for Email messages. To exit press CTRL+C')
channel.start_consuming()