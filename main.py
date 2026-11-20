
from schema import StudentPatch
from schema import StudentBase
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import schema
import models
from database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

app = FastAPI()

# HTML templates location
templates = Jinja2Templates(directory="templates")

# Serve CSS, JavaScript files
app.mount("/static", StaticFiles(directory="static"), name="static")


#get /profile/admission_no
@app.get("/profile/{admission_no}", response_class=HTMLResponse)

def get_profile(request: Request, admission_no: str, db = Depends(get_db)):

    student = db.query(models.Student).filter(
        models.Student.admission_no == admission_no
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return templates.TemplateResponse(
        request=request,
        name="profile.html",
        context={
            "student": student
        }
    )


@app.delete("/admin/delete_student/{admission_no}")
def delete_student( admission_no: str, db: Session = Depends(get_db)):
    # Find the student
    student = db.query(models.Student).filter(
        models.Student.admission_no == admission_no
    ).first()

    # Check whether student exists
    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # Delete the student
    db.delete(student)

    # Commit    changes to database
    db.commit()

    return {"message": "Student deleted successfully"}



@app.get("/admin/search_student/{admission_no}")
def edit_student(request: Request, admission_no : str, db=Depends(get_db)):
    student = db.query(models.Student).filter(
        models.Student.admission_no == admission_no
    ).first()

    return student

@app.get("/admin", response_class=HTMLResponse)
def admin(request: Request, db = Depends(get_db)):

    total_students = db.query(models.Student).count()

    return templates.TemplateResponse(
        request=request,
        name="admin.html",
        context={
            "total_students":total_students,
            "student":None
        }
    )



@app.post("/admin/add_student")
def admin_add_student(
    student: StudentBase,
    db: Session = Depends(get_db)
):

    try:
        # Create SQLAlchemy model instance
        new_student = models.Student(
            admission_no=student.admission_no,
            name=student.name,
            age=student.age,
            course=student.course,
            gender=student.gender,
            phone_no=student.phone_no,
            cgpa=student.cgpa,
            passing_year=student.passing_year
        )

        # Add object to database session
        db.add(new_student)

        # Commit transaction
        db.commit()

        # Retrieve database-generated values
        db.refresh(new_student)

        return {
            "message": "Student added successfully",
            "student_id": new_student.id,
            "admission_no": new_student.admission_no
        }

    except IntegrityError as e:
        db.rollback()

        print("Database integrity error:", e)

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Admission number already exists"
        )

    except Exception as e:
        db.rollback()

        print("Unexpected error:", repr(e))

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while adding the student"
        )


@app.get("/admin/edit_student/", response_class=HTMLResponse)

def get_profile(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="edit_student.html",
    )


# update_student

@app.patch("/admin/update_student/{admission_no}")
def update_student(admission_no: str, student: StudentPatch, db: Session = Depends(get_db)):
    existing_student = db.query(models.Student).filter(
        models.Student.admission_no == admission_no
    ).first()

    if not existing_student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    update_data = student.model_dump(exclude_unset=True)

    # Admission number is the primary identifier, not an editable field
    # update_data.pop("admission_no", None)

    for key, value in update_data.items():
        setattr(existing_student, key, value)

    db.commit()

    return {
        "success": True,
        "message": "Student updated successfully"
    }