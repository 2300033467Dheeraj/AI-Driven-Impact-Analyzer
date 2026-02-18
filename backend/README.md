# AI-Driven Impact Analyzer - Backend

FastAPI backend for cloud-native deployment risk analysis. Integrates with the Next.js frontend at http://localhost:3000.

## Tech Stack

- **Python 3.11+**
- **FastAPI**
- **Pydantic**
- **Scikit-learn** (RandomForest)
- **Neo4j** (bolt driver)
- **Uvicorn**
- **Structlog** (JSON structured logging)

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/risk-score/latest` | Latest risk score and decision |
| GET | `/metrics` | Simulated Prometheus-style metrics |
| GET | `/service-blast-radius/{service}` | Blast radius via Neo4j BFS |
| POST | `/analyze-deployment` | ML-based risk prediction |
| POST | `/webhook/github` | GitHub push webhook → risk analysis |

## Configuration

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

| Variable | Default | Description |
|----------|---------|-------------|
| MODEL_PATH | app/ml/model.joblib | Path to trained model |
| NEO4J_URI | bolt://localhost:7687 | Neo4j connection URI |
| NEO4J_USER | neo4j | Neo4j user |
| NEO4J_PASSWORD | password | Neo4j password |
| LOG_LEVEL | INFO | Log level |

## Local Run

**Note:** On Windows with Python 3.13, scikit-learn may fail to install (requires MSVC). The backend falls back to a heuristic risk calculator and runs without ML. For full ML support, use Python 3.11 or 3.12, or Docker.

### 1. Virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Train model

```bash
python scripts/train_model.py
```

### 4. (Optional) Seed Neo4j

If Neo4j is running:

```bash
python scripts/seed_neo4j.py
```

### 5. Start server

```bash
python -m uvicorn app.main:app --reload
```

Backend: http://localhost:8000  
Docs: http://localhost:8000/docs

## Testing

Run all API tests (no server needed):

```bash
pip install -r requirements.txt
pytest tests/ -v
```

Tests cover: `/`, `/health`, `/risk-score/latest`, `/metrics`, `/service-blast-radius/{service}`, `/analyze-deployment`, `/deployments`, `/webhook/github`.

## Docker

```bash
docker build -t impact-analyzer-backend .
docker run -p 8000:8000 impact-analyzer-backend
```

## Neo4j Graph

Default service graph (seeded by `scripts/seed_neo4j.py`):

```
(User)-[:CALLS]->(Order)
(Order)-[:CALLS]->(Payment)
(Order)-[:CALLS]->(Inventory)
(Order)-[:CALLS]->(Auth)
(Payment)-[:CALLS]->(Notification)
(Auth)-[:CALLS]->(Notification)
```

Blast radius is computed via BFS traversal from the given service. If Neo4j is unavailable, a fallback mock graph is used.

## ML Model

- **RandomForestClassifier**
- Features: `files_changed`, `critical_service_modified`, `dependency_depth`, `cpu_usage`, `latency`, `error_rate`
- Target: 0 (low), 1 (medium), 2 (high risk)
- Decision mapping: 0–30 Normal (approve), 30–60 Canary (manual_review), 60–100 Manual Approval (manual_review)
