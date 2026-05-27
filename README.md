# Competitor Intelligence API

An AI-powered competitive intelligence tool that automatically discovers competitors, scrapes their websites, and extracts structured signals — pricing, features, strengths, and weaknesses — using Claude and Firecrawl.

**Live demo:** [competitor-intelligence-ui-eight.vercel.app](https://competitor-intelligence-ui-eight.vercel.app)

---

## What it does

1. User inputs a company name and industry
2. Claude AI identifies the top 5 direct competitors
3. Firecrawl scrapes each competitor's website and G2 review page
4. Claude extracts structured intelligence: pricing model, features, strengths, weaknesses, target market
5. Results are stored in PostgreSQL and returned to the frontend

---

## Tech stack

| Layer | Technology |
|---|---|
| Backend | FastAPI (Python) |
| AI | Anthropic Claude API |
| Scraping | Firecrawl |
| Database | PostgreSQL (Railway) |
| Frontend | React + Vite |
| Backend hosting | Railway |
| Frontend hosting | Vercel |

---

## Project structure

```
competitor-intelligence-api/
├── app/
│   ├── main.py              # FastAPI entry point, CORS, lifespan
│   ├── config.py            # Environment variable management
│   ├── database.py          # Async SQLAlchemy engine and session
│   ├── models/
│   │   ├── competitor.py    # Competitor DB model
│   │   └── analysis.py      # Analysis DB model
│   ├── schemas/
│   │   ├── competitor.py    # Pydantic input/output schemas
│   │   └── analysis.py      # Pydantic input/output schemas
│   ├── routers/
│   │   ├── competitors.py   # POST /discover, GET / endpoints
│   │   └── analysis.py      # POST /{id}/run, GET /{id} endpoints
│   └── services/
│       ├── claude_service.py     # Competitor discovery + signal extraction
│       └── firecrawl_service.py  # Website + G2 scraping
└── tests/
    └── test_main.py
```

---

## API endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| POST | `/api/competitors/discover` | Discover competitors via Claude |
| GET | `/api/competitors/` | List all saved competitors |
| GET | `/api/competitors/{id}` | Get a single competitor |
| POST | `/api/analysis/{id}/run` | Run full analysis pipeline |
| GET | `/api/analysis/{id}` | Get saved analysis |

---

## Running locally

### Prerequisites
- Python 3.12+
- PostgreSQL running locally
- Anthropic API key — [console.anthropic.com](https://console.anthropic.com)
- Firecrawl API key — [firecrawl.dev](https://firecrawl.dev)

### Setup

```bash
# Clone the repo
git clone https://github.com/Deeks89/competitor-intelligence-api
cd competitor-intelligence-api

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Fill in your API keys and DATABASE_URL in .env

# Start the server
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.  
Interactive docs at `http://localhost:8000/docs`.

---

## Environment variables

```
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/competitor_intelligence
ANTHROPIC_API_KEY=sk-ant-...
FIRECRAWL_API_KEY=fc-...
```

---

## Frontend repo

[github.com/Deeks89/competitor-intelligence-ui](https://github.com/Deeks89/competitor-intelligence-ui)

---

## Author

Built by [Deekshitha](https://github.com/Deeks89) as a portfolio project demonstrating AI-powered product development with FastAPI, Claude, and Firecrawl.
