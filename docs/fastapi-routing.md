# FastAPI Routing and HTTP Methods

## 1. What is an API route?

A route defines how a server responds when a client sends an HTTP request to a particular URL.

For example, when a browser requests:

```http
GET /admin
```

FastAPI identifies the matching route and executes its associated Python function.

In FastAPI, routes are commonly defined using decorators:

```python
@app.get("/admin")
def admin_page():
    return {"message": "Welcome to Admin Page"}
```

Let's understand this code:

- `@app.get()` registers a route that accepts HTTP GET requests.
- `"/admin"` is the URL path.
- `admin_page()` is the function that handles the request.
- The returned dictionary is automatically converted into a JSON response.

## 2. Understanding HTTP methods

HTTP methods describe the operation a client wants to perform on a resource.

Your Student Management System uses the following methods:

| HTTP method | Purpose | Project example |
|---|---|---|
| GET | Retrieve information | Display student records |
| POST | Create a resource | Add a student |
| PATCH | Partially update a resource | Update student details |
| DELETE | Delete a resource | Delete a student |

### GET — Retrieve data

GET requests are used to retrieve information from the server.

Example:

```python
@app.get("/admin")
def admin_page():
    return {"message": "Admin page"}
```

A browser can access this endpoint by visiting:

```http
GET /admin
```

GET requests should not be used to perform operations that modify server-side data.

### POST — Create data

POST requests are commonly used to submit data to the server.

Your application uses POST to add students:

```python
@app.post("/admin/add_student")
def add_student(student: StudentBase, db: Session = Depends(get_db)):
    new_student = models.Student(**student.model_dump())

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return {"message": "Student added successfully"}
```

The client sends student information in the request body.

Example request:

```http
POST /admin/add_student
Content-Type: application/json
```

```json
{
    "admission_no": "ADM101",
    "name": "Rahul",
    "age": 20,
    "course": "Information Technology",
    "gender": "male",
    "phone": "9876543210",
    "cgpa": 8.5,
    "passing_year": 2027
}
```

FastAPI validates the request body using the `StudentBase` Pydantic schema before executing the route.

### PATCH — Update existing data

PATCH is used to partially update an existing resource.

Your application uses it to update student information:

```python
@app.patch("/admin/update_student/{admission_no}")
def update_student(
    admission_no: str,
    student: StudentPatch,
    db: Session = Depends(get_db)
):
    existing_student = db.query(models.Student).filter(
        models.Student.admission_no == admission_no
    ).first()

    if not existing_student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    update_data = student.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(existing_student, key, value)

    db.commit()

    return {"message": "Student updated successfully"}
```

The admission number in the URL identifies the student to update.

The request body contains only the fields that need to change.

For example:

```http
PATCH /admin/update_student/ADM101
Content-Type: application/json
```

```json
{
    "cgpa": 9.1
}
```

The `exclude_unset=True` argument ensures that only fields explicitly supplied by the client are included in the update dictionary.

Note: Your `StudentPatch` schema should exclude `admission_no` if the admission number is not intended to be editable.

### DELETE — Remove data

DELETE requests are used to remove an existing resource.

Your application uses:

```python
@app.delete("/admin/delete_student/{admission_no}")
def delete_student(
    admission_no: str,
    db: Session = Depends(get_db)
):
    student = db.query(models.Student).filter(
        models.Student.admission_no == admission_no
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db.delete(student)
    db.commit()

    return {"message": "Student deleted successfully"}
```

Example request:

```http
DELETE /admin/delete_student/ADM101
```

The route finds the student, deletes the database object, and commits the transaction.

## 3. Path parameters

Path parameters are values embedded directly in a URL.

For example:

```python
@app.get("/profile/{admission_no}")
def get_profile(admission_no: str):
    return {"admission_no": admission_no}
```

Here, `{admission_no}` is a path parameter.

If the client requests:

```http
GET /profile/ADM101
```

FastAPI extracts `ADM101` from the URL and passes it to the function.

Path parameters are useful when a request targets a specific resource.

Your project uses them to identify students by admission number.

## 4. Query parameters

Query parameters are values passed after `?` in a URL.

Example:

```http
GET /students?course=IT&year=2027
```

A FastAPI route can access them using function parameters:

```python
@app.get("/students")
def get_students(course: str, year: int):
    return {
        "course": course,
        "year": year
    }
```

FastAPI automatically extracts and validates these values.

Query parameters are commonly used for:

- Searching
- Filtering
- Sorting
- Pagination

Your current project uses admission numbers in the URL path for student searches.

## 5. Request body

A request body contains data sent by the client to the server.

For example, when adding a student, the frontend sends a JSON object containing student details.

FastAPI can receive and validate this data through a Pydantic model.

```python
@app.post("/admin/add_student")
def add_student(student: StudentBase):
    return student
```

Here, `StudentBase` defines the expected structure of the request body.

If the client sends invalid data, FastAPI returns a validation error instead of executing the route normally.

For example, if `age` must be an integer but the client sends an invalid value, validation will fail.

## 6. Response types

A route can return different kinds of responses depending on the application's requirements.

### JSON response

```python
@app.get("/api/message")
def message():
    return {"message": "Hello from FastAPI"}
```

FastAPI converts Python dictionaries and other supported values into JSON responses.

### HTML response

Your project uses Jinja2 templates to render HTML pages.

```python
return templates.TemplateResponse(
    "admin.html",
    {
        "request": request,
        "total_students": total_students,
        "student": None
    }
)
```

Instead of returning JSON, this route renders an HTML template and sends the resulting page to the browser.

This is useful for server-side rendered applications.

## 7. HTTP status codes

Status codes communicate the result of an HTTP request.

Some important status codes used in backend development:

| Status code | Meaning |
|---|---|
| 200 OK | Request completed successfully |
| 201 Created | Resource created successfully |
| 204 No Content | Request succeeded without a response body |
| 400 Bad Request | Request is invalid |
| 401 Unauthorized | Authentication is required or invalid |
| 403 Forbidden | Client is not permitted to perform the operation |
| 404 Not Found | Requested resource does not exist |
| 409 Conflict | Request conflicts with existing data |
| 422 Unprocessable Content | Request data failed validation |
| 500 Internal Server Error | Unexpected server-side error |

FastAPI provides `HTTPException` to return HTTP errors.

Example:

```python
from fastapi import HTTPException

if not student:
    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )
```

The request stops executing and FastAPI sends an appropriate error response.

You can also explicitly set the success status code:

```python
@app.post("/students", status_code=201)
def create_student():
    return {"message": "Student created"}
```

## 8. How frontend and backend communicate

Your application uses HTML, CSS, and JavaScript on the frontend and FastAPI on the backend.

For example, when an administrator adds a student:

1. The administrator fills out the student form.
2. JavaScript collects the entered values.
3. JavaScript sends a POST request to `/admin/add_student`.
4. FastAPI receives the request.
5. Pydantic validates the submitted data.
6. The route receives a database session through dependency injection.
7. SQLAlchemy performs the database operations.
8. PostgreSQL stores the new student.
9. FastAPI sends a response to the frontend.
10. JavaScript processes the response and updates the interface.

This is the basic request-response lifecycle of a web application.

## 9. Routes implemented in this project

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/admin` | Display the admin dashboard |
| GET | `/profile/{admission_no}` | Display a student's profile |
| POST | `/admin/add_student` | Add a student |
| GET | `/admin/search_student/{admission_no}` | Search for a student |
| DELETE | `/admin/delete_student/{admission_no}` | Delete a student |
| GET | `/admin/edit_student/` | Display the student editing page |
| PATCH | `/admin/update_student/{admission_no}` | Update student details |

## 10. Key takeaways

- Routes connect HTTP requests to Python functions.
- HTTP methods describe the operation being requested.
- Path parameters identify specific resources.
- Query parameters are useful for filtering and searching.
- Request bodies carry data from the client to the server.
- Pydantic validates request data.
- HTTP status codes communicate the result of a request.
- FastAPI supports both JSON APIs and HTML responses.

## Further reading

- [FastAPI — First Steps](https://fastapi.tiangolo.com/tutorial/first-steps/)
- [FastAPI — Path Parameters](https://fastapi.tiangolo.com/tutorial/path-params/)
- [FastAPI — Query Parameters](https://fastapi.tiangolo.com/tutorial/query-params/)
- [FastAPI — Request Body](https://fastapi.tiangolo.com/tutorial/body/)
- [MDN — HTTP Request Methods](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Methods)
- [MDN — HTTP Response Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status)