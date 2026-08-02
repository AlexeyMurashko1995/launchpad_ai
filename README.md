# Launchpad AI — Asynchronous Startup Valuation API 🚀

An asynchronous REST API designed for automated analysis, viability scoring, and technical assessment of startup proposals, powered by Artificial Intelligence.

## 🎯 Goal
This project demonstrates the architecture of a secure, production-ready asynchronous API featuring JWT authentication, role-based authorization, non-blocking background task execution, and structured LLM payload validation.

## 🛠 Tech Stack
* **Framework:** `FastAPI` (Asynchronous REST API)
* **ORM & Database:** `SQLModel` (SQLAlchemy 2.0 & Pydantic v2) with `SQLite` / `Aiosqlite`
* **Security & Auth:** JWT Tokens (`PyJWT`), Password Hashing (`Passlib` / `Bcrypt`)
* **AI Integration:** `Mistral AI API` (Model: `open-mixtral-8x7b`)
* **Task Processing:** FastAPI `BackgroundTasks` (Non-blocking LLM execution)

## 🌟 Key Features
* **Asynchronous Architecture:** High-performance non-blocking database operations via `Aiosqlite`.
* **JWT Authentication:** Secure user registration, login, and token-based route protection (`OAuth2PasswordBearer`).
* **Background Task Execution:** Heavy AI analytical processing is offloaded to `BackgroundTasks` to keep API response times sub-second.
* **Strict JSON Validation:** LLM responses are parsed and validated against strict Pydantic v2 schemas before database persistence.
* **Owner-Only Resource Protection:** Fine-grained authorization rules restricting `PATCH` and `DELETE` actions exclusively to resource owners.

## 🚀 API Endpoints

### Authentication (`/auth`)
* `POST /auth/register` — Register a new user account.
* `POST /auth/login` — Authenticate user and receive a JWT token.
* `GET /auth/me` — Retrieve current authenticated user profile.

### Startups Manager (`/startups`)
* `GET /startups/` — List all registered startups.
* `POST /startups/` — Create a new startup and trigger background AI analysis (Protected).
* `GET /startups/{startup_id}` — Get detailed information and AI analysis for a specific startup.
* `PATCH /startups/{startup_id}` — Update startup details (Owner only, Protected).
* `DELETE /startups/{startup_id}` — Remove a startup from the system (Owner only, Protected).

## 🌍 About Me
Based in **Warsaw, Poland**, focused on building clean, scalable Python backends and data pipelines with practical AI automation.

*Last updated: August 2026*