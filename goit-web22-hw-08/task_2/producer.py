import json
from faker import Faker
import pika
from contact_model import Contact

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='email_queue')

# Генерація фейкових контактів
fake = Faker()
num_contacts = 10

for _ in range(num_contacts):
    fullname = fake.name()
    email = fake.email()
    additional_info = fake.text()

    # Створення контакту та збереження в базу даних
    contact = Contact(fullname=fullname, email=email, additional_info=additional_info)
    contact.save()

    # Відправлення ObjectID контакту в чергу
    message = {'contact_id': str(contact.id)}
    channel.basic_publish(exchange='', routing_key='email_queue', body=json.dumps(message))

print("Contacts generated and messages sent to queue")
connection.close()


