import pika
import json
from faker import Faker
from mongoengine import connect, Document, StringField, BooleanField

# Підключення до MongoDB
connect(db='my_mongodb', host='mongodb://localhost:27017')

# Визначення моделі для контакту
class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    phone_number = StringField(required=True)
    send_via = StringField(choices=['SMS', 'email'], required=True)
    is_sent = BooleanField(default=False)

# Параметри підключення до RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Оголошення черг для SMS та email
channel.queue_declare(queue='sms_queue')
channel.queue_declare(queue='email_queue')

# Генерація фейкових контактів і відправка їх до MongoDB та RabbitMQ
fake = Faker()
num_contacts = 10  # Задайте бажану кількість контактів
for _ in range(num_contacts):
    contact_data = {
        'fullname': fake.name(),
        'email': fake.email(),
        'phone_number': fake.phone_number(),
        'send_via': fake.random_element(elements=('SMS', 'email')),
        'is_sent': False,
    }

    # Запис контакту в MongoDB
    contact = Contact(**contact_data)
    contact.save()

    # Відправка повідомлення до RabbitMQ з ID створеного контакту
    queue_name = 'sms_queue' if contact.send_via == 'SMS' else 'email_queue'
    message = {'contact_id': str(contact.id)}
    channel.basic_publish(exchange='', routing_key=queue_name, body=json.dumps(message))

print(f'{num_contacts} contacts generated and added to the queues.')

# Закриття з'єднань
connection.close()