# Database Dependency Injection in FastAPI

## 1. What is dependency injection?

Dependency Injection (DI) is a software design technique in which an object or function receives the resources it needs from an external source instead of creating those resources itself.

For example, consider an API route that needs a database session.

Without dependency injection, the route might create its own session:

```python
@app.get("/students")
def get_students():
    db = SessionLocal()

    students = db.query(Student).all()

    db.close()
    return students
```

This works for a simple example, but it has problems:

- Every route must repeat the database session creation logic.
- Every route must remember to close the session.
- Handling errors and cleanup becomes repetitive.
- Testing routes becomes more difficult.

FastAPI provides dependency injection to solve this problem.

## 2. Understanding `Depends()`

FastAPI provides `Depends()` to declare that a route requires a dependency.

For example:

```python
from fastapi import Depends

@app.get("/students")
def get_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    return students
```

Let's understand this declaration:

```python
db: Session = Depends(get_db)
```

- `db` is the parameter that receives the database session.
- `Session` is the SQLAlchemy session type.
- `Depends()` tells FastAPI that this parameter must be provided by a dependency.
- `get_db` is the dependency function responsible for providing the session.

You do not manually call `get_db()` inside the route. FastAPI calls it and provides its result to the route.

## 3. Understanding `get_db()`

Your project defines the database dependency in `database.py`.

```python
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
```

Let's understand each part.

### Creating a database session

```python
db = SessionLocal()
```

`SessionLocal` is a SQLAlchemy session factory created using `sessionmaker()`.

Calling it creates a new SQLAlchemy `Session` object.

A SQLAlchemy `Session` manages database operations and tracks changes to ORM objects. It is not the same thing as a raw database connection.

### Why use `yield` instead of `return`?

```python
yield db
```

A normal function using `return` finishes execution immediately.

A generator function using `yield` can provide a value and pause execution. It can continue executing later.

FastAPI uses this behavior to manage the dependency's lifecycle:

1. FastAPI calls `get_db()`.
2. The function creates a database session.
3. `yield db` provides the session to the route.
4. The route executes its database operations.
5. After the request's dependency lifecycle finishes, FastAPI resumes the generator.
6. The cleanup code runs.

### Why use `finally`?

```python
finally:
    db.close()
```

The `finally` block executes during cleanup, including when an exception occurs.

This ensures that the SQLAlchemy session is closed even if the route encounters an error.

Closing a SQLAlchemy session releases its transactional resources and returns any checked-out connection to the connection pool when appropriate. It does not normally shut down the PostgreSQL server connection itself.

## 4. How dependency injection works in your project

Consider this route from your application:

```python
@app.get("/admin")
def admin_page(
    request: Request,
    db: Session = Depends(get_db)
):
    total_students = db.query(models.Student).count()

    return templates.TemplateResponse(
        "admin.html",
        {
            "request": request,
            "total_students": total_students,
            "student": None
        }
    )
```

When a browser requests `GET /admin`, the following sequence occurs:

1. FastAPI receives the HTTP request.
2. FastAPI sees `Depends(get_db)` in the route parameters.
3. FastAPI executes `get_db()` and obtains a database session.
4. FastAPI passes that session into the `db` parameter.
5. The route uses the session to count the students.
6. The route returns the rendered HTML response.
7. FastAPI runs the dependency cleanup code.
8. `db.close()` releases the session's resources.

The same pattern can be used in other routes that need database access.

## 5. Why is this useful?

| Benefit | Explanation |
|---|---|
| Code reuse | Database session creation is written once. |
| Automatic cleanup | FastAPI manages the dependency's cleanup lifecycle. |
| Cleaner routes | Routes focus on application logic rather than session setup. |
| Easier testing | Dependencies can be overridden during tests. |
| Separation of concerns | Database setup stays separate from route logic. |

## 6. Does `get_db()` automatically commit changes?

No.

Dependency injection provides the database session. It does not automatically commit your database operations.

For example:

```python
db.add(new_student)
db.commit()
```

- `db.add()` stages the new object in the session.
- `db.commit()` commits the transaction to the database.

If you only call `db.add()` and never commit, the new record is not guaranteed to be persisted.

Similarly, `db.close()` is not a substitute for `db.commit()`.

In your project, the route responsible for adding a student explicitly commits the transaction and rolls it back when an error occurs.

## 7. Dependency injection and testing

One useful feature of FastAPI is that dependencies can be overridden during testing.

For example, you can provide a test database session instead of using your normal PostgreSQL database.

Conceptually:

```python
app.dependency_overrides[get_db] = override_get_db
```

Here, `override_get_db` is another dependency function that provides a test database session.

This makes it possible to test API routes without using your regular development database.

## 8. Key takeaways

- Dependency injection provides a route with the resources it needs.
- `Depends()` declares a dependency in FastAPI.
- `get_db()` creates and provides a SQLAlchemy session.
- `yield` provides the session and allows cleanup code to run afterward.
- `finally` ensures that session cleanup is performed.
- `db.close()` does not mean `db.commit()`.
- FastAPI also supports dependency overrides, which are useful for testing.

## Further reading

- [FastAPI — Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [FastAPI — Dependencies with yield](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/)
- [SQLAlchemy — Session Basics](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)