---
status: accepted
date: 2026-05-11
decision-makers: Ivo Vecchietti
---

# Use FastAPI as the backend framework

## Context and Problem Statement

The Weather App backend requires a modern Python web framework capable of exposing REST APIs with automatic documentation, request validation, authentication support, and high development speed.

The application is expected to grow over time, including user authentication, weather endpoints, search history persistence, caching, and external API integrations. The framework should therefore support scalability and maintainability while remaining simple to develop locally.

## Decision Drivers

* Automatic OpenAPI/Swagger documentation
* Request and response validation
* Good integration with modern Python tooling
* Async support for future scalability
* Fast development speed
* Easy integration with authentication systems (JWT)
* Good ecosystem and community support

## Considered Options

* FastAPI
* Flask
* Django REST Framework

## Decision Outcome

Chosen option: "FastAPI", because it provides automatic OpenAPI documentation, native validation through Pydantic, async support, and minimal boilerplate while maintaining high performance.

### Consequences

* Good, because Swagger/OpenAPI documentation is automatically available at `/docs`
* Good, because request validation is handled automatically with Pydantic schemas
* Good, because FastAPI integrates naturally with dependency injection patterns
* Good, because async support allows future scalability for external weather API calls
* Good, because JWT authentication integrates cleanly with FastAPI dependencies
* Neutral, because the framework introduces concepts such as dependency injection that require some learning
* Bad, because the ecosystem is newer than Flask/Django in some areas

### Confirmation

The backend is operational with:
- FastAPI application structure
- Modular API routes
- Pydantic request/response schemas
- Automatic Swagger documentation
- Authentication endpoints
- Dependency injection for database sessions

## Pros and Cons of the Options

### FastAPI

* Good, because automatic OpenAPI generation is built-in
* Good, because Pydantic provides strong typing and validation
* Good, because async support is native
* Good, because development speed is high with minimal boilerplate
* Neutral, because some advanced concepts require learning
* Bad, because some third-party integrations are less mature than Flask

### Flask

* Good, because it is lightweight and widely used
* Good, because the ecosystem is very mature
* Bad, because validation and documentation require additional libraries
* Bad, because async support is not native
* Bad, because larger projects require more manual structure

### Django REST Framework

* Good, because it provides many built-in features
* Good, because authentication and ORM are mature
* Bad, because it is heavyweight for the scope of this project
* Bad, because setup and configuration are more complex
* Bad, because it introduces unnecessary overhead for a backend-focused API

## More Information

FastAPI documentation:
https://fastapi.tiangolo.com/