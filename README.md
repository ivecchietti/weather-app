# weather-app

![CI](https://github.com/ivecchietti/weather-app/actions/workflows/ci.yml/badge.svg)

Modern full-stack weather application built with FastAPI and Next.js.

The project includes:
- JWT authentication
- PostgreSQL persistence
- SQLAlchemy ORM
- Alembic migrations
- Dockerized local development
- Automated testing
- CI with GitHub Actions
- Architecture Decision Records (ADRs)

---

## Overview

The application allows users to:
- Create accounts and authenticate securely
- Search weather information for different locations
- Persist user-related data
- Interact with a modern REST API backend
- Run the project locally using Docker

The project is designed following professional backend engineering practices with modular architecture, environment-based configuration, migrations, automated testing, and CI pipelines.

---

## Features

### Backend

- FastAPI REST API
- JWT authentication
- Password hashing
- PostgreSQL integration
- SQLAlchemy ORM
- Alembic database migrations
- Dependency injection pattern
- Environment-based configuration with `pydantic-settings`
- Automated tests with `pytest`
- Code quality checks with `ruff`

### Frontend

- Next.js frontend
- TypeScript support
- Modern React architecture
- API integration with backend services

### DevOps

- Docker Compose setup
- GitHub Actions CI pipeline
- Automated linting and testing
- Architecture Decision Records (ADRs)

---

## Tech Stack

### Backend

- Python 3.11+
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- Pydantic
- JWT Authentication
- Pytest
- Ruff

### Frontend

- Next.js
- React
- TypeScript
- TailwindCSS

### DevOps

- Docker
- Docker Compose
- GitHub Actions

---

## Project Structure


.
├── alembic/               # Database migrations
├── app/
│   ├── api/               # API routes and dependencies
│   ├── core/              # Configuration and security
│   ├── db/                # Database setup
│   ├── models/            # SQLAlchemy ORM models
│   ├── schemas/           # Pydantic schemas
│   └── main.py            # FastAPI application
├── docs/
│   └── adr/               # Architecture Decision Records
├── tests/                 # Automated tests
├── .github/
│   └── workflows/         # GitHub Actions CI
├── docker-compose.yml
├── requirements.txt
└── README.md


---

## Environment Variables

Create a `.env` file in the project root:


DATABASE_URL=postgresql://postgres:postgres@localhost:5432/weather_db
WEATHER_API_KEY=your_api_key
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

---

## Local Development

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run PostgreSQL with Docker

```bash
docker compose up -d
```

### Run database migrations

```bash
alembic upgrade head
```

### Start backend server

```bash
uvicorn app.main:app --reload
```

Swagger documentation:
http://localhost:8000/docs


---

## Testing

Run tests:

```bash
pytest
```

Run linting:

```bash
ruff check .
```

---

## Continuous Integration

The project includes a GitHub Actions CI pipeline that automatically:

- Runs Ruff lint checks
- Executes automated tests
- Validates pull requests
- Verifies environment configuration

The pipeline runs on:
- pushes to `develop`
- pushes to `feature/**`
- pull requests to `main` and `develop`

---

## Architecture Decisions

Technical decisions are documented using ADRs inside:

```text
docs/adr/
```

Current ADRs include:
- FastAPI framework selection
- Pydantic settings configuration
- PostgreSQL database choice
- SQLAlchemy + Alembic strategy

---

## Current Status

### Implemented

- Backend architecture
- PostgreSQL integration
- Authentication base
- Database migrations
- CI pipeline
- Automated testing
- ADR documentation

### In Progress

- Login flow
- Weather API integration
- Search history persistence
- Frontend integration
- Weather caching system

---

## Future Improvements

- Redis caching
- Rate limiting
- Background tasks
- Weather analytics
- User preferences
- Deployment infrastructure
- Monitoring and observability