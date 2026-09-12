# Security Policy — Sovereign Biz Box

## Supported Versions

| Version | Security Support |
|---------|-----------------|
| 1.x.x (latest) | ✅ Full support |
| < 1.0.0 | ❌ End of life |

## Reporting a Vulnerability

**Do NOT create a public GitHub issue for security vulnerabilities.**

**Report privately to:** russell@blackfoxgaming.com

### What to Include

1. Vulnerability description and CWE classification (if known)
2. Steps to reproduce (minimal PoC)
3. Affected component(s) and version
4. Potential impact assessment
5. Suggested mitigation (optional)

### Our Response Commitment

| Timeline | Action |
|----------|--------|
| 48 hours | Acknowledgment |
| 7 days | Initial assessment |
| 30 days | Fix or mitigation |
| 90 days | Public disclosure (coordinated) |

## Security Architecture

### Authentication
- All API endpoints require `X-SBB-API-Key` header
- Keys must be minimum 32 characters, randomly generated
- Keys stored only in environment variables (never source code)

### Container Security
- Non-root user: `appuser:appgroup` (UID/GID 1001)
- Read-only filesystem where possible
- No `privileged` mode
- Secrets mounted via env vars, not files

### Dependency Management
- Dependabot enabled for automated security updates
- Bandit runs in CI for static security analysis
- Dependencies pinned in `pyproject.toml`

### Network Security
- All external HTTPS, internal HTTP (behind reverse proxy)
- Rate limiting: 100 req/min per client
- Input validation via Pydantic strict models

## Security Checklist for Contributors

- [ ] No secrets committed to source code
- [ ] All user inputs validated with Pydantic
- [ ] External HTTP calls use timeouts
- [ ] No `eval()` or `exec()` on user input
- [ ] SQL queries use parameterized statements
- [ ] Logs do not contain secrets or PII
