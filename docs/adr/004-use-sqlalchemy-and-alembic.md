---
status: accepted
date: 2026-05-13
decision-makers: Ivo Vecchietti
---

# Use SQLAlchemy ORM with Alembic migrations

## Context and Problem Statement

The Weather App backend requires a maintainable way to interact with the PostgreSQL database while supporting schema evolution over time.

The project needs:
- Structured database models
- Type-safe database interactions
- Easy session management
- Versioned database schema migrations
- Compatibility with FastAPI and PostgreSQL

As the application evolves, new entities such as locations, search history, weather cache, and user preferences will be added. Database schema changes must therefore be reproducible and version-controlled.

## Decision Drivers

* Strong integration with FastAPI
* ORM support for relational modeling
* Type-safe model definitions
* Migration support for schema evolution
* Good PostgreSQL compatibility
* Large ecosystem and community support
* Maintainable database architecture

## Considered Options

* SQLAlchemy + Alembic
* Raw SQL queries
* Django ORM

## Decision Outcome

Chosen option: "SQLAlchemy with Alembic", because it provides a mature ORM system with strong PostgreSQL support and integrates naturally with FastAPI while allowing version-controlled database migrations.

### Consequences

* Good, because models are defined as Python classes with typed fields
* Good, because database access becomes more maintainable than raw SQL
* Good, because Alembic enables reproducible schema migrations
* Good, because migrations are version-controlled within the repository
* Good, because SQLAlchemy sessions integrate cleanly with FastAPI dependency injection
* Neutral, because ORM abstractions introduce some learning overhead
* Bad, because migration management adds additional development workflow steps

### Confirmation

The backend currently includes:
- SQLAlchemy database engine and session management
- Declarative ORM models
- Typed database columns using SQLAlchemy 2.0 style mappings
- Alembic migration environment
- Initial migration for the `users` table
- Dependency injection for database sessions in FastAPI routes

## Pros and Cons of the Options

### SQLAlchemy + Alembic

* Good, because provides a mature and production-ready ORM
* Good, because supports typed model definitions with SQLAlchemy 2.0
* Good, because Alembic allows version-controlled schema migrations
* Good, because integrates naturally with PostgreSQL and FastAPI
* Neutral, because ORM abstractions can hide generated SQL
* Bad, because migration management adds operational complexity

### Raw SQL queries

* Good, because full control over SQL execution
* Good, because no ORM abstraction overhead
* Bad, because repetitive boilerplate code
* Bad, because harder to maintain as the project grows
* Bad, because schema migrations must be managed manually

### Django ORM

* Good, because includes built-in migration support
* Good, because very mature ecosystem
* Bad, because tightly coupled to Django framework
* Bad, because unnecessary overhead for a FastAPI-based backend
* Bad, because integrating Django ORM independently increases complexity

## More Information

SQLAlchemy documentation:
https://docs.sqlalchemy.org/

Alembic documentation:
https://alembic.sqlalchemy.org/