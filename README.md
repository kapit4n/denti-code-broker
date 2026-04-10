# denti-code-broker-srv

Small **Flask** service that accepts **HTTP POST** publishes and forwards them to **RabbitMQ** (exchange `denti_code_events`, topic routing).

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

- HTTP: **http://localhost:5000**
- Publish: **POST /api/publish** — body `{ "routing_key": "user.registered", "body": { ... } }`
- Requires **RabbitMQ** on `localhost:5672` (e.g. Docker: `rabbitmq:3-management-alpine`).

## Monorepo stack

From **`denti-code-u2`**, `./start-denti-stack.sh dev` starts RabbitMQ (Docker), then this service, then services that publish/consume (see parent README).

Auth env: `BROKER_PUBLISH_URL=http://localhost:5000/api/publish`
