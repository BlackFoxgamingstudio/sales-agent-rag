# Contributing to Sovereign Biz Box

We welcome contributions from developers worldwide! The SBB platform is designed to be a global automation standard.

## Getting Started

1. **Fork** the repository on GitHub
2. **Clone** your fork: `git clone https://github.com/YOUR_USERNAME/REPO.git`
3. **Create a branch**: `git checkout -b feature/your-feature`
4. **Write tests** for all new functionality
5. **Run CI locally**: `python -m pytest tests/ -v && ruff check src/`
6. **Submit a PR** against the `develop` branch

## Commit Message Convention (Conventional Commits)

```
feat(component): add new capability
fix(api): correct response schema
docs(arch): update architecture diagram
test(core): add unit test for dispatcher
chore(deps): update dependencies
refactor(engine): simplify dispatch logic
perf(db): add index for faster queries
ci: add security scan step
```

## Code Standards

| Tool | Purpose | Config |
|------|---------|--------|
| `ruff` | Linting + formatting | `ruff.toml` or `pyproject.toml[tool.ruff]` |
| `mypy` | Type checking | `pyproject.toml[tool.mypy]` |
| `bandit` | Security scanning | CI step |
| `pytest` | Testing | `pyproject.toml[tool.pytest.ini_options]` |

## PR Requirements

- [ ] Tests pass (`python -m pytest tests/ -v`)
- [ ] No new linting errors (`ruff check src/`)
- [ ] CHANGELOG.md updated under `[Unreleased]`
- [ ] Documentation updated if API or architecture changes
- [ ] Docker image builds successfully (`docker build .`)

## Architecture Conventions (SBB Standards)

All SBB solutions follow the **Patterns Bible** conventions:
- REST API envelope: `{"action": "", "payload": {}, "trace_id": ""}`
- Health endpoint: `GET /health` → `{"status": "healthy"}`
- Port scheme: each solution has a unique port in the 8780–8820 range
- Event emission: all actions emit to the n8n Central Event Bus
- Non-root Docker: container user = `appuser:1001`

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
