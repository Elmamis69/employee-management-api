# Employee Management API

RESTful API for managing employees, with authentication, role-based access control and activity logging.  
Built with **Python + FastAPI + PostgreSQL**.

---

## Features (Planned)

- JWT authentication
- Role-based access control (ADMIN, MANAGER, EMPLOYEE)
- Employee CRUD with filters
- Activity logging for all actions
- Pagination & sorting
- Unit & integration tests

---

## Roadmap

### Phase 1 – Project Setup & Basics
- [x] Initialize FastAPI project
- [x] Configure dependencies
- [x] Add basic project structure
- [x] Healthcheck endpoint
- [x] Environment configuration

### Phase 2 – Database & Models
- [x] SQLAlchemy + PostgreSQL setup
- [x] User, Employee, ActivityLog models
- [x] Alembic migrations

### Phase 3 – Authentication & RBAC
- [x] JWT auth
- [x] Login & registration
- [x] Role-based access control

### Phase 4 – Employee Management
- [x] CRUD
- [x] Filters
- [x] Soft delete
- [x] Pagination

### Phase 5 – Activity Logging
- [x] Log system actions
- [x] Error handling
- [x] Tests

---

## Quick Start

### Prerequisites
- Python 3.14+
- Docker & Docker Compose
- PostgreSQL 16 (or use Docker)

### Installation

1. **Clone the repository:**
```bash
git clone <repo-url>
cd employee-management-api
```

2. **Create and activate virtual environment:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment:**
Create a `.env` file in the root (or use the existing one). Example:
```env
ENVIRONMENT=dev
POSTGRES_USER=employee_user
POSTGRES_PASSWORD=employee_password
POSTGRES_DB=employee_db
DATABASE_URL=postgresql+psycopg2://employee_user:employee_password@db:5432/employee_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Running with Docker

1. **Start containers:**
```bash
docker compose up --build
```

2. **Run migrations (in a new terminal):**
```bash
docker compose exec api alembic upgrade head
```

3. **Seed admin user:**
```bash
docker compose exec api python scripts/seed_admin.py
```

4. **Access the API:**
- API: http://localhost:8000
- Docs (Swagger UI): http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health check: http://localhost:8000/health

### Default Admin User
```
Email: admin@example.com
Password: hola123123
```

---

## Testing

### Run all tests:
```bash
pytest -v
```

### Run specific test file:
```bash
pytest tests/test_auth.py -v
pytest tests/test_employees.py -v
```

### Run with coverage:
```bash
pytest --cov=app --cov-report=html
```

### Test results summary:
- **Auth tests:** Login success, wrong password, user not found, missing fields
- **Employee tests:** CRUD operations, authorization, pagination, soft delete, error handling

---

## Database

### Running migrations:
```bash
# Inside Docker
docker compose exec api alembic upgrade head

# Locally (if Postgres is running)
alembic upgrade head
```

### Creating a new migration:
```bash
alembic revision --autogenerate -m "description of changes"
alembic upgrade head
```

### Viewing activity logs:
```bash
docker compose exec db psql -U employee_user -d employee_db -c \
"SELECT id, user_id, action, resource_type, resource_id, details, created_at FROM activity_logs ORDER BY id DESC LIMIT 20;"
```

---

## API Endpoints

### Authentication
- `POST /api/v1/auth/login` — Login with credentials (returns JWT token)
- `POST /api/v1/auth/register` — Register new user
- `GET /api/v1/auth/me` — Get current user profile

### Employees
- `POST /api/v1/employees` — Create employee (ADMIN/MANAGER only)
- `GET /api/v1/employees` — List employees (with pagination & filters)
- `GET /api/v1/employees/{id}` — Get employee by ID
- `PUT /api/v1/employees/{id}` — Update employee (ADMIN/MANAGER only)
- `DELETE /api/v1/employees/{id}` — Delete employee - soft delete (ADMIN/MANAGER only)

### Query Parameters
- `is_active` — Filter by active status (default: true)
- `skip` — Pagination offset (default: 0)
- `limit` — Items per page (default: 20, max: 100)

---

## Architecture

### Project Structure
```
app/
├── main.py                 # FastAPI app setup & exception handlers
├── api/
│   ├── deps_auth.py       # Auth dependencies & RBAC
│   └── v1/
│       ├── routes_auth.py # Authentication routes
│       └── routes_employees.py  # Employee CRUD routes
├── core/
│   ├── config.py          # Settings from env
│   ├── logging.py         # Activity logging helper
│   └── security.py        # JWT & password hashing
├── db/
│   ├── session.py         # DB connection setup
│   ├── deps.py            # DB dependencies
│   └── __init__.py
├── models/
│   ├── user.py            # User model
│   ├── employee.py        # Employee model
│   └── activity_log.py    # Activity log model
└── schemas/
    ├── user.py            # User Pydantic schemas
    └── employee.py        # Employee Pydantic schemas

tests/
├── conftest.py            # Pytest fixtures & configuration
├── test_auth.py           # Auth tests
└── test_employees.py      # Employee CRUD tests

migrations/                # Alembic migrations

scripts/
└── seed_admin.py          # Script to seed admin user
```

### Key Features

**1. Authentication (JWT)**
- OAuth2 with JWT tokens
- Secure password hashing with bcrypt
- 30-minute token expiration (configurable)

**2. Role-Based Access Control (RBAC)**
- Three roles: ADMIN, MANAGER, EMPLOYEE
- Protected endpoints require appropriate role
- Admin/Manager can manage employees
- Employees can view their own profile

**3. Activity Logging**
- All CRUD operations logged with user, action, resource, timestamp
- Soft delete: marks employees as inactive instead of removing

**4. Error Handling**
- Centralized exception handlers
- Consistent JSON error responses
- Validation errors (422), auth errors (401), not found (404)

**5. Testing**
- 17 unit & integration tests (pytest)
- Fixtures for BD session, TestClient, admin user
- Tests cover auth, CRUD, pagination, soft delete, edge cases

---

## Development

### Code Style
- Follow PEP 8
- Use type hints

### Git Workflow
- Main branch: production-ready code
- Feature branches: development

### Logging
- Uvicorn error logger for exceptions
- Activity logs for business events (stored in DB)

---

## Troubleshooting

### "Database connection refused"
- Ensure PostgreSQL is running
- Check `DATABASE_URL` in `.env`
- Verify Docker container is up: `docker compose ps`

### "Role 'postgres' does not exist"
- Use correct `POSTGRES_USER` from `.env` (e.g., `employee_user`)
- Recreate containers: `docker compose down && docker compose up --build`

### Tests fail with "fixture not found"
- Ensure `tests/conftest.py` exists and has correct imports
- Run from project root: `pytest tests/`

---

## License
MIT

---

## Author
Adrián Félix

Software Engineering

Passionate about Android Developer, Full Stack and iOS development and clean architecture.

GitHub: @Elmamis69
Email: guerofelix234@gmail.com

**License**
This project is licensed under the MIT License.


