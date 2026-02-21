"""Pydantic schemas for request/response models."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


# Risk Score
DecisionLabel = Literal["approve", "reject", "manual_review"]


class RiskScoreResponse(BaseModel):
    """Response for /risk-score/latest. Frontend expects 'score' and 'decision'."""

    score: float = Field(..., description="Risk score 0-100")
    risk_score: float = Field(..., description="Alias for score")
    decision: DecisionLabel = Field(..., description="approve, reject, or manual_review")
    decision_label: str = Field(..., description="Human-readable decision")
    deployment_id: str | None = None
    timestamp: datetime | None = None


# Metrics
class MetricDataPoint(BaseModel):
    """Single metrics data point."""

    timestamp: str
    latency: float = 0
    error_rate: float = 0
    cpu: float = 0
    memory: float = 0


class MetricsResponse(BaseModel):
    """Response for /metrics. Frontend expects 'data' array."""

    data: list[MetricDataPoint]
    period: str | None = None
    cpu_usage: float | None = None
    memory_usage: float | None = None
    latency: float | None = None
    error_rate: float | None = None


# Blast Radius
class BlastRadiusResponse(BaseModel):
    """Response for /service-blast-radius/{service}."""

    service: str
    impacted_services: list[str]


# Analyze Deployment
class AnalyzeDeploymentRequest(BaseModel):
    """Request for POST /analyze-deployment."""

    files_changed: int = Field(..., ge=0, description="Number of files changed")
    critical_service_modified: bool = Field(
        ..., description="Whether a critical service was modified"
    )
    dependency_depth: int = Field(..., ge=0, description="Depth of dependency tree")


class AnalyzeDeploymentResponse(BaseModel):
    """Response for POST /analyze-deployment."""

    risk_score: float
    decision: DecisionLabel
    decision_label: str
    deployment_id: str
    features_used: dict[str, float] | None = None


# GitHub Webhook
class GitHubCommitAuthor(BaseModel):
    """GitHub commit author."""

    name: str | None = None
    email: str | None = None


class GitHubCommit(BaseModel):
    """GitHub commit payload."""

    id: str | None = None
    message: str | None = None
    author: GitHubCommitAuthor | None = None
    added: list[str] = []
    removed: list[str] = []
    modified: list[str] = []


class GitHubRepository(BaseModel):
    """GitHub repository info."""

    name: str | None = None
    full_name: str | None = None


class GitHubWebhookPayload(BaseModel):
    """GitHub webhook payload (push event)."""

    ref: str | None = None
    commits: list[GitHubCommit] = []
    repository: GitHubRepository | None = None
    head_commit: GitHubCommit | None = None


# Manual data: add deployment
class AddDeploymentRequest(BaseModel):
    """Request for POST /deployments (manually add a deployment)."""

    service_name: str = Field(..., min_length=1)
    risk_score: float = Field(..., ge=0, le=100)
    decision: DecisionLabel = Field(...)
    status: Literal["success", "failed", "pending"] = "pending"


# Manual data: add service dependency (Neo4j graph)
class AddServiceLinkRequest(BaseModel):
    """Request for POST /service-graph/link (add CALLS relationship)."""

    from_service: str = Field(..., min_length=1, description="Caller service name")
    to_service: str = Field(..., min_length=1, description="Callee service name")
