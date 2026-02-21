"""Neo4j graph service for blast radius computation."""

from contextlib import contextmanager
from typing import Generator

from neo4j import GraphDatabase, Driver
from neo4j.exceptions import ServiceUnavailable

from app.config import get_settings
from app.models.schemas import BlastRadiusResponse


class GraphService:
    """Neo4j service for service dependency graph."""

    def __init__(self) -> None:
        settings = get_settings()
        self._uri = settings.neo4j_uri
        self._user = settings.neo4j_user
        self._password = settings.neo4j_password
        self._driver: Driver | None = None

    def _get_driver(self) -> Driver | None:
        """Lazy driver initialization."""
        if self._driver is None:
            try:
                self._driver = GraphDatabase.driver(
                    self._uri,
                    auth=(self._user, self._password),
                )
                self._driver.verify_connectivity()
            except (ServiceUnavailable, Exception):
                self._driver = None
        return self._driver

    @contextmanager
    def session(self) -> Generator:
        """Context manager for Neo4j session."""
        driver = self._get_driver()
        if driver is None:
            yield None
            return
        with driver.session() as s:
            yield s

    def get_blast_radius(self, service: str) -> BlastRadiusResponse:
        """Compute blast radius using BFS traversal.

        From service S, find all services reachable via CALLS relationship
        (downstream dependencies).
        """
        driver = self._get_driver()
        if driver is None:
            # Fallback when Neo4j unavailable
            return _fallback_blast_radius(service)

        with driver.session() as session:
            # BFS: start from service, follow CALLS edges
            result = session.run(
                """
                MATCH (s:Service {name: $service})-[:CALLS*1..]->(downstream:Service)
                RETURN DISTINCT downstream.name AS name
                ORDER BY name
                """,
                service=service,
            )
            impacted = [record["name"] for record in result if record["name"]]

        return BlastRadiusResponse(service=service, impacted_services=impacted)

    def seed_default_graph(self) -> bool:
        """Seed default service graph. Returns True on success."""
        driver = self._get_driver()
        if driver is None:
            return False

        with driver.session() as session:
            session.run(
                """
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
                """
            )
        return True

    def add_service_link(self, from_service: str, to_service: str) -> bool:
        """Manually add a CALLS link: from_service -> to_service. Returns True on success."""
        driver = self._get_driver()
        if driver is None:
            return False
        with driver.session() as session:
            session.run(
                """
                MERGE (a:Service {name: $from_service})
                MERGE (b:Service {name: $to_service})
                MERGE (a)-[:CALLS]->(b)
                """,
                from_service=from_service,
                to_service=to_service,
            )
        return True

    def close(self) -> None:
        """Close driver."""
        if self._driver:
            self._driver.close()
            self._driver = None


def _fallback_blast_radius(service: str) -> BlastRadiusResponse:
    """Return fallback blast radius when Neo4j is unavailable."""
    # Static mock graph: User->Order->Payment->Notification, Order->Auth->Notification
    graph: dict[str, list[str]] = {
        "User": ["Order"],
        "Order": ["Payment", "Inventory", "Auth"],
        "Payment": ["Notification"],
        "Auth": ["Notification"],
        "Inventory": [],
        "Notification": [],
    }
    # Map common service names (e.g. order-service, auth) to graph nodes
    name_map: dict[str, str] = {
        "user": "User",
        "order": "Order",
        "payment": "Payment",
        "notification": "Notification",
        "auth": "Auth",
        "inventory": "Inventory",
        "order-service": "Order",
        "payment-gateway": "Payment",
        "auth-service": "Auth",
        "notification-service": "Notification",
        "user-profile-api": "User",
    }
    key = service.lower().replace("_", "-").strip()
    node = name_map.get(key) or service.replace("-", " ").title()
    downstream: list[str] = []
    if node in graph:
        downstream = _bfs(graph, node)

    if not downstream:
        downstream = ["auth-service", "payment-gateway", "notification-service"]

    return BlastRadiusResponse(service=service, impacted_services=downstream)


def _bfs(graph: dict[str, list[str]], start: str) -> list[str]:
    """BFS to collect all downstream services."""
    visited: set[str] = set()
    queue = [start]
    result: list[str] = []

    while queue:
        node = queue.pop(0)
        if node in visited:
            continue
        visited.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                result.append(neighbor)
                queue.append(neighbor)

    return result


# Singleton for FastAPI
_graph_service: GraphService | None = None


def get_graph_service() -> GraphService:
    """Get or create graph service instance."""
    global _graph_service
    if _graph_service is None:
        _graph_service = GraphService()
    return _graph_service
