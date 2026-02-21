# How to Manually Add Backend Data

This guide explains how to add data manually to the backend: **deployments** and **service graph (Neo4j)**.

---

## 1. Manually Add Deployments

Deployments are stored in memory (lost when the server restarts). You can add them via the API.

### Option A: Using the API (POST)

**Endpoint:** `POST http://localhost:8000/deployments`

**Body (JSON):**
```json
{
  "service_name": "order-service",
  "risk_score": 45,
  "decision": "manual_review",
  "status": "pending"
}
```

| Field          | Type   | Required | Description |
|----------------|--------|----------|-------------|
| `service_name` | string | Yes      | Name of the deployed service |
| `risk_score`  | number | Yes      | 0–100 |
| `decision`    | string | Yes      | `approve`, `reject`, or `manual_review` |
| `status`      | string | No       | `success`, `failed`, or `pending` (default: `pending`) |

**Example (PowerShell):**
```powershell
Invoke-RestMethod -Uri http://localhost:8000/deployments -Method Post -ContentType "application/json" -Body '{"service_name":"order-service","risk_score":45,"decision":"manual_review","status":"pending"}'
```

**Example (curl):**
```bash
curl -X POST http://localhost:8000/deployments \
  -H "Content-Type: application/json" \
  -d "{\"service_name\":\"order-service\",\"risk_score\":45,\"decision\":\"manual_review\",\"status\":\"pending\"}"
```

**Get all deployments:** `GET http://localhost:8000/deployments`  
Manually added deployments appear first; then mock data. The frontend **Deployments** page uses this.

---

## 2. Manually Add Service Graph Data (Neo4j)

The **blast radius** is computed from the **service dependency graph** in Neo4j. You can add nodes (services) and edges (who calls whom) in two ways.

### Option A: Using the API (POST)

**Endpoint:** `POST http://localhost:8000/service-graph/link`

**Body (JSON):**
```json
{
  "from_service": "Order",
  "to_service": "Shipping"
}
```

This creates two services (`Order`, `Shipping`) if they do not exist, and adds a **CALLS** relationship: `Order` → `Shipping`.

**Example (PowerShell):**
```powershell
Invoke-RestMethod -Uri http://localhost:8000/service-graph/link -Method Post -ContentType "application/json" -Body '{"from_service":"Order","to_service":"Shipping"}'
```

**Example (curl):**
```bash
curl -X POST http://localhost:8000/service-graph/link \
  -H "Content-Type: application/json" \
  -d "{\"from_service\":\"Order\",\"to_service\":\"Shipping\"}"
```

Neo4j must be running. After adding links, use **GET** `http://localhost:8000/service-blast-radius/Order` or the frontend **Services** page to see blast radius.

### Option B: Using Neo4j Browser (Cypher)

1. Start Neo4j (e.g. `docker run -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password neo4j:5-community`).
2. Open **http://localhost:7474**, log in (neo4j / password).
3. Run Cypher in the query box.

**Create a single service:**
```cypher
MERGE (s:Service {name: 'Shipping'})
```

**Create two services and a CALLS link:**
```cypher
MERGE (a:Service {name: 'Order'})
MERGE (b:Service {name: 'Shipping'})
MERGE (a)-[:CALLS]->(b)
```

**Add more links (services already exist):**
```cypher
MERGE (a:Service {name: 'Shipping'})
MERGE (b:Service {name: 'Notification'})
MERGE (a)-[:CALLS]->(b)
```

**Seed the full default graph (same as the seed script):**
```cypher
MERGE (u:Service {name: 'User'})
MERGE (o:Service {name: 'Order'})
MERGE (p:Service {name: 'Payment'})
MERGE (n:Service {name: 'Notification'})
MERGE (a:Service {name: 'Auth'})
MERGE (i:Service {name: 'Inventory'})
MERGE (u)-[:CALLS]->(o)
MERGE (o)-[:CALLS]->(p)
MERGE (o)-[:CALLS]->(i)
MERGE (p)-[:CALLS]->(n)
MERGE (o)-[:CALLS]->(a)
MERGE (a)-[:CALLS]->(n)
```

**List all services:**
```cypher
MATCH (s:Service) RETURN s.name ORDER BY s.name
```

**List all CALLS relationships:**
```cypher
MATCH (a:Service)-[r:CALLS]->(b:Service) RETURN a.name, b.name
```

---

## 3. Seed Script (Default Graph)

To load the **default** service graph (User, Order, Payment, Notification, Auth, Inventory and their links) from the backend:

```bash
cd backend
python scripts/seed_neo4j.py
```

Neo4j must be running at `bolt://localhost:7687` with user `neo4j` and password `password` (or set `NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD` in `.env`).

---

## Summary

| Data              | How to add manually |
|-------------------|----------------------|
| **Deployments**   | `POST /deployments` with JSON body (in-memory; lost on restart). |
| **Service links** | `POST /service-graph/link` with `from_service`, `to_service` (Neo4j). |
| **Service graph** | Neo4j Browser: run Cypher `MERGE` for nodes and `MERGE (a)-[:CALLS]->(b)`. |
| **Default graph** | Run `python scripts/seed_neo4j.py` (Neo4j must be up). |

API docs: **http://localhost:8000/docs** (try the endpoints from there).
