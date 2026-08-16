.PHONY: install lint typecheck test test-integration audit docs compose-up compose-down seed

install:
	poetry install --with dev,docs
	poetry run pre-commit install

lint:
	poetry run ruff check retroville tests
	poetry run ruff format --check retroville tests

typecheck:
	poetry run mypy retroville/matching/domain.py retroville/matching/services.py retroville/providers retroville/health retroville/observability.py

test:
	poetry run pytest tests/unit tests/characterisation --cov=retroville --cov-report=term-missing --cov-fail-under=55

test-integration:
	poetry run pytest tests/integration -m integration --ds=retroville.settings.integration

audit:
	poetry run pip-audit --cache-dir ./.cache/pip-audit

sbom:
	docker build -t retroville-api:local .
	docker run --rm aquasec/trivy:latest image --format cyclonedx retroville-api:local

docs:
	poetry run mkdocs build --strict

compose-up:
	docker compose up --build

compose-down:
	docker compose down -v

seed:
	docker compose exec web python manage.py seed_demo
