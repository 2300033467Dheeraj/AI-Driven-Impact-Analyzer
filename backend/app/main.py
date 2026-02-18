"""FastAPI application entrypoint."""

import json
import sys
from contextlib import asynccontextmanager
from pathlib import Path

import structlog
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api.deployments import router as deployments_router
from app.api.graph import router as graph_router
from app.api.metrics import router as metrics_router
from app.api.risk import router as risk_router
from app.api.webhook import router as webhook_router
from app.config import get_settings
from app.dependencies import get_risk_predictor
from app.services.graph_service import get_graph_service

# Add project root for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
)

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup/shutdown lifecycle."""
    settings = get_settings()
    # Load ML model at startup
    try:
        get_risk_predictor()
        path = settings.model_path_resolved
        logger.info("ml_model_loaded", path=str(path), exists=path.exists())
    except Exception as e:
        logger.warning(
            "ml_model_load_failed", error=str(e), path=str(settings.model_path_resolved)
        )
    # Seed Neo4j if available
    try:
        graph = get_graph_service()
        if graph.seed_default_graph():
            logger.info("neo4j_seed_success")
        else:
            logger.info("neo4j_unavailable_using_fallback")
    except Exception as e:
        logger.info("neo4j_seed_skipped", error=str(e))
    yield
    graph = get_graph_service()
    graph.close()


app = FastAPI(
    title="AI-Driven Impact Analyzer",
    description="Backend for cloud-native deployment risk analysis",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests."""
    response = await call_next(request)
    log_data = {
        "method": request.method,
        "path": request.url.path,
        "status": response.status_code,
    }
    logger.info("request", **log_data)
    return response


# Include routers
app.include_router(risk_router)
app.include_router(metrics_router)
app.include_router(graph_router)
app.include_router(deployments_router)
app.include_router(webhook_router)


@app.get("/")
def root():
    """Health check."""
    return {"status": "ok", "service": "impact-analyzer"}


@app.get("/health")
def health():
    """Health endpoint for probes."""
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
