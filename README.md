# k8s-helm-bookstore

[![CI](https://github.com/Djones-qa/k8s-helm-bookstore/actions/workflows/ci.yml/badge.svg)](https://github.com/Djones-qa/k8s-helm-bookstore/actions/workflows/ci.yml)
[![Docker](https://img.shields.io/badge/docker-ghcr.io-2496ED?logo=docker&logoColor=white)](https://github.com/Djones-qa/k8s-helm-bookstore/pkgs/container/k8s-helm-bookstore)
[![Python](https://img.shields.io/badge/python-3.12-blue?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

A production-grade Kubernetes deployment project for a FastAPI microservice. Demonstrates Helm chart authoring, Kustomize overlays, Kubernetes health probes, HPA, Prometheus metrics, and a CI/CD pipeline that builds and publishes to GHCR.

---

## What this project demonstrates

| Skill | Implementation |
|-------|---------------|
| Helm chart authoring | Parameterised chart with helpers, probes, HPA, Ingress, security contexts |
| Multi-environment config | `values-dev.yaml` / `values-prod.yaml` + Kustomize overlays |
| Kubernetes health probes | `/health/live` (liveness) and `/health/ready` (readiness) |
| Horizontal Pod Autoscaler | CPU-based HPA, configurable min/max replicas |
| Prometheus metrics | `/metrics` via `prometheus-fastapi-instrumentator` |
| Pod security | Non-root user, read-only filesystem, dropped capabilities |
| CI/CD pipeline | Lint -> Test -> Helm lint -> Docker build -> Publish to GHCR |
| Container registry | Automatic image publish to GHCR on every merge to master |

---

## Project structure

```
k8s-helm-bookstore/
├── app/                          # FastAPI application
│   ├── main.py                   # App entry point + k8s probe endpoints
│   ├── config.py                 # Pydantic settings
│   └── routers/books.py          # In-memory CRUD
├── helm/bookstore/               # Helm chart
│   ├── Chart.yaml
│   ├── values.yaml               # Default values
│   ├── values-dev.yaml           # Development overrides (1 replica)
│   ├── values-prod.yaml          # Production overrides (3 replicas, HPA, TLS)
│   └── templates/
│       ├── _helpers.tpl
│       ├── deployment.yaml
│       ├── service.yaml
│       ├── ingress.yaml
│       ├── hpa.yaml
│       └── NOTES.txt
├── k8s/                          # Raw manifests (Kustomize)
│   ├── base/
│   └── overlays/
│       ├── dev/
│       └── prod/
├── tests/
│   ├── conftest.py
│   ├── test_health.py            # Liveness, readiness, metrics probes
│   └── test_books.py             # CRUD integration tests
├── .github/workflows/ci.yml
├── Dockerfile
├── Makefile
└── pyproject.toml
```

---

## Quick start

```bash
git clone https://github.com/Djones-qa/k8s-helm-bookstore.git
cd k8s-helm-bookstore
make dev        # install deps + copy .env
make run        # start API at http://localhost:8000
```

Endpoints:
- `http://localhost:8000/docs` — Swagger UI
- `http://localhost:8000/health/live` — liveness probe
- `http://localhost:8000/health/ready` — readiness probe
- `http://localhost:8000/metrics` — Prometheus metrics

### Run tests

```bash
make test
```

---

## Helm deployment

### Lint the chart

```bash
make helm-lint
```

### Deploy to a local cluster

```bash
# Dev
helm upgrade --install bookstore helm/bookstore/ \
  -f helm/bookstore/values-dev.yaml \
  --namespace bookstore-dev --create-namespace

# Prod
helm upgrade --install bookstore helm/bookstore/ \
  -f helm/bookstore/values-prod.yaml \
  --namespace bookstore-prod --create-namespace
```

### Port-forward and verify

```bash
kubectl port-forward svc/bookstore-bookstore 8000:80 -n bookstore-dev
curl http://localhost:8000/health/ready
```

---

## Kustomize deployment

```bash
# Dev
kubectl apply -k k8s/overlays/dev/

# Prod
kubectl apply -k k8s/overlays/prod/
```

---

## CI/CD pipeline

Every push to `master` runs:

```
lint -> test -> helm-lint -> docker -> all-checks gate
                                            |
                                       publish (master only)
                                       ghcr.io tags: sha-<commit>, latest
```

---

## Kubernetes concepts covered

### Health probes

```yaml
livenessProbe:
  httpGet:
    path: /health/live
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 15
readinessProbe:
  httpGet:
    path: /health/ready
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 10
```

### Horizontal Pod Autoscaler

```yaml
autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
```

### Pod security context

```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  allowPrivilegeEscalation: false
  readOnlyRootFilesystem: true
  capabilities:
    drop: [ALL]
```

### Prometheus scraping

```yaml
annotations:
  prometheus.io/scrape: "true"
  prometheus.io/path: /metrics
  prometheus.io/port: "8000"
```

---

## License

MIT
