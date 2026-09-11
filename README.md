# Enterprise AI Data Assistant

A production-style multi-agent AI assistant that answers questions across both unstructured enterprise documents and structured business data.

The application uses a React + TypeScript frontend, FastAPI backend, Azure AI Foundry agents, Azure AI Search for document retrieval, and Neon PostgreSQL for structured data queries.

It is deployed end-to-end with:

- Frontend on Azure Static Web Apps
- Backend on Azure Container Apps
- Azure Managed Identity for secure authentication
- Neon PostgreSQL for cloud-hosted relational data

---

## Overview

Enterprise AI Data Assistant is designed to simulate a real-world enterprise AI platform where users can ask natural-language questions and receive answers from the appropriate data source.

A manager agent determines whether a question should be handled by:

- a RAG agent for enterprise documents
- a SQL agent for structured database questions
- both agents for hybrid questions

---

## Demo

![Enterprise AI Data Assistant UI](docs/images/demo.png)

### Live Application

Frontend:

https://purple-sea-085e43810.5.azurestaticapps.net

API Documentation:

https://enterprise-ai-data-assistant-api.calmsky-9378937f.centralus.azurecontainerapps.io/docs

### Example Questions

```text
What is the warranty period for the Pro Gateway?

How many support tickets are currently open?

How many support tickets are there in total?

How many support tickets are open, and what does the warranty policy say?
```

---

## Architecture

```text
                        ┌──────────────────────────────┐
                        │        User / Browser        │
                        └──────────────┬───────────────┘
                                       │
                                       ▼
                        ┌──────────────────────────────┐
                        │   React + TypeScript UI      │
                        │  Azure Static Web Apps       │
                        └──────────────┬───────────────┘
                                       │
                                  HTTPS / REST
                                       │
                                       ▼
                        ┌──────────────────────────────┐
                        │        FastAPI Backend       │
                        │   Azure Container Apps       │
                        └──────────────┬───────────────┘
                                       │
                                       ▼
                        ┌──────────────────────────────┐
                        │       Manager Agent          │
                        │     Azure AI Foundry         │
                        └──────────────┬───────────────┘
                                      / \
                                     /   \
                                    ▼     ▼
                    ┌──────────────────┐  ┌──────────────────┐
                    │    RAG Agent     │  │    SQL Agent     │
                    └────────┬─────────┘  └────────┬─────────┘
                             │                     │
                             ▼                     ▼
                 ┌────────────────────┐   ┌────────────────────┐
                 │ Azure AI Search    │   │ Neon PostgreSQL    │
                 │ Enterprise Docs    │   │ Structured Data    │
                 └────────────────────┘   └────────────────────┘
```

---

## How It Works

The user submits a question through the React frontend.

The frontend sends the request to the FastAPI backend.

The manager agent determines which specialist agent should handle the request.

```text
Document / policy question
        ↓
RAG Agent

Structured database question
        ↓
SQL Agent

Question requiring both
        ↓
RAG Agent + SQL Agent
```

The final response is returned to the frontend together with information about which agent handled the request.

---

## Key Features

- Multi-agent orchestration
- Natural-language question answering
- RAG over enterprise documents
- SQL querying over structured business data
- Dynamic routing between RAG and SQL agents
- Hybrid multi-agent workflows
- React + TypeScript frontend
- FastAPI REST API
- Azure AI Foundry agents
- Azure AI Search document retrieval
- Neon PostgreSQL database
- Dockerized backend
- Azure Container Apps deployment
- Azure Static Web Apps deployment
- Azure Managed Identity
- Azure RBAC
- Environment-based configuration
- CORS configuration for frontend/backend communication

---

## Agent Architecture

### Manager Agent

The manager agent acts as the orchestration layer.

Its responsibility is to determine which specialist agent should answer the request.

It can route questions to:

- RAG Agent
- SQL Agent
- both agents for hybrid questions

This separates orchestration logic from specialist capabilities.

---

### RAG Agent

The RAG agent answers questions using enterprise documents indexed in Azure AI Search.

Example use cases include:

- warranty information
- product documentation
- service manuals
- return policies
- enterprise knowledge documents

Example:

```text
What is the warranty period for the Pro Gateway?
```

---

### SQL Agent

The SQL agent handles questions that require structured data.

The demo database contains support-ticket information stored in Neon PostgreSQL.

Example questions:

```text
How many support tickets are there?

How many support tickets are open?

How many critical support tickets exist?
```

The SQL workflow is designed for read-only analytical querying.

---

## Technology Stack

| Layer | Technology |
|---|---|
| Frontend | React, TypeScript |
| Frontend Build Tool | Vite |
| Styling | CSS |
| Backend | FastAPI, Python |
| Agent Platform | Azure AI Foundry |
| LLM | Azure OpenAI |
| Document Retrieval | Azure AI Search |
| Database | Neon PostgreSQL |
| Database Access | SQLAlchemy |
| Authentication | Azure Managed Identity |
| Credential Handling | DefaultAzureCredential |
| Authorization | Azure RBAC |
| Containerization | Docker |
| Backend Hosting | Azure Container Apps |
| Frontend Hosting | Azure Static Web Apps |

---

## Frontend

The frontend is built using React, TypeScript, Vite, and CSS.

The interface includes:

- user prompt input
- suggested prompts
- loading state
- response display
- agent-routing indicator
- Manager Agent card
- RAG Agent card
- SQL Agent card

The frontend communicates with the FastAPI backend through REST API calls.

Example:

```typescript
const response = await fetch(`${API_URL}/ask`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    question,
  }),
})
```

---

## Backend

The backend is implemented using FastAPI.

Main endpoints include:

```text
GET  /
GET  /health
POST /ask
POST /sql
```

The `/ask` endpoint sends the user's question through the orchestration layer.

Example request:

```json
{
  "question": "How many support tickets are open?"
}
```

Example response:

```json
{
  "answer": "There are 3 open support tickets.",
  "agents_used": [
    "SQL Agent"
  ]
}
```

---

## Database

The structured-data workflow uses Neon PostgreSQL.

Example support-ticket schema:

```sql
CREATE TABLE support_tickets (
    id SERIAL PRIMARY KEY,
    product VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL,
    severity VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

SQLAlchemy is used for database connectivity.

Example:

```python
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_recycle=300,
)
```

---

## Security

The deployed backend uses a system-assigned Azure Managed Identity.

Authentication flow:

```text
Azure Container App
        ↓
Managed Identity
        ↓
DefaultAzureCredential
        ↓
Azure Access Token
        ↓
Azure AI Foundry
```

The Container App identity is granted access to the Azure AI Foundry resource using Azure RBAC.

This avoids storing Azure client secrets directly in application code.

Sensitive values such as database credentials and API keys are stored using environment variables and Azure Container App secrets.

---

## Project Structure

```text
enterprise-ai-data-assistant/
│
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── App.css
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
│
├── src/
│   └── enterprise_ai_data_assistant/
│       ├── api/
│       │   └── routes/
│       ├── services/
│       ├── config.py
│       ├── database.py
│       └── main.py
│
├── tests/
├── Dockerfile
├── pyproject.toml
├── uv.lock
└── README.md
```

---

## Local Setup

### Prerequisites

Install:

- Python 3.11+
- Node.js
- npm
- Docker
- Azure CLI
- uv

Clone the repository:

```bash
git clone https://github.com/nakulpyasi/enterprise-ai-data-assistant.git
cd enterprise-ai-data-assistant
```

---

## Backend Setup

Create a `.env` file in the project root.

Example:

```env
APP_NAME=Enterprise AI Data Assistant

AZURE_SEARCH_ENDPOINT=<your-search-endpoint>
AZURE_SEARCH_KEY=<your-search-key>
AZURE_SEARCH_INDEX=enterprise-rag

AZURE_OPENAI_ENDPOINT=<your-openai-endpoint>
AZURE_OPENAI_API_KEY=<your-openai-api-key>
AZURE_OPENAI_MODEL=gpt-4.1-mini

DATABASE_URL=<your-postgresql-connection-string>

FOUNDRY_PROJECT_ENDPOINT=<your-foundry-project-endpoint>

FOUNDRY_RAG_AGENT_NAME=enterprise-rag-agent
FOUNDRY_RAG_AGENT_VERSION=4

FOUNDRY_SQL_AGENT_NAME=enterprise-sql-agent
FOUNDRY_SQL_AGENT_VERSION=4
```

Do not commit `.env` to GitHub.

Install dependencies:

```bash
uv sync
```

Start the FastAPI backend:

```bash
uv run uvicorn enterprise_ai_data_assistant.main:app --reload
```

Backend:

```text
http://localhost:8000
```

Swagger API documentation:

```text
http://localhost:8000/docs
```

---

## Frontend Setup

Open another terminal:

```bash
cd frontend
npm install
```

Create:

```text
frontend/.env
```

Add:

```env
VITE_API_URL=http://localhost:8000
```

Start the development server:

```bash
npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

## Production Frontend Build

Build the frontend:

```bash
cd frontend
npm run build
```

This runs TypeScript validation and Vite's production build.

The optimized frontend files are created in:

```text
frontend/dist
```

---

## Docker

Build and push the backend image:

```bash
docker buildx build \
  --platform linux/amd64 \
  -t nakulpyasi11/enterprise-ai-data-assistant:latest \
  --push \
  .
```

The `linux/amd64` platform is used for compatibility with Azure Container Apps.

Run locally:

```bash
docker run \
  --env-file .env \
  -p 8000:8000 \
  nakulpyasi11/enterprise-ai-data-assistant:latest
```

---

## Deployment

### Backend

The FastAPI backend is deployed to Azure Container Apps.

```text
Application Code
      ↓
Docker Image
      ↓
Docker Hub
      ↓
Azure Container Apps
      ↓
FastAPI / Uvicorn
```

Runtime configuration is supplied through Azure Container App environment variables and secrets.

---

### Frontend

The React frontend is deployed to Azure Static Web Apps.

```text
React + TypeScript
        ↓
npm run build
        ↓
dist/
        ↓
Azure Static Web Apps
```

The deployed frontend calls the Azure Container Apps backend using:

```env
VITE_API_URL=<AZURE_CONTAINER_APP_URL>
```

---

## CORS

The frontend and backend are hosted on different domains.

FastAPI therefore uses CORS configuration to allow the frontend to communicate with the backend.

Example:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://purple-sea-085e43810.5.azurestaticapps.net",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## What This Project Demonstrates

This project demonstrates practical experience with:

- agentic AI architecture
- multi-agent orchestration
- agent routing
- retrieval-augmented generation
- natural-language-to-SQL workflows
- Azure AI Foundry
- Azure AI Search
- PostgreSQL
- FastAPI
- React
- TypeScript
- Docker
- Azure Container Apps
- Azure Static Web Apps
- Managed Identity
- Azure RBAC
- REST APIs
- full-stack AI application deployment

---

## Author

**Nakul Pyasi**

Data Scientist / Machine Learning Engineer focused on:

- Agentic AI
- LLM systems
- RAG
- AI platforms
- MLOps
- production AI applications

---

## Disclaimer

This project is a portfolio demonstration of an enterprise-style AI architecture.

The included datasets and enterprise scenarios are intended for demonstration purposes.
