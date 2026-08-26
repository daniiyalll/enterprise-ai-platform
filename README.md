# Enterprise Autonomous Business Process Intelligence Platform

An AI-powered workflow automation platform, developed as part of the Ezitech
internship. It combines a rules + ML based decision engine, individual AI
agents (compliance, approval, document checks), a risk-prediction model,
a conversational copilot, and process mining over workflow event logs —
all exposed through a FastAPI backend and a browser-based frontend
("CortexFlow").

## Status

Core backend and frontend are implemented and working end-to-end locally
(authentication, workflows, decisions, AI agents, risk prediction, copilot,
process mining, user management).

## Tech Stack

**Backend:** Python, FastAPI, SQLAlchemy, PostgreSQL, scikit-learn, pm4py
**Frontend:** HTML5, CSS3, JavaScript (no build tooling — plain SPA)
**Auth:** JWT (OAuth2 password flow)
**Migrations:** Alembic

## Project Structure

\`\`\`
backend/
  app/
    api/          # route handlers (auth, workflows, decisions, agents, ...)
    core/         # config, security, roles/permissions
    database/     # engine, session, declarative base
    models/       # SQLAlchemy models
    schemas/      # Pydantic request/response schemas
    services/     # business logic (decision engine, copilot, process mining, ...)
    ai/           # risk prediction model
  alembic/        # database migrations
  tests/          # pytest test suite (runs against a throwaway SQLite DB)
  dataset/        # training data + workflow event log for process mining
  .env.example    # required environment variables (copy to .env)
frontend/
  index.html, css/, js/    # plain JS single-page app ("CortexFlow")
\`\`\`

## Running locally

### 1. Backend

\`\`\`bash
cd backend
pip install -r requirements.txt
cp .env.example .env        # then fill in real values
alembic upgrade head        # create/update database tables
uvicorn app.main:app --reload
\`\`\`

Backend runs at \`http://127.0.0.1:8000\`. Interactive API docs at
\`http://127.0.0.1:8000/docs\`.

### 2. Frontend

\`\`\`bash
cd frontend
python -m http.server 5500
\`\`\`

Open \`http://127.0.0.1:5500\`. If your backend isn't on the default
\`http://127.0.0.1:8000/api/v1\`, change it from the login screen (stored in
\`localStorage\`, no rebuild needed).

### 3. First account

Sign-up requires the \`SIGNUP_SECRET\` value from \`backend/.env\`. Use
"Request access" on the login screen. The first account should be role
\`admin\` so you can manage other users afterward from the Users page.

## Database migrations

This project uses Alembic instead of relying on \`create_all()\`, so schema
changes are tracked and repeatable.

\`\`\`bash
cd backend
alembic upgrade head                              # apply all migrations
alembic revision --autogenerate -m "add X column"  # create a new migration after changing a model
alembic downgrade -1                               # roll back one migration
\`\`\`

If you already have tables created the old way (via \`create_tables.py\` or
app startup) and want to start using Alembic without losing data, run:
\`alembic stamp head\` instead of \`alembic upgrade head\` the first time —
this tells Alembic "the schema is already at this point" without
re-running the migration.

## Tests

\`\`\`bash
cd backend
pip install pytest httpx
pytest
\`\`\`

Tests run against an isolated SQLite database (\`test.db\`, created and
deleted automatically) — they never touch your real Postgres database.

## Environment variables

See \`backend/.env.example\`. Required:

| Variable | Description |
|---|---|
| \`DATABASE_URL\` | PostgreSQL connection string |
| \`SECRET_KEY\` | Signs JWT auth tokens — keep secret, rotate if ever exposed |
| \`SIGNUP_SECRET\` | Invite code required to create new accounts |

**Never commit \`.env\`.** It's already in \`.gitignore\`; use \`.env.example\`
as the template for what needs to be set.
