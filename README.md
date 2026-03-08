# secure-notes-api

Architecture and Security Design

The Secure Notes API is designed as a small but realistic example of a security-aware backend service. The application allows authenticated users to store and retrieve personal notes while ensuring that sensitive information is protected using modern security practices. The architecture intentionally emphasizes defensive design, clear data boundaries, and responsible credential management.

System Overview

The system consists of a REST API built with FastAPI, a lightweight and high-performance Python framework for building web services. The API exposes endpoints for user registration, authentication, and note management. Internally, the service separates authentication logic, encryption logic, database access, and API routing to maintain clean architectural boundaries.

At a high level, the workflow operates as follows:

A user registers or logs in using the authentication endpoints.

The system validates credentials and issues a signed JSON Web Token (JWT).

The client includes the token in future API requests.

Authenticated requests can create, retrieve, or delete notes.

Note content is encrypted before it is written to the database.

When a note is retrieved, the system decrypts the content before returning it to the user.

This flow ensures that authentication, authorization, and data protection occur at distinct stages of request processing.

Authentication Model

Authentication is implemented using JSON Web Tokens (JWT). After a successful login, the server generates a signed token that represents the authenticated user. The token includes a short expiration window and is verified on every protected API request.

Using token-based authentication provides several benefits:

Stateless authentication suitable for distributed systems

Clear separation between authentication and application logic

Reduced reliance on server-side session storage

Compatibility with modern API clients and microservices

The token payload contains the user identity and expiration timestamp, and the signature is verified using a server-side secret.

Password Security

User passwords are never stored in plaintext. Instead, they are processed using bcrypt hashing through the passlib library. Bcrypt is intentionally computationally expensive, which significantly reduces the effectiveness of brute-force password attacks.

The authentication workflow follows these steps:

The user submits a password during registration.

The password is hashed using bcrypt.

The hash is stored in the database.

During login, the submitted password is verified against the stored hash.

Because bcrypt includes built-in salting, identical passwords do not produce identical hashes, which helps mitigate rainbow table attacks.

Encryption at Rest

One of the primary goals of this project is to demonstrate application-level encryption of sensitive data.

The content of each note is encrypted using the Fernet symmetric encryption scheme provided by the cryptography library. This encryption occurs before the data is written to the database.

The workflow is as follows:

A user submits note content.

The application encrypts the content using a Fernet key.

The encrypted ciphertext is stored in the database.

When the note is retrieved, the ciphertext is decrypted before returning the response.

This approach ensures that even if the database is accessed directly, the stored note contents remain unreadable without the encryption key.

In a production environment, encryption keys should be managed using a dedicated key management system such as:

AWS KMS

Azure Key Vault

HashiCorp Vault

Hardware Security Modules (HSMs)

For demonstration purposes, this project loads the encryption key from environment configuration.

Database Design

The service uses SQLAlchemy as the Object Relational Mapper (ORM) to interact with the database. SQLAlchemy allows the application to define structured models for users and notes while keeping database access organized and maintainable.

The core models include:

User

Unique username

Password hash

Relationship to stored notes

Note

Note identifier

Owner identifier

Encrypted note content

Title metadata

SQLite is used as the default database to keep the project easy to run locally, but the architecture allows straightforward migration to PostgreSQL or other production-grade databases.

API Security Controls

Several defensive security practices are implemented throughout the service:

Credential Protection
Passwords are hashed using bcrypt and never stored in plaintext.

Token-Based Authorization
All note-related endpoints require a valid JWT access token.

Encryption at Rest
Sensitive note content is encrypted before database storage.

Security Headers
Basic HTTP security headers are applied to reduce common browser-based attack surfaces.

Environment-Based Secrets
Sensitive configuration such as signing keys and encryption keys are loaded from environment variables rather than embedded in the source code.

Project Structure

The repository is organized to separate responsibilities clearly across modules.

app/
  config.py        Application configuration
  db.py            Database initialization
  models.py        Database models
  schemas.py       API request/response schemas
  security.py      Authentication and encryption logic
  routes_auth.py   Authentication endpoints
  routes_notes.py  Note management endpoints
  main.py          FastAPI application entry point

This separation makes the code easier to maintain, test, and extend.

Testing and Validation

The project includes automated tests that validate authentication and note management workflows. These tests confirm that:

Users can register and log in successfully

JWT authentication protects note endpoints

Notes are stored and retrieved correctly

Deletion operations behave as expected

Automated testing helps ensure the API behaves consistently as new features are added.

Intended Use

This project is intended as a learning and portfolio example demonstrating secure backend design patterns. It is not intended to be deployed as a production system without additional controls such as:

key management services

rate limiting

audit logging

database migrations

monitoring and alerting

infrastructure hardening

However, the architectural patterns used here mirror those commonly implemented in real-world secure API services.
## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

cp .env.example .env
uvicorn app.main:app --reload

## Run with Docker

cp .env.example .env
docker compose up --build
Security notes (intended design)
