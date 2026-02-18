"""Seed Neo4j with default service dependency graph.

Run: python scripts/seed_neo4j.py

Requires Neo4j running at NEO4J_URI (default bolt://localhost:7687).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.services.graph_service import get_graph_service


def main() -> None:
    graph = get_graph_service()
    if graph.seed_default_graph():
        print("Neo4j seeded successfully.")
        print("Graph: User->Order->(Payment,Inventory,Auth); Payment->Notification; Auth->Notification")
    else:
        print("Neo4j unavailable. Ensure Neo4j is running at bolt://localhost:7687")


if __name__ == "__main__":
    main()
