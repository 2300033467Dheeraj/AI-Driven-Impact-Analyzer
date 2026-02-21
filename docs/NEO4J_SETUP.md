# Step-by-Step: Create Neo4j and Load Database

## Step 1: Run Neo4j

### Option A: Docker (recommended)

```bash
docker run -d \
  --name neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password \
  neo4j:5-community
```

- **7474** = Neo4j Browser (web UI)
- **7687** = Bolt (app connections)
- **User:** `neo4j` | **Password:** `password`

### Option B: Docker Compose (with this project)

From project root:

```bash
docker compose up -d neo4j
```

---

## Step 2: Wait for Neo4j to Start

Wait 15–30 seconds, then check:

- **Browser:** http://localhost:7474  
- **Login:** Connect URL `bolt://localhost:7687`, user `neo4j`, password `password`

---

## Step 3: Understand the “Database”

Neo4j 5 has a **default database** named `neo4j`. You are already using it.

- To **create another database** (optional):  
  In Neo4j Browser, run:
  ```cypher
  CREATE DATABASE mydb;
  ```
- To **switch** to it for queries in the Browser:  
  Use the database dropdown and select `mydb`.  
- **This app** uses the default database only; no need to create a new one unless you want to experiment.

---

## Step 4: Create the Service Graph (Load Data)

You need nodes and relationships so the backend can compute blast radius.

### Option A: Run the seed script (easiest)

From the **backend** folder, with Neo4j running and `.env` set:

```bash
cd backend
# If using venv
venv\Scripts\activate
pip install -r requirements.txt

# Seed the default graph
python scripts/seed_neo4j.py
```

You should see: `Neo4j seeded successfully.`

### Option B: Run Cypher in Neo4j Browser

1. Open http://localhost:7474 and connect.
2. In the query box, paste and run:

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
MERGE (a)-[:CALLS]->(n);
```

3. Click **Run**.

---

## Step 5: Verify the Data

In Neo4j Browser, run:

```cypher
MATCH (n:Service)-[r:CALLS]->(m:Service) RETURN n, r, m;
```

You should see a graph: User → Order → Payment, Order → Inventory, Order → Auth, Payment → Notification, Auth → Notification.

---

## Step 6: Point the Backend at Neo4j

In **backend**, create or edit `.env`:

```env
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password
```

If Neo4j runs in Docker and the backend runs on the host, use `localhost`. If both run in Docker Compose, the app already uses `bolt://neo4j:7687`.

---

## Quick Reference

| Step | Action |
|------|--------|
| 1 | Run Neo4j (Docker or `docker compose up -d neo4j`) |
| 2 | Open http://localhost:7474, login `neo4j` / `password` |
| 3 | (Optional) Create another DB with `CREATE DATABASE mydb;` |
| 4 | Load data: `python scripts/seed_neo4j.py` or run the Cypher above in Browser |
| 5 | Verify with the `MATCH` query above |
| 6 | Set `NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD` in backend `.env` |

---

## Database names in this project

- **Default (used by the app):** `neo4j`
- **Creating another database:** `CREATE DATABASE mydb;` in Neo4j Browser (Neo4j 5+). The backend does not use a custom database name; it uses the default.
