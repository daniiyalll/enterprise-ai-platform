# CortexFlow — Frontend for the Enterprise AI Workflow Platform

A dependency-free HTML/CSS/JS single-page app (no npm, no build step) that talks
directly to the FastAPI backend in `enterprise-ai-platform-main/backend`.

## Run it

1. **Start the backend** (from `backend/`):
   ```bash
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```
   It should be running at `http://127.0.0.1:8000`. CORS is now enabled in
   `app/main.py` so the frontend can call it from a different origin.

2. **Serve the frontend** (any static server works — opening `index.html`
   directly also works in most browsers, but a local server avoids edge
   cases with `fetch`):
   ```bash
   cd frontend
   python3 -m http.server 5500
   ```
   Then open `http://127.0.0.1:5500`.

3. If your backend isn't on `http://127.0.0.1:8000/api/v1`, click the
   "API: ..." link at the bottom of the login screen to change it — it's
   stored in `localStorage`, no rebuild needed.

## Getting your first account

Signup requires the `SIGNUP_SECRET` value from the backend's `.env` file
(`POST /auth/signup` checks it). Use "Request access" on the login screen
and enter that value as the secret key. The first account you create can be
role `admin`, which unlocks user management (`/users` page) to promote/demote
everyone else later.

## Pages

| Route | Who can see it | Talks to |
|---|---|---|
| `#/dashboard` | admin, manager | `GET /dashboard/stats` |
| `#/workflows` | everyone | `GET/POST/PUT/DELETE /workflows` |
| `#/decisions` | admin, manager | `POST /decisions/evaluate`, `GET /decisions/history` |
| `#/mining` | admin, manager | `GET /process-mining/summary` |
| `#/agents` | everyone | `POST /agents/compliance|approval|document` |
| `#/predict` | everyone | `POST /ai/predict` |
| `#/copilot` | everyone | `POST /copilot/ask` |
| `#/users` | admin | `GET /users`, `PUT /users/{id}/role` |

Role gating in the UI mirrors the backend's `require_role` /
`require_manager` / `require_employee` dependencies — but the backend is
still the real enforcement point, the frontend just hides links a given
role can't use.

## Notes / limitations

- No build tooling was used because this container has no network access to
  npm; if you'd rather have a React/Vite version, this is a straightforward
  1:1 port — every page here is a plain render function.
- The JWT is decoded client-side (not verified) purely to read `sub`/`role`
  for display and nav gating; every real request still carries the token
  and the backend verifies it.
- `#/predict` assumes the model's 3 features are, in order:
  `process_duration_hours, num_approvals, priority_level` (matches
  `dataset/risk_training_data.csv`). Update `js/pages/predict.js` if the
  model is retrained with different features.
