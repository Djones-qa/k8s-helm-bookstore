"""
Bookstore API - production-ready FastAPI app instrumented for Kubernetes.

Exposes:
  /health/live   - liveness probe  (is the process alive?)
  /health/ready  - readiness probe (is the app ready to serve traffic?)
  /metrics       - Prometheus metrics (via prometheus-fastapi-instrumentator)
  /books         - simple in-memory CRUD used to demo the deployment
"""

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from app.config import get_settings
from app.routers import books

settings = get_settings()


def create_app() -> FastAPI:
    application = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
    )
    application.include_router(books.router)

    # instrument() must be called before the app starts so middleware is added
    # while the stack is still mutable; expose() registers the /metrics route.
    Instrumentator().instrument(application).expose(application)

    return application


app = create_app()


@app.get("/health/live", tags=["health"], summary="Liveness probe")
def liveness():
    """Returns 200 while the process is running."""
    return {"status": "alive"}


@app.get("/health/ready", tags=["health"], summary="Readiness probe")
def readiness():
    """Returns 200 when the app is ready to serve traffic."""
    return {"status": "ready", "version": settings.app_version}


@app.get("/", tags=["root"])
def root():
    return {"message": f"Welcome to {settings.app_name}", "docs": "/docs"}
