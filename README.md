# secure-notes-api
A secure-by-design REST API for encrypted-at-rest notes, with JWT auth, password hashing, basic security headers, Docker, tests, and CI.

# vaultlight-secure-notes-api

A secure notes API built with FastAPI:
- JWT authentication
- Password hashing (bcrypt)
- Notes encrypted at rest (Fernet)
- SQLite for demo, easy to swap to Postgres
- Docker + docker-compose
- Tests + CI

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

cp .env.example .env
uvicorn app.main:app --reload

Open docs:

http://127.0.0.1:8000/docs

Run with Docker
cp .env.example .env
docker compose up --build
Security notes (intended design)

Passwords are hashed with bcrypt.

Notes are encrypted before storage using a server-side key (FERNET_KEY).

JWT access tokens are signed with JWT_SECRET.

This is a demo architecture; for production, move secrets to a vault/KMS, add refresh tokens, and use Postgres with migrations.