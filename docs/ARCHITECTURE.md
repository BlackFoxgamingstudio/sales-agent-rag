# Architecture: Sovereign Sales Agent RAG

## Overview

**Package ID:** `PKG-022`  
**Domain:** Conversational AI & Sales Automation  
**Microservice Port:** `8802`  
**n8n Webhook Path:** `sales-agent-rag-trigger`  
**GitHub:** [BlackFoxgamingstudio/sales-agent-rag](https://github.com/BlackFoxgamingstudio/sales-agent-rag)

Conversational AI sales assistant with RAG-powered product knowledge, objection handling, quote generation, CRM sync, and revenue forecasting.

---

## System Architecture

```
                     ┌──────────────────────────────────┐
                     │       Sovereign Sales Agent RAG     │
                     │       Port: 8802            │
                     ├──────────────┬───────────────────┤
   n8n Webhook ────▶ │  REST API    │   Core Engine     │
   HTTP POST         │  /api/v1/*   │   Dispatcher      │
                     └──────┬───────┴────────┬──────────┘
                            │                │
              ┌─────────────▼────────────────▼─────────┐
              │          Component Layer                 │
              │  ConversationEng | ProductKnowledg | ObjectionHan  │
              └────────────────────────┬────────────────┘
                                       │
              ┌────────────────────────▼────────────────┐
              │      n8n Central Event Bus (:5678)       │
              └─────────────────────────────────────────┘
```

## Core Components

### `ConversationEngine`
Handles all conversation operations. Exposes async methods callable from the core dispatcher.

### `ProductKnowledgeRAG`
Handles all productknowledgerag operations. Exposes async methods callable from the core dispatcher.

### `ObjectionHandler`
Handles all objectionhandler operations. Exposes async methods callable from the core dispatcher.

### `QuoteGenerator`
Handles all quotegenerator operations. Exposes async methods callable from the core dispatcher.

### `CRMSyncer`
Handles all crmsyncer operations. Exposes async methods callable from the core dispatcher.

---

## API Contract

All interactions follow the SBB standard envelope:

```http
POST /api/v1/execute
Content-Type: application/json
X-SBB-API-Key: <api-key>

{
  "action": "<operation>",
  "payload": {},
  "trace_id": "optional-uuid"
}
```

**Success Response (HTTP 200):**
```json
{
  "status": "success",
  "data": {},
  "trace_id": "...",
  "timestamp": "2025-01-01T00:00:00Z"
}
```

**Health Check:**
```http
GET /health
→ {"status": "healthy", "service": "sovereign-sales-agent-rag", "port": 8802}
```

## Integration Matrix

| System | Protocol | Direction | Purpose |
|--------|----------|-----------|---------|
| n8n Event Bus (:5678) | HTTP POST | Outbound | Event forwarding |
| n8n Webhook | HTTP POST | Inbound | Trigger execution |
| SBB Codebase Vault (:8766) | HTTP | Outbound | Code analysis |
| SBB Patterns Bible (:8794) | HTTP | Outbound | Standards validation |
| External APIs | HTTPS | Outbound | Domain-specific data |

## Deployment Architecture

```yaml
# docker-compose excerpt
sovereign-sales-agent-rag:
  image: sovereign-sales-agent-rag:latest
  ports: ["8802:8802"]
  healthcheck:
    test: curl -f http://localhost:8802/health
    interval: 30s
```

## Security Model

| Control | Implementation |
|---------|---------------|
| Authentication | `X-SBB-API-Key` header (env: `SBB_API_KEY`) |
| Rate Limiting | 100 req/min per client IP |
| Input Validation | Pydantic models (strict mode) |
| Container Security | Non-root user (`appuser:1001`) |
| Secrets | Environment variables only (never hardcoded) |
| TLS | Terminate at reverse proxy (nginx/caddy) |

## Tags
`sales`, `rag`, `llm`, `crm`
