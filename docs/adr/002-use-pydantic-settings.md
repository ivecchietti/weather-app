---
status: accepted
date: 2026-05-13
decision-makers: Ivo Vecchiett
---

# Use pydantic-settings for configuration management

## Context and Problem Statement

The Weather App backend requires multiple configuration values such as database URLs, JWT secrets, API keys, and token settings. These values must not be hardcoded in the source code and should be easily configurable across development, testing, and production environments.

The project also requires validation to ensure the application fails fast if required environment variables are missing or invalid.

## Decision Drivers

* Sensitive values must not be committed to the repository
* Configuration should be environment-based
* Missing variables should fail at startup
* Type validation is required
* Easy local development with `.env` support
* Integration with FastAPI and Pydantic ecosystem

## Considered Options

* pydantic-settings
* python-dotenv with os.environ
* Manual environment variable parsing

## Decision Outcome

Chosen option: "pydantic-settings", because it provides typed configuration management with validation, automatic `.env` loading, and seamless integration with FastAPI and Pydantic.

### Consequences

* Good, because sensitive values remain outside the codebase
* Good, because configuration validation happens automatically at startup
* Good, because environment variables are strongly typed
* Good, because `.env` files simplify local development
* Good, because the configuration system integrates naturally with dependency injection patterns
* Neutral, because additional setup is required for CI/CD environment variables
* Bad, because introduces an additional dependency (`pydantic-settings`)

### Confirmation

The backend currently uses `BaseSettings` to manage:
- Database connection URL
- Weather API key
- JWT secret key
- JWT algorithm
- Token expiration settings

The application refuses to start if required configuration variables are missing.

## Pros and Cons of the Options

### pydantic-settings

* Good, because environment variables are automatically validated
* Good, because supports `.env` files natively
* Good, because integrates directly with Pydantic models
* Good, because typed configuration reduces runtime errors
* Neutral, because requires learning Pydantic Settings patterns
* Bad, because introduces one additional dependency

### python-dotenv with os.environ

* Good, because simple and lightweight
* Good, because widely used
* Bad, because no automatic validation
* Bad, because all variables are treated as strings
* Bad, because missing values fail only at runtime

### Manual environment variable parsing

* Good, because no dependencies required
* Bad, because repetitive boilerplate code
* Bad, because no type validation
* Bad, because error handling must be implemented manually
* Bad, because difficult to maintain as the project grows

## More Information

Pydantic Settings documentation:
https://docs.pydantic.dev/latest/concepts/pydantic_settings/