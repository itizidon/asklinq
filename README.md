---

# 📱 AskLinq — Text Your Documents and Get Answers

## What it does

* 📄 Send PDFs or text files via iMessage/SMS and have them automatically processed
* 🧠 Ask questions about your documents and get AI answers instantly
* 🔎 Semantic search across your personal document memory using embeddings (pgvector)
* 📦 Automatic document chunking + embedding pipeline per user
* 🔐 Multi-user isolation — each phone number has its own private knowledge base

---

## Architecture

```
User ──iMessage──▶ Linq Blue ──webhook──▶ FastAPI RAG Server ──▶ OpenAI Embeddings
                                                        │
                                                        │
                                                        ├──▶ PostgreSQL + pgvector
                                                        │        (chunks + embeddings)
                                                        │
                                                        └──▶ Claude / GPT (answer generation)

User ◀──iMessage── Linq Blue ◀────API response────── AI Answer
```

---

## Quick Start

### Prerequisites

* Python 3.10+
* PostgreSQL with `pgvector` enabled
* ngrok (for local webhook testing)
* Linq Blue sandbox account
* OpenAI API key (embeddings + chat)

---

## Setup

```bash
# Clone the repo
git clone https://github.com/yourname/asklinq.git
cd asklinq

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

### Environment Variables

Create `.env`:

```
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/asklinq
OPENAI_API_KEY=your_openai_key
LINQ_API_KEY=your_linq_api_key
LINQ_FROM_NUMBER=+1XXXXXXXXXX
```

---

## Run the server

```bash
uvicorn app.main:app --reload --port 8000
```

Expose it with ngrok:

```bash
ngrok http 8000
```

Then set your webhook in Linq Blue to:

```
https://your-ngrok-url.ngrok-free.app/webhook/linq
```

---

## How it works

1. User sends a message or PDF via iMessage/SMS
2. Linq Blue triggers `message.received` webhook
3. Server extracts:

   * phone number
   * text message OR file URL
4. If file:

   * PDF/text is downloaded
   * text is extracted
   * document is chunked
   * chunks are embedded
   * embeddings stored in PostgreSQL (pgvector)
5. If question:

   * question is embedded
   * similarity search over user's chunks
   * top results passed into LLM
6. LLM generates answer
7. Response is sent back via Linq API

---

## Key Features

* Multi-user isolation (phone number based)
* PDF + TXT ingestion
* Vector similarity search (pgvector)
* Stateless FastAPI webhook
* Real-time SMS/iMessage interaction via Linq
* Fully serverless-friendly design

---

## Project Structure

```
app/
├── main.py                # FastAPI app + webhook
├── api/
│   └── webhooks.py       # Linq webhook handler
├── core/
│   ├── database.py       # Async DB session
│   └── config.py         # Env variables
├── users/
│   └── service.py       # get_or_create_user
├── rag/
│   ├── store.py         # document + chunk storage
│   ├── search.py        # vector similarity search
│   ├── embeddings.py    # OpenAI embeddings
│   ├── chunker.py       # text splitting
│   └── ask.py           # LLM answering logic
```

---

## Commands

Users can text:

| Command               | Action                        |
| --------------------- | ----------------------------- |
| “hello”               | Chat with documents           |
| send PDF              | ingest document automatically |
| “what does this say?” | semantic retrieval            |

---
### Railway

Set:

```
PORT=8000
DATABASE_URL=...
OPENAI_API_KEY=...
LINQ_API_KEY=...
```

Deploy normally and set webhook URL to deployed endpoint.

---

## Built with

* Linq Blue — iMessage / SMS webhook API
* FastAPI — backend server
* PostgreSQL + pgvector — vector database
* OpenAI — embeddings + LLM reasoning
* PyPDF — PDF parsing

---

## License

MIT

---
