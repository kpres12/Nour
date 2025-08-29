# Nour - Narrative Intelligence Platform

> "Allah is the Light of the heavens and the earth" (Ayat an-Nur, 24:35)

Nour transforms siloed enterprise data into digestible narratives and actionable recommendations, replacing consultants and optimizing sales operations.

## 🚀 Quick Start

```bash
# Clone and setup
git clone <repo>
cd Nour

# Start the platform
make demo

# Access the application
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## 🏗️ Architecture

- **Frontend**: React.js (JavaScript) with modern UI
- **Backend**: Python FastAPI with SQLAlchemy
- **Database**: PostgreSQL with Alembic migrations
- **Storage**: Pluggable adapters (local files, S3, etc.)
- **Security**: Multi-tenant with RBAC

## 📊 Core Features

1. **Data Ingestion**: CSV uploads, API connectors (Salesforce, HubSpot, etc.)
2. **Entity Resolution**: Fuzzy matching and probabilistic linking
3. **Signal Detection**: Automated anomaly and trend detection
4. **Rule Engine**: Configurable business logic in YAML/JSON
5. **Narrative Generation**: AI-powered insights and recommendations
6. **Export & Sharing**: PDF, Markdown, and shareable links

## 🔧 Development

```bash
# Backend development
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend development
cd frontend
npm install
npm run dev

# Database migrations
cd backend
alembic upgrade head
```

## 📚 Documentation

- [Architecture Overview](docs/ARCHITECTURE.md)
- [API Reference](docs/API.md)
- [Demo Guide](docs/DEMO.md)
- [Ontology Schema](docs/ONTOLOGY.md)

## 🎯 MVP Acceptance Criteria

- ✅ Upload 3+ CSVs and ingest into ontology
- ✅ Compute 3+ signals and evaluate 2+ rules
- ✅ Generate 2+ narratives with evidence and actions
- ✅ Export narratives to Markdown
- ✅ Multi-tenant with basic RBAC
- ✅ End-to-end demo in <5 minutes

## 🚧 Roadmap

- [ ] Neo4j graph adapter
- [ ] Streaming connectors (Kafka)
- [ ] LLM-powered summarization
- [ ] Advanced RBAC and audit
- [ ] Playbook automation
