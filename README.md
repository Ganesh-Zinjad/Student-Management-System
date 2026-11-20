# Student Management System — FastAPI

A beginner-friendly Student Management System built using **FastAPI, PostgreSQL, SQLAlchemy, Pydantic, and Jinja2**.

This project is designed as a practical learning resource for developers who want to understand how backend applications work using FastAPI. The project demonstrates CRUD operations using important backend concepts through a working application.

## Features

- Add new student records.
- View student profiles.
- Search students using their admission number.
- Update existing student information.
- Delete student records.
- Display total registered students.
- Validate incoming data using Pydantic.
- Store student information in PostgreSQL using SQLAlchemy ORM.
- Dynamically render HTML pages using Jinja2.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming language |
| FastAPI | Backend web framework |
| PostgreSQL | Relational database |
| SQLAlchemy | ORM and database interaction |
| Pydantic | Data validation and serialization |
| Psycopg | PostgreSQL database driver |
| Jinja2 | Server-side HTML rendering |
| HTML, CSS, JavaScript | Frontend |


## Project Structure

```text
fastapi-student-management-system/
│
├── static/
│   ├── css/
│   │   ├── Admin.css
│   │   └── Profile.css
│   │
│   └── javascript/
│       ├── Admin.js
│       └── edit.js
│
├── templates/
│   ├── admin.html
│   ├── edit_student.html
│   └── profile.html
│
├── .env.example
├── .gitignore
├── database.py
├── main.py
├── models.py
├── schema.py
├── requirements.txt
├── README.md
└── LICENSE
```

### Understanding the Project Files

| File | Description |
|---|---|
| `main.py` | FastAPI application, routes, request handling, exception handling and Jinja2 integration. |
| `database.py` | Database connection, SQLAlchemy engine, session factory and database dependency. |
| `models.py` | SQLAlchemy ORM models representing database tables. |
| `schema.py` | Pydantic schemas for request validation and data serialization. |
| `templates/` | Jinja2 HTML templates. |
| `static/` | CSS and JavaScript files served by FastAPI. |

## Getting Started

Follow these instructions to run the project locally.

### 1. Prerequisites

Make sure you have installed:

- Python 3.10 or later (use the version supported by your dependencies).
- PostgreSQL.
- Git.
- Any code editor such as VS Code or VSCodium.

### 2. Clone the Repository

```bash
git clone https://github.com/Ganesh-Zinjad/fastapi-student-management-system.git
```

Navigate into the project directory:

```bash
cd fastapi-student-management-system
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it.

**Windows:**

```powershell
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the project root.

Use `.env.example` as a reference.

Configure your PostgreSQL credentials:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=student_management
DB_USER=postgres
DB_PASSWORD=your_password
```

### 6. Create the PostgreSQL Database

You must create the database and student table before
running the application.

### 7. Run the Application

```bash
uvicorn main:app --reload
```

The application will be available at:

```text
http://127.0.0.1:8000
```

Open the admin dashboard:

```text
http://127.0.0.1:8000/admin
```

**Note:** The application currently relies on the existing database table being available. Follow the database setup instructions in the documentation or create the table using your project's existing schema setup before running the application.

## Application Routes

The following routes are implemented in the application.

| HTTP Method | Endpoint | Description |
|---|---|---|
| GET | `/admin` | Displays the admin dashboard. |
| GET | `/profile/{admission_no}` | Displays a student's profile. |
| POST | `/admin/add_student` | Adds a new student. |
| GET | `/admin/search_student/{admission_no}` | Searches for a student. |
| DELETE | `/admin/delete_student/{admission_no}` | Deletes a student. |
| GET | `/admin/edit_student/` | Displays the student editing page. |
| PATCH | `/admin/update_student/{admission_no}` | Updates student information. |

## Backend Concepts Demonstrated

This project provides practical examples of the following concepts.

### 1. FastAPI Routing

Learn how to define API endpoints using decorators such as:

- `@app.get()`
- `@app.post()`
- `@app.patch()`
- `@app.delete()`

Understand how HTTP methods correspond to different operations.

### 2. Dependency Injection

Learn how FastAPI's `Depends()` works and how dependencies are used to provide database sessions to route functions.

Explore how `yield` and `finally` help manage database session lifecycles.

### 3. SQLAlchemy ORM

Understand Object Relational Mapping (ORM) and how Python classes represent database tables.

Explore:

- `create_engine()`
- `sessionmaker()`
- `declarative_base()`
- `Column()`
- `db.query()`
- `db.add()`
- `db.commit()`
- `db.refresh()`
- `db.delete()`

### 4. Pydantic Validation

Learn how Pydantic validates incoming request data.

Explore:

- `BaseModel`
- `Field()`
- `ConfigDict`
- `field_validator`
- `model_validator`
- `model_dump()`
- Partial update validation.

### 5. PostgreSQL Integration

Understand how a Python backend connects to PostgreSQL using SQLAlchemy and Psycopg.

### 6. Server-Side Rendering

Learn how FastAPI integrates with Jinja2 to render dynamic HTML pages using data retrieved from the database.

## Learning Resources

The following official documentation is useful when exploring the project:

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Jinja Documentation](https://jinja.palletsprojects.com/)

## Learning Roadmap

If you are new to FastAPI, I recommend exploring the project in this order:

1. Understand the project structure.
2. Explore FastAPI routes and HTTP methods.
3. Understand Pydantic request validation.
4. Explore SQLAlchemy models and ORM.
5. Understand database sessions and dependency injection.
6. Explore CRUD operations.
7. Understand Jinja2 templates and server-side rendering.
8. Trace the complete request lifecycle.

## Limitations

This is an educational project intended to demonstrate fundamental backend development concepts.

- Authentication and authorization are not implemented.
- The admin interface is not protected by user roles or permissions.
- The application is not intended for production deployment without additional security and reliability improvements.

## Future Improvements

Possible enhancements include:

- Authentication and authorization using JWT or session-based authentication.
- Modular architecture using FastAPI APIRouter.
- Service layer for separating business logic from routes.
- Database migrations using Alembic.
- Automated testing using Pytest.
- Docker-based deployment.
- Improved logging and error handling.

## Contributing

Suggestions, bug reports, and improvements are welcome!

If you are learning FastAPI, feel free to fork this repository, experiment with the code, and submit improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

**Built as a learning project to explore backend development with FastAPI.**