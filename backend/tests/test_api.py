"""API tests using FastAPI TestClient."""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    """Health check at /"""
    r = client.get("/")
    assert r.status_code == 200
    data = r.json()
    assert data.get("status") == "ok"
    assert "impact-analyzer" in data.get("service", "")


def test_health():
    """Health endpoint"""
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json().get("status") == "healthy"


def test_risk_score_latest():
    """GET /risk-score/latest returns score and decision"""
    r = client.get("/risk-score/latest")
    assert r.status_code == 200
    data = r.json()
    assert "score" in data
    assert "risk_score" in data
    assert data["decision"] in ("approve", "reject", "manual_review")
    assert 0 <= data["score"] <= 100


def test_metrics():
    """GET /metrics returns data array for frontend"""
    r = client.get("/metrics")
    assert r.status_code == 200
    data = r.json()
    assert "data" in data
    assert isinstance(data["data"], list)
    if data["data"]:
        point = data["data"][0]
        assert "timestamp" in point
        assert "latency" in point
        assert "cpu" in point
        assert "memory" in point


def test_service_blast_radius():
    """GET /service-blast-radius/{service} returns impacted services"""
    r = client.get("/service-blast-radius/Order")
    assert r.status_code == 200
    data = r.json()
    assert data["service"] == "Order"
    assert "impacted_services" in data
    assert isinstance(data["impacted_services"], list)


def test_analyze_deployment():
    """POST /analyze-deployment returns risk score and decision"""
    r = client.post(
        "/analyze-deployment",
        json={
            "files_changed": 5,
            "critical_service_modified": True,
            "dependency_depth": 3,
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert "risk_score" in data
    assert data["decision"] in ("approve", "reject", "manual_review")
    assert "deployment_id" in data


def test_deployments():
    """GET /deployments returns list"""
    r = client.get("/deployments")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)


def test_webhook_github():
    """POST /webhook/github accepts payload"""
    r = client.post(
        "/webhook/github",
        json={
            "ref": "refs/heads/main",
            "commits": [],
            "head_commit": {
                "id": "abc",
                "message": "test",
                "added": ["src/auth.py"],
                "modified": [],
                "removed": [],
            },
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert "risk_score" in data
    assert "decision" in data
