# Architecture

## Overview

**denti-code-broker-srv** is the event/message broker shim for the denti-code platform. It provides an HTTP endpoint for microservices to publish events to RabbitMQ, decoupling producers from consumers.

```
┌─────────────────────┐     POST /api/publish     ┌──────────────────────┐
│  Producer Services  │──────────────────────────►│  Broker Service      │
│                     │  { routing_key, body }    │  Flask · Python 3    │
│  Auth Service       │                            │  (port 5000)         │
│  Patient Service    │                            │                      │
│  Appointments Svc   │                            │  publish_event()     │
│                     │                            │         │            │
└─────────────────────┘                            │         │ pika      │
                                                   │         ▼            │
                                                   │  ┌──────────────┐   │
                                                   │  │   RabbitMQ   │   │
                                                   │  │  Topic Exch. │   │
                                                   │  │denti_code_   │   │
                                                   │  │   events     │   │
                                                   │  └──────┬───────┘   │
                                                   └─────────┼───────────┘
                                                             │
                                                   ┌─────────▼───────────┐
                                                   │  Consumer Services  │
                                                   │                     │
                                                   │  Patient Service    │
                                                   │  (user.registered)  │
                                                   │  Other services     │
                                                   └─────────────────────┘
```

## Project Structure

```
app/
  __init__.py           # Flask app factory (create_app)
  broker.py             # RabbitMQ publishing logic (pika)
  consumer.py           # Standalone RabbitMQ consumer (example)
  routes.py             # Flask Blueprint with POST /api/publish
run.py                  # Entry point
```

## Message Flow

```
Producer                          Broker                        RabbitMQ
  │                                 │                             │
  │ POST /api/publish               │                             │
  │ { routing_key: "user.registered",│                            │
  │   body: { userId, email, ... }} │                             │
  │────────────────────────────────►│                             │
  │                                 │ pika.BlockingConnection     │
  │                                 │────────────────────────────►│
  │                                 │  basic_publish              │
  │                                 │  exchange: denti_code_events│
  │                                 │  routing_key: user.registered│
  │                                 │◄────────────────────────────│
  │◄──────── 202 Accepted ─────────│                             │
```

## API Routes

| Method | Endpoint          | Description                          |
|--------|-------------------|--------------------------------------|
| POST   | `/api/publish`    | Publish event to RabbitMQ exchange   |

Request body:
```json
{
  "routing_key": "user.registered",
  "body": { "userId": "abc123", "email": "user@example.com" }
}
```

## Consumer

The standalone consumer (`app/consumer.py`) listens for `user.registered` events and auto-reconnects on connection loss:
- Exchange: `denti_code_events` (topic, durable)
- Queue: `patient_service_queue`
- Binding key: `user.registered`
