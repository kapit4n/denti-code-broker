import pika
import json
import time

RABBITMQ_HOST = 'localhost'
EXCHANGE_NAME = 'denti_code_events'
QUEUE_NAME = 'patient_service_queue' # A queue for the patient service
BINDING_KEY = 'user.registered' # This queue is interested in 'user.registered' events

def callback(ch, method, properties, body):
    """This function is called when a message is received."""
    print(f" [ consumer ] Received event with routing key '{method.routing_key}'")
    
    try:
        message = json.loads(body)
        print(f" [ consumer ] Processing message: {message}")
        
        print(" [ consumer ] Done processing.")
        ch.basic_ack(delivery_tag=method.delivery_tag) # Acknowledge the message
    except Exception as e:
        print(f" [ consumer ] Error processing message: {e}")
        # In a real app, you might requeue the message or move it to a dead-letter queue
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


def start_consuming():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
            channel = connection.channel()

            channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='topic', durable=True)
            
            # Declare a durable queue
            channel.queue_declare(queue=QUEUE_NAME, durable=True)
            
            # Bind the queue to the exchange with the specific routing key
            channel.queue_bind(exchange=EXCHANGE_NAME, queue=QUEUE_NAME, routing_key=BINDING_KEY)

            print(' [*] Consumer waiting for events. To exit press CTRL+C')
            channel.basic_qos(prefetch_count=1) # Process one message at a time
            channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)
            
            channel.start_consuming()

        except pika.exceptions.AMQPConnectionError:
            print("Connection to RabbitMQ failed. Retrying in 5 seconds...")
            time.sleep(5)
        except Exception as e:
            print(f"An unexpected error occurred: {e}. Restarting consumer...")
            time.sleep(5)

if __name__ == '__main__':
    start_consuming()