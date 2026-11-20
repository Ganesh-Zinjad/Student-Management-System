# Pydantic and Request Validation in FastAPI

## 1. What is Pydantic?

Pydantic is a Python library used for data validation, parsing, and serialization.

In a web application, clients send data to the backend. That data cannot always be trusted.

For example, an administrator might submit the following student information:

```json
{
    "admission_no": "ADM101",
    "name": "Rahul",
    "age": 20,
    "course": "Information Technology",
    "gender": "male",
    "phone_no": "9876543210",
    "cgpa": 8.5,
    "passing_year": 2027
}
```

But what if the client sends:

- An age of `"twenty"` instead of a number?
- A CGPA of `15`, when the maximum allowed value is `10`?
- A missing admission number?
- An invalid gender value?

Your backend needs a way to validate incoming data before processing it.

Pydantic provides this functionality.

## 2. What is a Pydantic model?

A Pydantic model is a Python class that inherits from `BaseModel`.

It defines the expected structure and validation rules for data.

Example:

```python
from pydantic import BaseModel

class StudentBase(BaseModel):
    admission_no: str
    name: str
    age: int
    course: str
    gender: str
    phone_no: str
    cgpa: float
    passing_year: int
```

This model tells Pydantic that student data must contain these fields with the specified types.

Pydantic validates the supplied data when a model instance is created.

## 3. Field validation and constraints

Pydantic supports constraints beyond basic Python types.

For example:

```python
from pydantic import BaseModel, Field, ConfigDict
from typing import Literal

class StudentBase(BaseModel):

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True
    )

    admission_no: str = Field(min_length=1, max_length=10)

    name: str = Field(min_length=2, max_length=100)

    age: int = Field(ge=5, le=100)

    course: str = Field(min_length=2, max_length=100)

    gender: Literal["male", "female", "other"]

    phone_no: str = Field(
        min_length=8,
        max_length=15,
        pattern=r"^\+?[1-9]\d{7,14}$"
    )

    cgpa: float = Field(ge=0, le=10)

    passing_year: int = Field(ge=1900, le=2100)
```

Let's understand the important options.

### `Field()`

`Field()` allows you to define additional validation rules for a field.

For example:

```python
age: int = Field(ge=5, le=100)
```

This means:

- `ge=5`: Value must be greater than or equal to 5.
- `le=100`: Value must be less than or equal to 100.

Other useful constraints include:

| Constraint | Meaning |
|---|---|
| `min_length` | Minimum string length |
| `max_length` | Maximum string length |
| `ge` | Greater than or equal to |
| `le` | Less than or equal to |
| `gt` | Greater than |
| `lt` | Less than |
| `pattern` | Regular expression pattern |

### `Literal`

```python
gender: Literal["male", "female", "other"]
```

`Literal` restricts a field to a predefined set of values.

For example, `"male"` is accepted, but `"unknown"` is rejected.

### `ConfigDict`

```python
model_config = ConfigDict(
    extra="forbid",
    str_strip_whitespace=True
)
```

This configures how Pydantic handles model data.

- `extra="forbid"` rejects unexpected fields.
- `str_strip_whitespace=True` removes leading and trailing whitespace from strings before validation.

For example, `" Rahul "` becomes `"Rahul"`.

## 4. How FastAPI uses Pydantic

FastAPI integrates directly with Pydantic.

Consider your add-student endpoint:

```python
@app.post("/admin/add_student")
def add_student(
    student: StudentBase,
    db: Session = Depends(get_db)
):
    ...
```

Here:

```python
student: StudentBase
```

tells FastAPI that the request body should be validated using the `StudentBase` model.

When a client sends a request:

1. FastAPI receives the JSON body.
2. FastAPI reads the expected Pydantic model.
3. Pydantic validates the incoming data.
4. If validation succeeds, FastAPI creates a `StudentBase` object.
5. That object is passed to the route function.
6. If validation fails, FastAPI returns a validation error, normally with HTTP status `422`.

This means your route does not need to manually validate every field.

## 5. Why separate request schemas from SQLAlchemy models?

Your project has two different types of models:

- Pydantic schemas in `schema.py`
- SQLAlchemy models in `models.py`

Although both describe student data, they serve different purposes.

### Pydantic schema

A Pydantic schema defines the structure and validation rules for data entering or leaving your application.

Example:

```python
class StudentBase(BaseModel):
    admission_no: str
    name: str
    age: int
    course: str
    gender: Literal["male", "female", "other"]
    phone_no: str
    cgpa: float
    passing_year: int
```

### SQLAlchemy model

A SQLAlchemy model represents the database table and its columns.

Example:

```python
class Student(Base):
    __tablename__ = "student"

    id = Column(Integer, primary_key=True)
    admission_no = Column(String(10), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
```

### Main differences

| Pydantic schema | SQLAlchemy model |
|---|---|
| Validates application data | Represents database structure |
| Used for request validation | Used for database operations |
| Inherits from `BaseModel` | Inherits from SQLAlchemy `Base` |
| Defines validation constraints | Defines columns and database constraints |
| Converts data into Python objects | Maps Python objects to database rows |

Keeping them separate makes your application easier to maintain.

For example, a field can be required when creating a student but optional when updating one.

## 6. Why have separate schemas for creating and updating?

Your application uses `StudentBase` for adding students and `StudentPatch` for updating them.

This is useful because creating and updating a resource have different requirements.

### StudentBase — Creating a student

When creating a student, all required information must be provided.

For example:

```python
class StudentBase(BaseModel):
    admission_no: str
    name: str
    age: int
    course: str
    gender: Literal["male", "female", "other"]
    phone_no: str
    cgpa: float
    passing_year: int
```

If the client omits a required field, validation fails.

### StudentPatch — Updating a student

When updating a student, the client may only want to change one field.

For example:

```json
{
    "cgpa": 9.1
}
```

It would be inconvenient to require the client to send every student field just to update the CGPA.

Therefore, update schemas make fields optional.

A simplified example:

```python
class StudentPatch(BaseModel):
    name: str | None = None
    age: int | None = None
    course: str | None = None
    gender: Literal["male", "female", "other"] | None = None
    phone_no: str | None = None
    cgpa: float | None = None
    passing_year: int | None = None
```

Notice that `admission_no` is not included.

Your application uses admission number to identify a student, and it should not be changed through this update endpoint.

## 7. Understanding `model_dump()`

Pydantic provides `model_dump()` to convert a model instance into a Python dictionary.

Example:

```python
student_data = student.model_dump()
```

Suppose `student` contains:

```python
StudentBase(
    admission_no="ADM101",
    name="Rahul",
    age=20,
    course="IT",
    gender="male",
    phone_no="000000000000",
    cgpa=8.5,
    passing_year=2027
)
```

Calling `model_dump()` produces a dictionary:

```python
{
    "admission_no": "ADM101",
    "name": "Rahul",
    "age": 20,
    "course": "IT",
    "gender": "male",
    "phone_no": "0000000000",
    "cgpa": 8.5,
    "passing_year": 2027
}
```

Your application uses this when creating a SQLAlchemy object:

```python
new_student = models.Student(**student.model_dump())
```

The dictionary is unpacked into keyword arguments for the SQLAlchemy model constructor.

## 8. Understanding `exclude_unset=True`

This is particularly important for your PATCH endpoint.

Consider:

```python
update_data = student.model_dump(exclude_unset=True)
```

The `exclude_unset=True` argument tells Pydantic to include only fields that were explicitly provided when the model was created.

Suppose the client sends:

```json
{
    "cgpa": 9.1
}
```

Without `exclude_unset=True`, the dictionary could also contain the default `None` values of omitted fields.

With `exclude_unset=True`, the result is:

```python
{
    "cgpa": 9.1
}
```

This prevents omitted fields from unintentionally overwriting existing database values.

### Difference between `exclude_unset` and `exclude_none`

These options are different:

- `exclude_unset=True`: Excludes fields the client did not provide.
- `exclude_none=True`: Excludes fields whose value is `None`.

For example, if a client explicitly sends:

```json
{
    "cgpa": null
}
```

Then `exclude_unset=True` retains the field because it was provided.

If your schema does not allow `None` as a valid CGPA, validation rejects that request.

This distinction is important when designing PATCH endpoints.

## 9. Understanding Pydantic validation errors

Suppose your application expects:

```python
age: int = Field(ge=5, le=100)
```

But the client sends:

```json
{
    "age": 150
}
```

Pydantic rejects the value because it exceeds the maximum allowed age.

FastAPI returns a response similar to:

```json
{
    "detail": [
        {
            "type": "less_than_equal",
            "loc": ["body", "age"],
            "msg": "Input should be less than or equal to 100",
            "input": 150,
            "ctx": {
                "le": 100
            }
        }
    ]
}
```

The response tells the client:

- Where the validation failed.
- Which field caused the problem.
- Why the value was rejected.

The exact error details can vary depending on the input and Pydantic version.

## 10. Understanding custom validation

Sometimes built-in field constraints are not sufficient.

Pydantic supports custom validators.

For example:

```python
from pydantic import BaseModel, model_validator

class StudentPatch(BaseModel):
    name: str | None = None
    age: int | None = None

    @model_validator(mode="after")
    def check_at_least_one_field(self):
        if not self.model_fields_set:
            raise ValueError("At least one field must be provided")

        return self
```

Here:

- `model_validator` defines validation for the entire model.
- `mode="after"` runs the validator after the model's fields have been validated.
- `self.model_fields_set` contains the fields explicitly supplied during model creation.
- If no fields were supplied, validation fails.

This is useful for PATCH requests because an empty update request should not silently succeed.

## 11. Important: Keep validation rules consistent

Your Pydantic schemas and SQLAlchemy models should agree with your actual database schema.

For your PostgreSQL table:

| Field | Database definition | Suggested application validation |
|---|---|---|
| admission_no | VARCHAR(10) | 1–10 characters |
| name | VARCHAR(100) | 2–100 characters |
| age | INTEGER | 5–100 |
| course | VARCHAR(100) | 2–100 characters |
| gender | VARCHAR(10) | Allowed gender values |
| phone_no | VARCHAR(15) | 8–15 characters |
| cgpa | FLOAT | 0–10 |
| passing_year | INTEGER | 1900–2100 |

The database enforces its own constraints, while Pydantic validates incoming application data.

Both layers are important.

For example, Pydantic can validate that an admission number is no longer than 10 characters, while PostgreSQL's unique constraint prevents duplicate admission numbers.

## 12. Key takeaways

- Pydantic validates and parses application data.
- FastAPI automatically integrates Pydantic with request bodies.
- `BaseModel` is the foundation of Pydantic models.
- `Field()` defines additional validation constraints.
- `Literal` restricts a field to specific values.
- `model_dump()` converts a Pydantic object into a dictionary.
- `exclude_unset=True` is useful for partial updates.
- Custom validators handle validation rules that built-in constraints cannot express conveniently.
- Pydantic schemas and SQLAlchemy models serve different purposes.
- Database constraints provide an additional layer of data integrity.

## Further reading

- [Pydantic — Models](https://docs.pydantic.dev/latest/concepts/models/)
- [Pydantic — Fields](https://docs.pydantic.dev/latest/concepts/fields/)
- [Pydantic — Validators](https://docs.pydantic.dev/latest/concepts/validators/)
- [Pydantic — Serialization](https://docs.pydantic.dev/latest/concepts/serialization/)
- [FastAPI — Request Body](https://fastapi.tiangolo.com/tutorial/body/)