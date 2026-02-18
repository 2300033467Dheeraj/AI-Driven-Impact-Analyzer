"""Graph / blast radius API routes."""

from fastapi import APIRouter

from app.models.schemas import BlastRadiusResponse
from app.services.graph_service import get_graph_service

router = APIRouter(tags=["graph"])


@router.get("/service-blast-radius/{service}", response_model=BlastRadiusResponse)
def get_service_blast_radius(service: str) -> BlastRadiusResponse:
    """Compute blast radius for a service using Neo4j BFS traversal.

    Returns downstream impacted services. Uses fallback when Neo4j unavailable.
    """
    graph = get_graph_service()
    return graph.get_blast_radius(service)
