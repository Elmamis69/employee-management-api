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
- [ ] Role-based access control

### Phase 4 – Employee Management
- [x] CRUD
- [x] Filters
- [x] Soft delete
- [x] Pagination

### Phase 5 – Activity Logging
- [x] Log system actions
- [x] Error handling
- [ ] Tests


---
