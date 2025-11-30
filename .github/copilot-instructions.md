<!-- GitHub Copilot instructions for AI coding agents -->
# Repository guide for AI coding agents

Purpose: Help an AI agent get productive quickly in this repository by
listing the high-level architecture signals to look for, concrete discovery
commands, and project-specific guidance discovered in the workspace.

1) Immediate repo note
- There are currently no application source files committed — a single
  notebook exists at `webcam_proto.ipynb`. Treat that notebook as an
  experimental prototype; confirm before changing it.

2) High-level discovery checklist (run these first)
- List files: `ls -la`
- Search for common project roots:
  - `rg -n "docker-compose.yml|Dockerfile|requirements.txt|pyproject.toml|package.json|README.md|src/|app/|main.py|.env" || true`
  - If `webcam`, `camera`, or `rtsp` keywords appear, prioritize camera/runtime code.
- Open the notebook `webcam_proto.ipynb` to inspect prototype code and notes.

3) Architecture signals an agent should infer
- Look for these files/directories (if present) to assign responsibilities:
  - `docker-compose.yml` / `Dockerfile` -> deployment boundaries and services
  - `src/`, `app/`, `camera/` -> application code and device adapters
  - `configs/`, `*.yaml`, `.env` -> runtime configuration (camera endpoints, credentials)
  - `notebooks/` or `webcam_proto.ipynb` -> experimental signal processing/prototypes

4) Developer workflows & commands (only run if those files exist)
- Install deps (Python): `python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt`
- Install deps (node): `npm install` if `package.json` exists
- Run tests: `pytest -q` if `tests/` or `pyproject.toml` includes pytest
- Docker compose: `docker compose up --build` if `docker-compose.yml` present

5) Project-specific conventions and patterns
- Prototype-first: presence of `webcam_proto.ipynb` indicates active experimentation.
  - When adding code, prefer creating small modules under `src/` and add a
    minimal script (`run.py` / `main.py`) that can be invoked from CLI or container.
- Config precedence: if both `.env` and `configs/*.yaml` exist, treat `.env`
  as local overrides. (Confirm by searching for code that reads env files.)

6) Integration points to check
- Camera RTSP / HTTP endpoints: search for `rtsp://`, `http://`, `ONVIF` in repo
- Message queues / DB: search for `redis`, `rabbit`, `postgres`, `mqtt` keywords

7) How to modify this file (merge guidance)
- If a `.github/copilot-instructions.md` already exists, merge by:
  1. Preserving any repository-specific examples and commands already present.
  2. Appending missing discovery steps from section 2.
 3. Avoid removing human-authored rationale; update only to reflect current files.

8) Safety & permissions
- Do not attempt to connect to external camera endpoints or modify secrets.
  - If credentials or endpoints are missing, open an issue rather than guessing.

9) When unsure — what to ask the human
- "Where is the main app entrypoint (if any)?"
- "Are cameras simulated or real? Can I run integration tests locally?"

Examples
- Notebook prototype: `webcam_proto.ipynb` — open to review image-capture and analysis code before refactoring.

If anything above is unclear or you want me to tailor the instructions to a
specific layout in this repo, tell me which files to inspect next and I'll
merge/update this document accordingly.
