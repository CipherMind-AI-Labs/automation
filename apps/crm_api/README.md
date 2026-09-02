# CRM API

FastAPI server that exposes the CRM data layer via REST endpoints, backed by
Cloudflare D1 through the D1 HTTP REST API. No Cloudflare Workers runtime required.

## Setup

### 1. Configure credentials

```powershell
copy apps\crm_api\.env.example apps\crm_api\.env
# Then fill in CF_ACCOUNT_ID and CF_API_TOKEN in .env
```

`CF_D1_DATABASE_ID` is pre-filled — it matches `wrangler.jsonc`.

To get a **Cloudflare API Token**:
`dash.cloudflare.com → My Profile → API Tokens → Create Token`
Use the **"Edit Cloudflare Workers"** template and verify it includes **D1: Edit**.

### 2. Install dependencies (first time only)

From the `automation/` root:

```powershell
uv pip install --python .venv "fastapi[standard]" "uvicorn[standard]" httpx python-dotenv
```

## Running locally

All commands run from the **`automation/` root** using the shared `.venv`.

```powershell
# Start the API server on port 8787
.venv\Scripts\uvicorn src.app:app --app-dir apps\crm_api --port 8787 --reload
```

The server starts at `http://127.0.0.1:8787`.

## API endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Liveness probe |
| GET | `/api/companies` | List all companies |
| POST | `/api/companies` | Create a company |
| GET | `/api/companies/:id` | Get company by ID |
| PUT | `/api/companies/:id` | Update company |
| DELETE | `/api/companies/:id` | Delete company |
| GET | `/api/contacts` | List contacts |
| GET | `/api/opportunities` | List opportunities |
| GET | `/api/communication-threads` | List communication threads |
| GET | `/api/reminders` | List follow-up reminders |

Interactive API docs: `http://127.0.0.1:8787/docs`

## Tests

```powershell
C:/Users/Vishal/AppData/Local/Python/pythoncore-3.14-64/python.exe -m pytest -q
```

## Deployment

`wrangler.jsonc` is retained for future Cloudflare deployment. The D1 database
binding and schema remain the same — only the server runtime changes.
