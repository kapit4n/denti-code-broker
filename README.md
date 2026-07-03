# denti-code-broker-srv

Event broker shim for the denti-code platform. Accepts HTTP events from microservices and relays them to RabbitMQ.

## System Diagram

```
Microservice ──POST /api/publish──► Broker Svc ──AMQP──► RabbitMQ ──► Consumer
                                     (port 5000)          │
                                                      user.registered
                                                           │
                                                           ▼
                                                   Patient Service
```

## How It Works

1. Any service POSTs an event to `/api/publish` with a `routing_key` and `body`
2. The broker publishes the message to a RabbitMQ topic exchange `denti_code_events`
3. Consumers (like the Patient Service) listen on bound queues for relevant routing keys

## Getting Started

```bash
pip install -r requirements.txt
python run.py
```

Server starts on `http://0.0.0.0:5000`.

Requires RabbitMQ running on `localhost:5672`.

## Docs

- [Architecture](./ARCHITECTURE.md)
- [Tech Stack](./TECH_STACK.md)
