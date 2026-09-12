# Developer Guide: Sovereign Sales Agent RAG

## Prerequisites

| Requirement | Minimum Version | Notes |
|-------------|----------------|-------|
| Python | 3.10+ | 3.11 recommended |
| Docker | 24+ | For containerized dev |
| docker-compose | v2+ | |
| n8n | 1.90+ | Command Center must be running |

## Quick Start

```bash
# 1. Clone
git clone https://github.com/BlackFoxgamingstudio/sales-agent-rag.git
cd sales-agent-rag

# 2. Environment
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env   # then edit .env

# 3. Run tests
python -m pytest tests/ -v

# 4. Start service
python src/core.py

# 5. Verify
curl http://localhost:8802/health
```

## Environment Configuration

```bash
export SBB_VECTOR_DB_URL=your_value_here
export SBB_LLM_API_KEY=your_value_here
export SBB_CRM_API_KEY=your_value_here
export SBB_PRODUCT_CATALOG_PATH=your_value_here

# Always required
SBB_API_KEY=change-me-in-production
SBB_N8N_EVENT_BUS_URL=http://localhost:5678/webhook/event-bus
LOG_LEVEL=INFO
```

---

## Project Structure

```
sales-agent-rag/
├── src/
│   ├── __init__.py          # Package root
│   ├── core.py              # FastAPI entrypoint + dispatcher
│   ├── cli.py               # Typer CLI (sovereign-sales-agent-rag)
│   ├── models.py            # Pydantic request/response models
│   └── ...                  # Component modules
├── tests/
│   ├── __init__.py
│   └── test_solution.py     # Unit + integration tests
├── docs/
│   ├── ARCHITECTURE.md      # System design
│   ├── DEVELOPER_GUIDE.md   # This file
│   ├── SME_PLAYBOOK.md      # Domain expert reference
│   └── SOP.md               # Operational procedures
├── n8n/
│   ├── workflow.json        # n8n workflow definition
│   └── webhook_adapter.py   # Standalone webhook adapter
├── templates/               # Domain-specific config templates
├── .github/workflows/
│   └── ci.yml               # GitHub Actions (Python 3.10/3.11/3.12)
├── Dockerfile               # Multistage, non-root user
├── docker-compose.yml       # Platform network integration
├── pyproject.toml           # PEP 518 packaging
├── .env.example             # Environment template
├── CHANGELOG.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
└── SECURITY.md
```

---

## Testing

```bash
# Full suite
python -m pytest tests/ -v --tb=short

# With HTML coverage report
python -m pytest tests/ --cov=src --cov-report=html
open htmlcov/index.html

# Single test
python -m pytest tests/test_solution.py::TestCore::test_health -v
```

### Test Conventions

- Tests inherit from `unittest.TestCase` (no external test framework needed)
- Each component has a dedicated test class
- Mock all external HTTP calls with `unittest.mock.patch`
- Health tests must always pass without any env vars set

## Code Quality

```bash
# Lint (ruff is fast, replaces flake8+isort+pyupgrade)
pip install ruff
ruff check src/ tests/

# Format
ruff format src/ tests/

# Type check
pip install mypy
mypy src/ --ignore-missing-imports
```

## Docker Workflow

```bash
# Build
docker build -t sovereign-sales-agent-rag:dev .

# Run with env file
docker run --env-file .env -p 8802:8802 sovereign-sales-agent-rag:dev

# Full stack (with n8n network)
docker-compose up --build

# Logs
docker-compose logs -f sovereign-sales-agent-rag

# Health check
curl http://localhost:8802/health
```

## n8n Integration

### Triggering via n8n Custom Node

1. In n8n, open any workflow
2. Search for **"Sovereign"** in the node palette
3. Use **SovereignTools** node → configure endpoint to `http://localhost:8802`

### Triggering Directly

```bash
curl -X POST http://localhost:8802/api/v1/execute \
  -H "Content-Type: application/json" \
  -H "X-SBB-API-Key: $SBB_API_KEY" \
  -d '{"action": "health_ping", "payload": {}}'
```

### Event Bus Integration

The service auto-emits structured events to n8n:
```python
# In src/core.py (automatic)
requests.post(N8N_EVENT_BUS_URL, json={
    "source": "sovereign-sales-agent-rag",
    "event": "action_completed",
    "data": result
})
```

---

## Adding a New Component

1. **Create** `src/your_component.py` implementing `BaseComponent.execute(action, payload)`
2. **Register** in `src/core.py` dispatcher dict
3. **Test** in `tests/test_solution.py` with a new `TestYourComponent(unittest.TestCase)`
4. **Document** in `docs/ARCHITECTURE.md` under Core Components

## Troubleshooting

| Issue | Diagnosis | Fix |
|-------|-----------|-----|
| Port `8802` in use | `lsof -i :8802` | Kill PID or change `SERVICE_PORT` |
| ImportError on start | venv not active | `source .venv/bin/activate` |
| n8n webhook 404 | Workflow inactive | Activate in n8n UI |
| Docker HEALTHCHECK fail | Service slow start | Increase `start_period` |
| Tests fail in CI | Missing stdlib | Check pyproject.toml `[dev]` extras |

## Release Process

```bash
# 1. Update CHANGELOG.md
# 2. Bump version in pyproject.toml
git add -A
git commit -m "chore: release v1.x.x"
git tag v1.x.x
git push origin main --tags
# GitHub Actions CI runs automatically
```
