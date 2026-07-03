# Tech Stack

| Layer              | Technology                              |
|--------------------|-----------------------------------------|
| Runtime            | Python 3                                |
| Web Framework      | Flask                                   |
| Message Broker     | RabbitMQ (via pika AMQP library)        |
| Exchange Type      | Topic                                   |
| Protocols          | HTTP (Flask) + AMQP (RabbitMQ)          |
| Config             | Hardcoded constants in source           |

## Dependencies (`requirements.txt`)

| Package      | Purpose                                 |
|--------------|-----------------------------------------|
| Flask        | Web framework for HTTP API              |
| pika         | Python AMQP library for RabbitMQ        |
| python-dotenv| Installed but not currently used        |

## Configuration

All values are currently hardcoded in source files:

| Constant            | Value                  | Defined In     |
|---------------------|------------------------|----------------|
| `RABBITMQ_HOST`     | `localhost`            | `broker.py`    |
| `EXCHANGE_NAME`     | `denti_code_events`    | `broker.py`    |
| `QUEUE_NAME`        | `patient_service_queue`| `consumer.py`  |
| `BINDING_KEY`       | `user.registered`      | `consumer.py`  |

## Running

```bash
# Start the HTTP server
python run.py

# Start the consumer (separate process)
python app/consumer.py
```

The server runs on `http://0.0.0.0:5000`.
