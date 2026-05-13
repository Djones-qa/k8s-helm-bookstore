"""Tests for Kubernetes health probe endpoints."""


class TestLivenessProbe:
    def test_liveness_returns_200(self, client):
        response = client.get("/health/live")
        assert response.status_code == 200

    def test_liveness_body(self, client):
        data = client.get("/health/live").json()
        assert data["status"] == "alive"


class TestReadinessProbe:
    def test_readiness_returns_200(self, client):
        response = client.get("/health/ready")
        assert response.status_code == 200

    def test_readiness_body(self, client):
        data = client.get("/health/ready").json()
        assert data["status"] == "ready"
        assert "version" in data


class TestMetricsEndpoint:
    def test_metrics_returns_200(self, client):
        response = client.get("/metrics")
        assert response.status_code == 200

    def test_metrics_content_type(self, client):
        response = client.get("/metrics")
        assert "text/plain" in response.headers["content-type"]