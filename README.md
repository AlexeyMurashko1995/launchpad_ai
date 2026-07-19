# Launchpad AI

An asynchronous web API designed for automated analysis and viability assessment of startup ideas, powered by Artificial Intelligence. The system evaluates startup proposals and generates structured feedback including strengths, weaknesses, and potential business risks.

## 🛠 Tech Stack
* **Backend Framework:** FastAPI (Async)
* **Data Management & ORM:** SQLModel + SQLAlchemy
* **Database:** SQLite (with Aiosqlite for asynchronous interaction)
* **Data Validation:** Pydantic v2
* **AI Integration:** Mistral AI API (Model: `open-mixtral-8x7b`)
* **Security:** JWT Tokens (PyJWT) + Password Hashing (Passlib)

## 🌟 Key Features
* **Asynchronous Architecture:** High-performance database operations and non-blocking requests.
* **JWT Authentication:** Secure user registration, login, and protected routes.
* **Background Processing:** AI analysis is handled as a background task to keep the API responsive.
* **Strict JSON Validation:** AI responses are strictly validated against Pydantic schemas before saving.
* **Data Sanitization:** Automatic trimming of input strings to prevent whitespace pollution in the database.

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