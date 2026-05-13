---
status: accepted
date: 2026-05-13
decision-makers: Ivo Vecchietti
---

# Use PostgreSQL as the primary database

## Context and Problem Statement

The Weather App backend requires persistent storage for users, authentication data, locations, search history, and future weather-related entities.

The database solution must support relational data modeling, scalability, transactions, and integration with modern Python backend tooling. The project should also remain portable between local development and future cloud deployments.

## Decision Drivers

* Reliable relational database support
* ACID compliance and transactional integrity
* Good integration with SQLAlchemy
* Scalability for future application growth
* Strong ecosystem and community support
* Compatibility with Docker-based local development
* Production readiness

## Considered Options

* PostgreSQL
* SQLite
* MongoDB

## Decision Outcome

Chosen option: "PostgreSQL", because it provides a robust and scalable relational database system with excellent support for transactions, indexing, relationships, and integration with SQLAlchemy.

### Consequences

* Good, because PostgreSQL is production-ready and widely adopted
* Good, because relational modeling fits the application's user and authentication system
* Good, because SQLAlchemy integrates naturally with PostgreSQL
* Good, because PostgreSQL supports advanced querying and indexing capabilities
* Good, because Docker Compose makes local setup straightforward
* Neutral, because running PostgreSQL locally requires container orchestration or local installation
* Bad, because setup complexity is higher compared to SQLite

### Confirmation

The backend currently uses PostgreSQL through SQLAlchemy with:
- Database session management
- User persistence
- Alembic migrations
- Docker Compose database configuration
- Environment-based database URL configuration

## Pros and Cons of the Options

### PostgreSQL

* Good, because fully-featured relational database with strong ACID guarantees
* Good, because excellent support for indexing and complex queries
* Good, because integrates seamlessly with SQLAlchemy and Alembic
* Good, because widely used in production systems
* Neutral, because local setup is more complex than file-based databases
* Bad, because requires additional infrastructure compared to SQLite

### SQLite

* Good, because extremely simple setup with no separate server
* Good, because useful for prototypes and lightweight local testing
* Bad, because limited concurrency support
* Bad, because not ideal for scalable production deployments
* Bad, because lacks some advanced PostgreSQL capabilities

### MongoDB

* Good, because flexible schema design
* Good, because document storage can simplify some workflows
* Bad, because the application data is strongly relational
* Bad, because transactions and relational constraints are less natural
* Bad, because SQLAlchemy integration is not as straightforward

## More Information

PostgreSQL documentation:
https://www.postgresql.org/docs/