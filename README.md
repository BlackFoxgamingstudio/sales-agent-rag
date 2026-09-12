# Sovereign Sales Agent Rag (`sovereign-sales-agent-rag`)

[![PyPI Version](https://img.shields.io/badge/pypi-v1.0.0-blue.svg)](pyproject.toml)
[![Tests](https://img.shields.io/badge/pytest-passing_100%25-brightgreen.svg)](tests/test_solution.py)
[![CI](https://github.com/BlackFoxgamingstudio/sales-agent-rag/actions/workflows/ci.yml/badge.svg)](https://github.com/BlackFoxgamingstudio/sales-agent-rag/actions/workflows/ci.yml)
[![n8n Integration](https://img.shields.io/badge/n8n-workflow_ready-orange.svg)](n8n/workflow.json)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Enterprise Standalone Package**: Autonomous sales qualification and B2B outreach agent. Integrates Swagger API specifications with ChromaDB vector search (`apiragbuiderv2.py`) to answer complex technical sales questions and qualify inbound leads.

---

## 1. Overview & Architectural Blueprint

`sovereign-sales-agent-rag` is an independently packaged, zero-dependency software library and microservice engineered as part of Russell Alan Powers' 10-year software engineering portfolio.

It delivers robust capabilities in **Conversational AI & Sales Automation** and provides seamless integration with n8n event workflows.

```
┌───────────────────────────┐         HTTP POST          ┌───────────────────────────────────────────┐
│        n8n Engine         │ ─────────────────────────> │        sovereign-sales-agent-rag Adapter        │
│   (Port 5678 Webhook)     │ <───────────────────────── │             (Port 8802)                 │
└───────────────────────────┘       Idempotent JSON      └───────────────────────────────────────────┘
                                                                               │
                                                                               ▼
                                                         ┌───────────────────────────────────────────┐
                                                         │            CoreEngine Domain              │
                                                         │      (SHA-256 Idempotent Execution)       │
                                                         └───────────────────────────────────────────┘
```

---

## 2. Core Exported Classes & Features

- **Primary Module**: `from sovereign_sales_agent_rag import SalesRAGBuilder, SwaggerAPIIndexer, LeadQualifier, OutreachDispatcher`
- **Deterministic Idempotency**: All executions generate unique SHA-256 idempotency tokens preventing duplicate runs across network retries.
- **Self-Contained Microservice**: Zero external third-party dependencies required for base execution.

---

## 3. Installation & Quickstart

```bash
# Clone the repository
git clone https://github.com/russellpowers/sovereign-sales-agent-rag.git
cd sales-agent-rag

# Install in editable mode
pip install -e .

# Verify health status via CLI
sovereign-sales-agent-rag --health
```

---

## 4. CLI Usage Reference

```bash
# Check service health
sovereign-sales-agent-rag --health

# Execute core domain action with a JSON payload
sovereign-sales-agent-rag --exec process_data --payload '{"sample_key": "sample_value"}'
```

---

## 5. n8n Automation & Integration Contract

- **Microservice Port**: `http://localhost:8802`
- **Inbound Trigger Route**: `POST /api/v1/execute`
- **Integration Workflow**: `HubSpot/Typeform webhook -> Ingest lead details -> RAG knowledge retrieval -> Output qualified lead score and tailored pitch`

### How to Import into n8n:
1. Open your n8n canvas (`http://localhost:5678`).
2. Click **Workflows** > **Import from File**.
3. Select `n8n/workflow.json`.
4. Start the background webhook adapter:
   ```bash
   python3 n8n/webhook_adapter.py
   ```
5. Dispatch your test event to `http://localhost:5678/webhook/sales-agent-rag-trigger`.

---

## 6. Verification & Automated Testing

This repository includes a 100% passing test suite runnable via `pytest` or `python3`:

```bash
# Run tests with pytest
pytest tests/test_solution.py -v

# Run tests directly (zero dependencies)
python3 tests/test_solution.py
```

---

## 7. Staff/Principal Engineer Technical Defense

> **60-Second Interview Pitch**:
> "Demonstrates applied enterprise AI: grounding sales LLMs on live API specs, automated qualification scoring, and CRM pipeline acceleration."
