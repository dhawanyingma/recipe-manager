# 🍲 Flask Recipe Manager API

A simple RESTful API to manage your favorite recipes, built with Flask, SQLAlchemy, and SQLite.

---

## 📌 Project Overview

This project provides a backend API for managing recipes (create, read, update, delete). It uses Flask for the web framework, SQLAlchemy for ORM, and Flask-Migrate for database migrations. The goal is to provide a lightweight and extensible API for practicing backend skills.

---
## 🧩 Data Model

### 🥘 Recipe

Represents a recipe with optional ingredients and instructions.

| Field         | Type     | Description                               |
|---------------|----------|-------------------------------------------|
| `id`          | Integer  | Primary key, auto-generated               |
| `name`        | String   | Name of the recipe (required, ≥ 3 chars)  |
| `ingredients` | Text     | Ingredients list (optional)               |
| `instructions`| Text     | Cooking steps (optional)                  |
| `created_at`  | DateTime | Auto-added timestamp when created         |
| `updated_at`  | DateTime | Auto-updated timestamp on modification    |

- Managed via SQLAlchemy ORM.
- Will be persisted in SQLite (or PostgreSQL in prod).


## 🚀 Features

* CRUD operations on recipes
* SQLite as a dev database (easily switch to Postgres later)
* Environment-based config
* Input validation
* Global error handling
* Pagination & search
* Auto-generated API docs (OpenAPI/Swagger)
* Unit & integration tests with `pytest`
* Logging and basic security headers

---

## 🔧 Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/your-username/flask-recipe-manager.git
cd flask-recipe-manager
```

### 2. Set up virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # Mac/Linux
.venv\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set environment variables

Copy `.env.example` to `.env` and modify values as needed.

```bash
cp .env.example .env
```

### 5. Run the server (DEV mode)

```bash
flask run
```

---

## 🗃️ Folder Structure

```
app/
├── api/            # API routes
├── models/         # SQLAlchemy models
├── schemas/        # (Optional) Marshmallow or Pydantic schemas
├── services/       # Business logic (optional)
├── db/             # DB setup/migrations

config.py           # Config classes
.env                # Local env variables
requirements.txt    # Python dependencies
README.md           # Project info
```

---

## 🧪 Run Tests

```bash
pytest
```

With coverage:

```bash
pytest --cov=app
```

---

### 📬 API Endpoints (Detailed Contract)

#### ✅ Health & Version

| Method | Endpoint   | Description      | Success | Example Response         |
|--------|------------|------------------|---------|--------------------------|
| GET    | /health    | Health check     | 200     | `{ "status": "ok" }`     |
| GET    | /version   | API version info | 200     | `{ "version": "v1" }`    |

---

#### 🍽️ Recipes

| Method | Endpoint               | Description              | Success | Errors   | Example Response                    |
|--------|------------------------|--------------------------|---------|----------|-------------------------------------|
| POST   | /recipes               | Create a new recipe      | 201     | 422      | `{ "id": 1, "name": "Pasta Salad" }`|
| GET    | /recipes               | List recipes (paginated) | 200     | —        | `{ "items": [...], "page": 1 }`     |
| GET    | /recipes/{id}          | Get recipe by ID         | 200     | 404      | `{ "id": 1, "name": "Chicken" }`    |
| PUT    | /recipes/{id}          | Update recipe by ID      | 200     | 404, 422 | `{ "id": 1, "name": "Updated" }`    |
| DELETE | /recipes/{id}          | Delete recipe by ID      | 204     | 404      | —                                   |
| GET    | /recipes?search=chicken| Search recipes by name   | 200     | —        | `{ "items": [...], "page": 1 }`     |

#### ⚠️ Error Format

All errors follow a consistent structure:

```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Recipe not found",
    "details": {}
  }
}

---

## 📖 API Documentation (OpenAPI)

The API is documented using the OpenAPI standard (Swagger). You can explore and test it using tools like [Swagger Editor](https://editor.swagger.io/) or Postman.

- 🔗 [OpenAPI Spec (YAML)](docs/openapi.yaml) *(will be added in Milestone 10)*
- 🧪 Postman Collection: Coming soon

> Once the `openapi.yaml` file is added in the `docs/` folder, link it here.


📝 Note:
- Pagination will use query params like `?page=1&page_size=10`
- Search will use query param like `?search=chicken`

## 📅 Milestone Checklist

### ✅ Milestone 0 — Repo & Planning

* [ ] Create Git repo
* [ ] Add README & CHANGELOG
* [ ] Define GitHub issues (M1–M10)

### 🏁 Milestone 1 — Environment & Scaffolding

Environment and base structure for the Flask Recipe Manager project has been set up.
✅ Folder Structure
flask-recipe-manager/
├── app/
│   ├── __init__.py
│   ├── api/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── db/
├── tests/
├── docs/
├── .env.example
├── .gitignore
├── README.md
├── CHANGELOG.md
├── config.py
├── requirements.txt
└── .venv/
✅ Setup Completed
Created Python virtual environment: .venv/
Installed core dependencies:
Flask
SQLAlchemy
Flask-Migrate
python-dotenv
Installed developer tools:
black, isort, flake8, pytest, pytest-cov
Created and froze requirements.txt
Added .gitignore (Python template)
Created .env.example:
DATABASE_URL=sqlite:///recipes.db
SECRET_KEY=changeme
DEBUG=True
Created config.py with configuration classes:
Config: base settings
DevConfig: local dev settings (uses SQLite)
TestConfig: test settings (uses in-memory DB)
ProdConfig: production-ready (expects DATABASE_URL from environment)

### 🏗️ Milestone 2 — API Contract (Design First)

* [ ] Add `openapi.yaml` or doc section
* [ ] Document endpoint behavior, request/response formats

### 🗄️ Milestone 3 — DB & Migrations

* [ ] Set up DB URI for SQLite
* [ ] Create migration scripts with Flask-Migrate
* [ ] Add seed file (CSV/JSON) for sample recipes

### ✅ Milestone 4 — Health & Version Endpoints

* [ ] GET /health
* [ ] GET /version
* [ ] Add to Postman collection

### 🍽️ Milestone 5 — Recipe CRUD

* [ ] Create Recipe model & migration
* [ ] Add CRUD routes
* [ ] Manual test via Postman

### ✅ Milestone 6 — Validation & Errors

* [ ] Add field validation
* [ ] Create global error handlers

### 🔍 Milestone 7 — Pagination & Search

* [ ] Add `page`, `page_size`, `search` query params
* [ ] Add response metadata

### ✅ Milestone 8 — Testing

* [ ] Add unit/integration tests
* [ ] Track test coverage

### 🛡️ Milestone 9 — Logging & Security

* [ ] Add structured logs
* [ ] Add basic headers (CORS, no sniff, etc)

### 📚 Milestone 10 — Docs & DX

* [ ] Update OpenAPI spec
* [ ] Finalize README with run/test commands
* [ ] Add changelog entries

### 🌱 Optional: Milestone 11 — Seed & Demo

* [ ] Seed 10–20 recipes for demo/testing

---

## 🛠️ Stretch Goals

* Auth (JWT)
* Tags as many-to-many
* Sorting (`sort=name,-created_at`)
* Dockerfile + docker-compose
* CI/CD workflow (lint, test on push)

---

## ✅ Definition of Done (v1)

* [ ] All endpoints complete
* [ ] SQLite + migrations
* [ ] ≥80% test coverage
* [ ] API docs (OpenAPI + Postman)
* [ ] Errors handled consistently
* [ ] README and changelog polished
