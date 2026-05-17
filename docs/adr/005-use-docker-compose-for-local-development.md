---
status: accepted
date: 2026-05-17
decision-makers: Ivo Vecchietti
---

# Use Docker Compose for local development

## Context and Problem Statement

The Weather App backend requires multiple services to run together during local development, including the FastAPI application and a PostgreSQL database.

Running these services manually across different environments introduces setup inconsistencies and increases onboarding complexity. The project also needs a reproducible local development environment that mirrors future deployment architectures more closely.

The development workflow should therefore support:

- Easy startup of all services
- Consistent environments across machines
- Simplified database setup
- Containerized local development
- Reduced dependency on host machine configuration

## Decision Drivers

* Consistent local development environments
* Simplified onboarding process
* Easy PostgreSQL setup
* Isolation from host machine dependencies
* Compatibility with future deployment workflows
* Single-command startup experience
* Good integration with FastAPI and PostgreSQL

## Considered Options

* Manual local setup
* Docker Compose
* Cloud-hosted development database

## Decision Outcome

Chosen option: "Docker Compose", because it allows the backend API and PostgreSQL database to run together with a single command while ensuring consistent environments across development machines.

### Consequences

* Good, because developers can start the entire stack with `docker compose up`
* Good, because PostgreSQL setup becomes automatic and reproducible
* Good, because services are isolated from the host machine
* Good, because the environment becomes closer to production deployments
* Good, because onboarding new developers becomes simpler
* Neutral, because Docker introduces additional tooling requirements
* Bad, because containerized workflows may consume more system resources

### Confirmation

The backend currently includes:

- Dockerfile for FastAPI application
- Docker Compose configuration
- PostgreSQL container setup
- Persistent Docker volumes for database storage
- Environment-based configuration through `.env`
- Working API communication between containers

The application can now be started with:

```bash
docker compose up --build
```

Database migrations can be executed with:

```bash
docker compose exec api alembic upgrade head
```

## Pros and Cons of the Options

### Docker Compose

* Good, because multiple services can run together with a single command
* Good, because environments remain consistent across machines
* Good, because PostgreSQL setup is automated
* Good, because container isolation reduces host dependency issues
* Neutral, because developers must learn basic Docker workflows
* Bad, because containers consume additional system resources

### Manual local setup

* Good, because no container tooling is required
* Good, because simpler for extremely small projects
* Bad, because environment inconsistencies are common
* Bad, because PostgreSQL installation varies across systems
* Bad, because onboarding becomes more difficult

### Cloud-hosted development database

* Good, because no local database setup is required
* Good, because production-like infrastructure can be used
* Bad, because internet access becomes mandatory
* Bad, because introduces external service dependencies
* Bad, because local development workflows become less portable

## More Information

Docker documentation:
https://docs.docker.com/

Docker Compose documentation:
https://docs.docker.com/compose/