# WhatsApp AI Sales Agent

A smart WhatsApp AI assistant designed for e-commerce and shopping. It handles customer inquiries naturally while referencing live product inventory from a database, effectively serving as an automated 24/7 sales representative.

## Key Features

- **Conversational AI Sales**: Uses LLMs (via OpenRouter) to chat with customers, answer questions, and recommend products based on real-time inventory.
- **WhatsApp Cloud API native**: Fully integrated with the official Meta WhatsApp Business Cloud API through webhooks.
- **Persistent Memory**: Saves conversation histories to a PostgreSQL database so the AI remembers the context of the chat.
- **Live Inventory Context**: Dynamically injects up-to-date products and pricing directly into the AI's prompts.
- **High Performance & Reliable**: Built efficiently using asynchronous Python (FastAPI), with background task processing for instant webhook acknowledgments and Redis-backed idempotency to prevent duplicate message processing.

## Tech Stack

- **Framework**: Python 3, FastAPI
- **Database**: PostgreSQL (SQLAlchemy + asyncpg), Alembic for migrations
- **Caching**: Redis
- **AI Integration**: OpenRouter API (`openrouter/free` or other models)
- **Deployment**: Docker & Docker Compose (for Postgres/Redis infrastructure)

## Setup & Installation

**1. Clone the project and install dependencies**
```bash
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
```

**2. Start internal infrastructure (Postgres & Redis)**
```bash
docker-compose up -d
```

**3. Set up the Environment Variables**
Rename `.env.example` to `.env` and fill in your credentials:
- OpenRouter API key
- WhatsApp Meta App details (Verify Token, Access Token, Phone Number ID)
- Postgres and Redis URIs

**4. Run Database Migrations and Seed Data**
```bash
# Apply any alembic migrations
alembic upgrade head

# Seed test products
python seed_db.py
```

**5. Start the Application**
```bash
uvicorn app.main:app --reload
```

## How It Works

1. A customer sends a message to your WhatsApp Business number.
2. Meta sends a webhook containing the message to the FastAPI `/api/v1/webhook` endpoint.
3. The server immediately returns a `200 OK` and passes work to a background task so WhatsApp doesn't timeout.
4. The Redis cache checks if this message ID was already processed (Idempotency).
5. The PostgreSQL DB fetches the latest store inventory and the past conversation history.
6. The AI API generates a contextual response acting as a friendly store assistant.
7. The response is sent back to the customer's WhatsApp instantly.
