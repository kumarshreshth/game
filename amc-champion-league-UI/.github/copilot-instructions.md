# Copilot Coding Agent Onboarding Guide

Trust these instructions first. Only search the repository if information here is missing or provably incorrect.

Overview
- Purpose: FastAPI starter kit for building production-grade REST APIs with a clean architecture, database migrations, tests, linting, and containerized local dev.
- Stack: Python 3.10+ (prefer 3.11/3.12), FastAPI + Uvicorn, SQLAlchemy + Alembic, PostgreSQL (via Docker Compose), Pytest + Coverage, Pre-commit (format/lint), Mypy (types), MkDocs (docs).
- Data modeling & validation: Pydantic (v2 recommended) for request/response schemas and settings; SQLAlchemy for persistence models.

High-signal layout (common paths)
- app/: application code
  - app/routers/: FastAPI APIRouter layer (HTTP surface)
  - app/controllers/ or app/services/: business logic/service layer (no DB direct access)
  - app/crud/: data-access layer (SQLAlchemy sessions/queries only)
  - app/schemas/: Pydantic models for request/response DTOs
  - app/models/: SQLAlchemy ORM models and metadata
  - app/core/ or app/config/: settings, security, DI helpers
  - app/main.py: FastAPI app factory/instance and router wiring
- migration/ or migrations/: Alembic environment and versioned migrations (alembic.ini in root)
- tests/: pytest test suite mirrors app/ layout (routers/controllers/crud/schemas)
- .github/workflows/: CI pipelines (lint, type-check, tests, coverage, image build)
- Config at repo root (examples): pyproject.toml, pytest.ini, mypy.ini, .coveragerc, .pre-commit-config.yaml, Dockerfile, docker-compose.yml, mkdocs.yml, requirements*.txt or uv.lock.

Architecture conventions (follow strictly)
- Layering: routes → controllers/services → crud/data-access.
  - Routes (FastAPI routers): parse/validate inputs with Pydantic, call a controller, return Pydantic responses only. No SQLAlchemy session logic here.
  - Controllers/services: orchestrate business rules; no direct HTTP or DB specifics beyond calling crud and assembling results. Keep functions small and SRP-compliant.
  - CRUD: isolated data-access functions using SQLAlchemy sessions/queries; no business logic.
- SRP and separation of concerns: one reason to change per function/module; extract helpers rather than mixing responsibilities.
- Pydantic usage:
  - Define request/response schemas in app/schemas/*.py using Pydantic models.
  - Validate inputs/outputs at the edges (router signatures and response_model).
  - Prefer immutable DTOs for responses (model_config = {"frozen": True}) when applicable.
- Dependency Injection: prefer FastAPI Depends for DB sessions and settings providers.
- Error handling: raise HTTPException from routers only; controllers/crud raise domain/data exceptions mapped at router boundary.

Environment setup (choose one path and stick with it per session)
A) pip + venv
1) python -m venv .venv && source .venv/bin/activate  (Windows: .venv\Scripts\activate)
2) pip install -U pip setuptools wheel
3) pip install -r requirements.txt
4) pip install -r requirements-dev.txt  (tools: pytest, mypy, linters, pre-commit)
5) pre-commit install && pre-commit run -a  (fix and re-run until clean)

B) uv (if present)
1) uv sync --dev
2) uv run pre-commit install
3) uv run pre-commit run -a

Database and migrations
- If using Docker for Postgres: docker compose up -d db and wait for health.
- Apply migrations before running the app: alembic upgrade head (or uv run alembic upgrade head).
- When changing models: alembic revision --autogenerate -m "<message>" then alembic upgrade head.

Run the application
- Local dev: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
- Verify OpenAPI docs: http://localhost:8000/docs
- Docker: docker compose up --build -d (then docker compose logs -f app)

Quality gates (run before commit and push)
- Formatting/linting/types:
  - pre-commit run -a
  - mypy .  (or via pre-commit)
- Tests with 100% coverage required (enforce locally):
  - pytest --maxfail=1 -q
  - pytest --cov=app --cov-report=term-missing --cov-fail-under=100
  - If coverage < 100%, add/adjust tests; mirror tests to routers/controllers/crud for every code path, including error branches.
- Migrations: alembic upgrade head must succeed on a clean database.
- Container build smoke: docker compose build should succeed.

Testing guidance
- Place tests under tests/ mirroring app/ structure: tests/routers, tests/controllers, tests/crud, tests/schemas.
- Use FastAPI TestClient for router tests; unit-test controllers and crud in isolation; use factories/fixtures for DB objects.
- Prefer deterministic tests; isolate time/UUID with injectable providers.

CI expectations
- Workflows in .github/workflows typically run: pre-commit, mypy, pytest with coverage, and Docker build. Local runs above should pass to avoid CI failures.

Change checklist for PRs
- Code placed in correct layer (routes/controllers/crud) and follows SRP.
- New/changed endpoints have Pydantic request/response schemas.
- Tests added/updated with 100% coverage locally.
- pre-commit, mypy, pytest, alembic upgrade head, and docker compose build all pass locally.

Common pitfalls
- Mixing layers: keep HTTP concerns in routers, business rules in controllers, and DB calls in crud only.
- Missing .env or DB not ready: ensure .env is created (copy from .env.example) and Postgres is running before migrations/tests.
- Tooling mismatch: do not mix pip/venv and uv within the same environment.

Final note for Copilot Agent
- Prefer documented commands and existing scripts over ad-hoc shell.
- Minimize changes; keep diffs focused and include tests/migrations alongside code.
- Trust this guide first; only search if a step here is missing or fails.
