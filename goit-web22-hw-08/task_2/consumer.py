import pika
import json
from contact_model import Contact

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='email_queue')


def send_email(contact):
    # Імітація надсилання email
    print(f"Sending email to {contact.email}")
    # Тут можна додати логіку для реального надсилання email


def callback(ch, method, properties, body):
    message = json.loads(body)
    contact_id = message['contact_id']

    # Отримання контакту з бази даних
    contact = Contact.objects(id=contact_id).first()
    if contact and not contact.message_sent:
        # Імітація надсилання email
        send_email(contact)
        # Оновлення статусу контакту
        contact.message_sent = True
        contact.save()

    ch.basic_ack(delivery_tag=method.delivery_tag)


# Підписка на чергу
channel.basic_consume(queue='email_queue', on_message_callback=callback)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
