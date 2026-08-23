# AGENTS.md

## What this repo is

Sigma — hybrid quantum-classical financial risk engine (VaR/CVaR/stress testing).
**Currently a scaffold**: all files under `src/`, `ui/`, and `configs/` are empty placeholders.
The real specification lives in the Vietnamese docs (`README.md`, `docs/RULES.md`, `docs/ARCHITECTURE.md`,
`docs/TECH_STACK.md`, `CONTRIBUTING.md`). Read them before implementing anything.

## Commands

Package manager is **uv**; Python is pinned (`3.12.11`, `<3.13`).

```bash
uv sync                          # install dependencies
uv run pytest                    # run tests
uv run pytest tests/unit/test_foo.py::test_bar   # single test (standard pytest, no custom config/markers exist yet)
uv run ruff check .
uv run ruff format --check .
uv run uvicorn sigma.api.main:app --reload      # FastAPI dev server
```

Gotchas:
- **Makefile is empty** — no make targets exist despite the file being present.
- `pyright` is referenced in docs but is **not in dev dependencies**; don't assume `uv run pyright` works.
- No `[tool.ruff]` / `[tool.pytest.ini_options]` sections in `pyproject.toml` — all defaults.
- `pyproject.toml` has **no `[build-system]`**, so the package isn't installable; imports of `sigma.*` rely on path setup until packaging is added.
- No CI workflows, no pre-commit config.

## Architecture rules (hard constraints from docs/RULES.md)

Dependency direction: `Taipy UI →(HTTP)→ FastAPI → Application → Core`. Never violate:
- UI must not import `sigma.*` core modules directly — only via HTTP API (`ui/api_client.py`).
- Domain/core modules must not depend on FastAPI, Taipy, or Qiskit.
- Qiskit code stays in `src/sigma/quantum/` only; "risk" module must not depend on "quantum".
- API layer holds zero financial computation.
- No premature abstractions: no Factory/Manager/Repository/Service layers, no giant `utils.py`.

Priority when trade-offs conflict: Financial Correctness > Scientific Validity > Architectural Integrity > Reproducibility > Product Utility > Engineering Convenience.

Other binding conventions:
- **Loss convention: loss > 0 means a loss.** Keep simple-vs-log return conventions consistent per RULES-006/007.
- Classical First: every quantum method needs a classical counterpart benchmarked on identical problem/data/settings. Negative/inconclusive results are valid outcomes.
- Data flows `data/raw → data/processed → data/artifacts`.
- Notebooks in `research/notebooks/` are never runtime dependencies; reusable logic graduates to `src/sigma/` via research → validate → stabilize → test.
- Secrets only in `.env` (gitignored); `.env.example` documents keys. Model/scenario params go in `configs/*.yaml`, not env vars.

## Workflow

- Branches: `feature/`, `fix/`, `research/`, `docs/`, `refactor/<name>`. Don't develop significant changes on `main`.
- Commits: small, prefixed — `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, plus non-standard **`research:`** for notebook/experiment work.
- Any change affecting architecture/schema/rules/workflow **must update the corresponding doc in the same change** (RULE-084).
- Test layout semantics (no tests exist yet): `tests/unit` = numerics/domain helpers; `tests/integration` = workflows/API; `tests/evaluation` = model quality + classical-vs-quantum benchmarks. Keep quantum tests independent of backend availability.
