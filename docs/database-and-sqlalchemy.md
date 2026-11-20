# Database and SQLAlchemy ORM

## 1. What is SQLAlchemy?

SQLAlchemy is a Python SQL toolkit and Object Relational Mapper (ORM).

It allows Python applications to interact with relational databases such as PostgreSQL, MySQL, and SQLite.

Without an ORM, you would generally write SQL queries manually:

```python
cursor.execute(
    "SELECT * FROM student WHERE admission_no = %s",
    ("ADM101",)
)
```

With SQLAlchemy ORM, you can perform similar operations using Python objects:

```python
student = db.query(Student).filter(
    Student.admission_no == "ADM101"
).first()
```

SQLAlchemy translates ORM operations into SQL queries and communicates with the database.

### What is an ORM?

ORM stands for Object Relational Mapping.

It maps:

- Database tables to Python classes.
- Database rows to Python objects.
- Database columns to Python attributes.

For example, your PostgreSQL table:

```sql
CREATE TABLE student (
    id SERIAL PRIMARY KEY,
    admission_no VARCHAR(10) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    age INTEGER NOT NULL,
    course VARCHAR(100) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    phone_no VARCHAR(15) NOT NULL,
    cgpa FLOAT NOT NULL,
    passing_year INTEGER NOT NULL
);
```

Is represented by a Python class in `models.py`.

## 2. Understanding `models.py`

Your `models.py` file defines the structure of the database table using a Python class.

A simplified version looks like this:

```python
from sqlalchemy import Column, Integer, String, Float
from database import Base

class Student(Base):
    __tablename__ = "student"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    admission_no = Column(String(10), unique=True, nullable=False, index=True)

    name = Column(String(100), nullable=False)

    age = Column(Integer, nullable=False)

    course = Column(String(100), nullable=False)

    gender = Column(String(10), nullable=False)

    phone_no = Column(String(15), nullable=False)

    cgpa = Column(Float, nullable=False)

    passing_year = Column(Integer, nullable=False)
```

Let's understand the important parts.

### `Base`

```python
from database import Base
```

`Base` is the declarative base class created in `database.py`.

SQLAlchemy uses it to register ORM model classes and their table definitions.

### `__tablename__`

```python
__tablename__ = "student"
```

This tells SQLAlchemy that the `Student` class represents the database table named `student`.

### `Column()`

```python
name = Column(String(100), nullable=False)
```

This defines a database column.

- `String(100)` specifies a string column with a maximum length of 100 characters.
- `nullable=False` means the database column cannot contain NULL values.

### Primary key

```python
id = Column(Integer, primary_key=True, index=True, autoincrement=True)
```

A primary key uniquely identifies each row in a table.

Your application uses `id` as its primary key, while `admission_no` is also unique and is used to identify students in the application routes.

### Unique constraint

```python
admission_no = Column(String(10), unique=True, nullable=False)
```

The `unique=True` option prevents two student records from having the same admission number.

This constraint is enforced by PostgreSQL, not just by Python validation.

## 3. Understanding `database.py`

Your `database.py` file is responsible for configuring the database connection and creating SQLAlchemy sessions.

The important components are:

1. Database URL
2. Engine
3. Declarative Base
4. Session factory
5. Database dependency

### Database URL

Your application reads database credentials from environment variables:

```python
DATABASE_URL = (
    f"postgresql+psycopg://{user}:{password}@{host}:{port}/{name}"
)
```

This URL tells SQLAlchemy:

- Database type: PostgreSQL
- Driver: Psycopg 3
- Host: Database server address
- Port: PostgreSQL port
- Database name: Target database
- Username and password: Database credentials

Your project uses `python-dotenv` to load these values from `.env`.

### Engine

```python
engine = create_engine(DATABASE_URL)
```

The SQLAlchemy Engine is responsible for managing database connectivity.

It provides the underlying connections that SQLAlchemy sessions use to communicate with PostgreSQL.

The engine also manages a connection pool so that database connections can be reused rather than creating a completely new connection for every operation.

Creating the engine does not normally establish a database connection immediately. Connections are generally acquired when an operation needs one.

### Declarative Base

```python
Base = declarative_base()
```

This creates the base class used by your ORM models.

Your `Student` model inherits from this Base:

```python
class Student(Base):
    ...
```

This allows SQLAlchemy to register the model's table metadata.

### Session factory

```python
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
```

`sessionmaker()` creates a factory for SQLAlchemy Session objects.

Calling:

```python
db = SessionLocal()
```

creates a new session.

The configuration means:

- `autocommit=False`: Changes are not automatically committed; you explicitly call `db.commit()`.
- `autoflush=False`: SQLAlchemy does not automatically flush pending changes before every query.
- `bind=engine`: Sessions use the configured database engine.

A session is a unit of work that tracks ORM objects and manages database transactions.

## 4. Understanding SQLAlchemy Session

A SQLAlchemy Session is the main interface your application uses to work with ORM objects.

For example:

```python
student = db.query(models.Student).first()
```

The `db` variable is a Session object.

You use it to:

- Retrieve records.
- Add new records.
- Update existing records.
- Delete records.
- Commit transactions.
- Roll back failed transactions.

A session is not the same thing as a database connection. It manages ORM state and transactions, and obtains connections from the engine when needed.

## 5. Retrieving records

Your application uses the following pattern to find a student:

```python
student = db.query(models.Student).filter(
    models.Student.admission_no == admission_no
).first()
```

Let's understand each method.

### `query()`

```python
db.query(models.Student)
```

Creates an ORM query targeting the `Student` model.

### `filter()`

```python
.filter(models.Student.admission_no == admission_no)
```

Adds a condition to the query.

It is conceptually similar to this SQL statement:

```sql
SELECT *
FROM student
WHERE admission_no = 'ADM101';
```

### `first()`

```python
.first()
```

Executes the query and returns the first matching result.

If no record matches, it returns `None`.

This is why your routes check whether the returned student exists:

```python
if not student:
    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )
```

### Counting records

Your admin dashboard uses:

```python
total_students = db.query(models.Student).count()
```

This counts the number of matching records.

Conceptually, it performs:

```sql
SELECT COUNT(*) FROM student;
```

Note: Your project uses SQLAlchemy's legacy `Query` interface through `db.query()`. It remains supported in SQLAlchemy 2.x. SQLAlchemy 2.x also provides the newer `select()` API, which is recommended for new code.

## 6. Adding a new student

Your application uses the following operations:

```python
new_student = models.Student(**student.model_dump())

db.add(new_student)

db.commit()

db.refresh(new_student)
```

Let's understand each operation.

### Step 1: Creating an ORM object

```python
new_student = models.Student(**student.model_dump())
```

`student` is a Pydantic object received from the request.

`model_dump()` converts it into a Python dictionary.

The `**` operator unpacks the dictionary into keyword arguments for the `Student` constructor.

For example:

```python
student_data = {
    "admission_no": "ADM101",
    "name": "Rahul",
    "age": 20,
    "course": "IT",
    "gender": "male",
    "phone_no": "0000000000",
    "cgpa": 8.5,
    "passing_year": 2027
}

new_student = models.Student(**student_data)
```

This creates a Python ORM object. It does not immediately insert a database row.

### Step 2: Adding the object to the session

```python
db.add(new_student)
```

This tells SQLAlchemy to track the new object.

The object becomes pending in the current session.

It is not necessarily stored in PostgreSQL yet.

### Step 3: Committing the transaction

```python
db.commit()
```

This commits the current transaction.

SQLAlchemy flushes pending changes to the database before committing.

PostgreSQL then persists the changes if the transaction succeeds.

Conceptually, the operation performs an INSERT:

```sql
INSERT INTO student (
    admission_no,
    name,
    age,
    course,
    gender,
    phone_no,
    cgpa,
    passing_year
)
VALUES (
    'ADM101',
    'Rahul',
    20,
    'IT',
    'male',
    '00000000000',
    8.5,
    2027
);
```

### Step 4: Refreshing the object

```python
db.refresh(new_student)
```

This reloads the object's database-backed values.

It is useful when the database generates values, such as an automatically generated primary key.

For example, after insertion, PostgreSQL may generate:

```text
id = 1
```

Refreshing allows the ORM object to reflect the database's current values.

## 7. Updating an existing student

Your project uses:

```python
update_data = student.model_dump(exclude_unset=True)

for key, value in update_data.items():
    setattr(existing_student, key, value)

db.commit()
```

Let's understand this.

### `model_dump(exclude_unset=True)`

This converts the Pydantic model into a dictionary containing only fields explicitly supplied by the client.

For example, if the request contains:

```json
{
    "cgpa": 9.1
}
```

The resulting dictionary is:

```python
{
    "cgpa": 9.1
}
```

It does not include fields that the client omitted.

### `setattr()`

```python
setattr(existing_student, key, value)
```

`setattr()` is a built-in Python function that assigns a value to an object's attribute.

For example:

```python
setattr(existing_student, "cgpa", 9.1)
```

Is equivalent to:

```python
existing_student.cgpa = 9.1
```

SQLAlchemy tracks the changed attribute.

### Commit

```python
db.commit()
```

This persists the update to PostgreSQL.

Conceptually:

```sql
UPDATE student
SET cgpa = 9.1
WHERE admission_no = 'ADM101';
```

## 8. Deleting a student

Your project uses:

```python
db.delete(student)
db.commit()
```

### `delete()`

```python
db.delete(student)
```

Marks the ORM object for deletion in the current session.

### `commit()`

```python
db.commit()
```

Commits the deletion to the database.

Conceptually:

```sql
DELETE FROM student
WHERE admission_no = 'ADM101';
```

The deletion is persisted only when the transaction commits successfully.

## 9. Transactions: Commit and Rollback

A database transaction is a group of database operations treated as a logical unit.

SQLAlchemy uses transactions to maintain consistency when performing database operations.

### Commit

```python
db.commit()
```

Commits the current transaction.

If the transaction succeeds, its changes become persistent.

### Rollback

```python
db.rollback()
```

Rolls back the current transaction.

It is particularly important when a database operation fails.

For example:

```python
try:
    db.add(new_student)
    db.commit()

except IntegrityError:
    db.rollback()
    raise
```

Suppose a student with admission number `ADM101` already exists.

Because `admission_no` has a unique constraint, PostgreSQL rejects the duplicate insertion.

The failed transaction must be rolled back before the session can be used for further database operations.

Your add-student route uses this approach when it catches `IntegrityError`.

### Why are transactions important?

Consider a registration operation that must insert a student and a related record.

If the first operation succeeds but the second fails, the application may be left with incomplete data.

Transactions allow related operations to be committed together or rolled back together.

## 10. Understanding the database lifecycle in your application

Your application follows this general process:

1. A request reaches a FastAPI route.
2. FastAPI provides a SQLAlchemy Session through `Depends(get_db)`.
3. The route performs database operations using the session.
4. SQLAlchemy communicates with PostgreSQL through the engine.
5. The route commits or rolls back its transaction as necessary.
6. The response is returned.
7. The dependency cleanup closes the session.

This separation makes database access easier to organize and maintain.

## 11. Important distinction: ORM models vs database tables

Your project manually created its PostgreSQL table through pgAdmin.

Defining this class:

```python
class Student(Base):
    __tablename__ = "student"
```

does not automatically create the table.

The ORM model describes the table structure to SQLAlchemy, but creating or changing the actual database schema requires a separate operation.

SQLAlchemy supports table creation through:

```python
Base.metadata.create_all(bind=engine)
```

However, your project currently uses a manually created table.

For larger applications, database migration tools such as Alembic are generally preferred because they help track and apply schema changes over time.

## 12. Key takeaways

- SQLAlchemy is an ORM that maps Python classes to database tables.
- `models.py` defines the database structure.
- `database.py` configures the engine and session factory.
- A Session manages ORM objects and transactions.
- `query()`, `filter()`, and `first()` retrieve records.
- `add()` stages a new object in the session.
- `commit()` persists transaction changes.
- `refresh()` reloads an object's database-backed values.
- `delete()` marks an object for deletion.
- `rollback()` cancels the current failed transaction.
- ORM model definitions do not automatically create or migrate database tables.

## Further reading

- [SQLAlchemy — ORM Quick Start](https://docs.sqlalchemy.org/en/20/orm/quickstart.html)
- [SQLAlchemy — Session Basics](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)
- [SQLAlchemy — Engine Configuration](https://docs.sqlalchemy.org/en/20/core/engines.html)
- [SQLAlchemy — ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)
- [PostgreSQL — SQL Commands](https://www.postgresql.org/docs/current/sql-commands.html)