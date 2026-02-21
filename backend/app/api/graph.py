"""Graph / blast radius API routes."""

from fastapi import APIRouter, HTTPException

from app.models.schemas import AddServiceLinkRequest, BlastRadiusResponse
from app.services.graph_service import get_graph_service

router = APIRouter(tags=["graph"])


@router.get("/service-blast-radius/{service}", response_model=BlastRadiusResponse)
def get_service_blast_radius(service: str) -> BlastRadiusResponse:
    """Compute blast radius for a service using Neo4j BFS traversal.

    Returns downstream impacted services. Uses fallback when Neo4j unavailable.
    """
    graph = get_graph_service()
    return graph.get_blast_radius(service)


@router.post("/service-graph/link")
def add_service_link(request: AddServiceLinkRequest):
    """Manually add a service dependency: from_service CALLS to_service.

    Requires Neo4j. Creates both services if they do not exist.
    """
    graph = get_graph_service()
    if graph.add_service_link(request.from_service, request.to_service):
        return {
            "message": "Link added",
            "from_service": request.from_service,
            "to_service": request.to_service,
        }
    raise HTTPException(
        status_code=503,
        detail="Neo4j unavailable. Start Neo4j and try again.",
    )
