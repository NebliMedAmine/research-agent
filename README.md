# research-agent

Minimal scaffold for the research-agent project.

Run the backend locally:

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000
```

Visit `http://localhost:8000/health` to check the service.
