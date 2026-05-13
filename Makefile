.PHONY: help install dev run test lint format typecheck docker-build clean

help:
@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install production dependencies
pip install -r requirements.txt

dev: ## Install all dependencies
pip install -r requirements.txt -r requirements-dev.txt
cp -n .env.example .env || true

run: ## Start the API server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test: ## Run tests
pytest tests/ -v

lint: ## Run ruff linter
ruff check .

format: ## Auto-format with ruff
ruff format .

typecheck: ## Run mypy
mypy app/ --ignore-missing-imports

docker-build: ## Build Docker image
docker build -t bookstore:local .

helm-lint: ## Lint Helm chart
helm lint helm/bookstore/
helm lint helm/bookstore/ -f helm/bookstore/values-dev.yaml
helm lint helm/bookstore/ -f helm/bookstore/values-prod.yaml

helm-template: ## Dry-run Helm template render
helm template bookstore helm/bookstore/ -f helm/bookstore/values-prod.yaml

clean: ## Remove generated files
find . -type f -name "*.pyc" -delete
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
rm -rf reports .pytest_cache