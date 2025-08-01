# app/broker.py
import pika
import json

RABBITMQ_HOST = 'localhost'
EXCHANGE_NAME = 'denti_code_events'

def get_connection():
    """Establishes a connection to RabbitMQ."""
    return pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))

def publish_event(routing_key, body):
    """
    Publishes an event to the RabbitMQ exchange.
    
    :param routing_key: The key to route the message (e.g., 'user.registered').
    :param body: A dictionary containing the message payload.
    """
    connection = None
    try:
        connection = get_connection()
        channel = connection.channel()

        # Declare a 'topic' exchange, which is flexible for routing
        channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='topic', durable=True)

        message = json.dumps(body)

        channel.basic_publish(
            exchange=EXCHANGE_NAME,
            routing_key=routing_key,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ))
        print(f" [x] Sent event with routing key '{routing_key}': {message}")
    except Exception as e:
        print(f"Error publishing event: {e}")
        # In a real app, you'd have more robust error handling/retry logic
    finally:
        if connection:
            connection.close()