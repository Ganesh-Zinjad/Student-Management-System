# Project Architecture

## 1. Introduction

This document explains the architecture of the Student Management System and how its different components interact.

The application follows a simple backend architecture using FastAPI, SQLAlchemy ORM, Pydantic and PostgreSQL.

The primary objective is to understand how a browser communicates with a backend server and how the backend interacts with a database.

## 2. Application Architecture

The application consists of four major components:

1. Frontend
2. Backend
3. Data validation
4. Database

### Frontend

The frontend is built using HTML, CSS and JavaScript.

- HTML defines the structure of web pages.
- CSS handles the appearance and styling.
- JavaScript handles user interactions and sends HTTP requests to the backend.

Jinja2 is used to dynamically render HTML pages using data received from the backend.

### Backend

FastAPI handles incoming HTTP requests.

It is responsible for:

- Defining application routes.
- Processing incoming requests.
- Validating request data using Pydantic.
- Performing database operations.
- Handling errors.
- Returning responses to the frontend.

### Data Validation

Pydantic schemas define the expected structure of incoming data.

For example, when adding a student, the backend validates fields such as name, age, course, gender and CGPA before processing the request.

### Database

PostgreSQL stores student records.

SQLAlchemy ORM allows the application to interact with PostgreSQL using Python objects instead of writing SQL queries manually for every operation.

## 3. Understanding the Request Lifecycle

Consider the operation of adding a new student.

The following steps take place:

1. An administrator fills in the student registration form.
2. JavaScript collects the form data.
3. JavaScript sends an HTTP POST request to `/admin/add_student`.
4. FastAPI receives the request.
5. Pydantic validates the incoming data using the `StudentBase` schema.
6. FastAPI resolves the database dependency using `Depends(get_db)`.
7. The route creates a SQLAlchemy Student object.
8. `db.add()` adds the object to the database session.
9. `db.commit()` commits the transaction.
10. The backend returns a JSON response.
11. JavaScript processes the response and updates the interface.

## 4. Role of Each Python File

### main.py

This is the entry point of the FastAPI application.

It contains:

- FastAPI application initialization.
- Application routes.
- HTTP request handling.
- Exception handling.
- Jinja2 template configuration.
- Static file configuration.

### database.py

This file manages database connectivity.

It defines:

- Database connection URL.
- SQLAlchemy engine.
- Session factory.
- Database dependency.

The `get_db()` function provides database sessions to route functions.

### models.py

This file defines SQLAlchemy ORM models.

The Student class represents the student table in PostgreSQL.

Each class attribute corresponds to a database column.

### schema.py

This file defines Pydantic schemas.

Schemas specify what data the application expects from clients and which validation rules should be applied.

They are separate from SQLAlchemy models because database representation and API data validation serve different purposes.

## 5. ORM Models vs Pydantic Schemas

These two concepts are particularly important.

**SQLAlchemy Model:**

Represents the database structure and is used to interact with database records.

**Pydantic Schema:**

Represents the expected structure of data received or returned by the application.

For example:

- `models.Student` represents a student record in PostgreSQL.
- `schema.StudentBase` validates incoming student registration data.
- `schema.StudentPatch` validates partial update requests.

Keeping these responsibilities separate makes backend applications easier to maintain.

## 6. Important Architectural Concepts

This project demonstrates:

- Separation of database models and validation schemas.
- Dependency injection for database session management.
- HTTP methods for CRUD operations.
- Exception handling using HTTPException.
- Database transaction handling.
- Server-side rendering using Jinja2.
- Frontend and backend communication using HTTP.

## 7. Current Architectural Limitations

The application is intentionally kept simple for educational purposes.

Currently, routes and application initialization are maintained in `main.py`.

As an application grows, it can be organized into separate routers, service layers and additional modules.

This project provides a foundation for understanding that evolution.