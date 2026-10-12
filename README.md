# CreativeOps AI

Python-native creative production and governed asset management demo.

## Phase 1 scaffold
Includes FastAPI health endpoint and Google Drive OAuth brand-library initialization. Image generation, ComfyUI, agents, Streamlit, and renderer are planned, not yet implemented.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Place your private Google OAuth **Desktop** client JSON in `secrets/credentials.json` (never commit this). Keep a local copy of the approved brand library with its folder structure intact, then run:

```bash
python -m scripts.initialize_brand_repository '/absolute/path/to/brand-library'
uvicorn app.api.main:app --reload
pytest
```

The initialization script creates a **new app-managed copy** of the approved brand files in your personal Google Drive, preserving their relative folders, and verifies every upload using SHA-256. It does not modify your manually uploaded originals. Running it again creates a duplicate library. It writes file IDs to `.local/brand_repository.json`.

The restricted `drive.file` scope does not automatically grant access to existing manually uploaded files. After initialization, the application will treat approved brand files as read-only by policy; this is not a separate Google-enforced permission boundary.

## Architecture

FastAPI + explicit Python orchestration; OpenAI default generation; optional ComfyUI; Streamlit review UI; static brand library; Google Drive DAM integration. The original LangGraph system coordinated broader dependencies; the narrower reference flow deliberately uses deterministic services where agent orchestration is unnecessary.
