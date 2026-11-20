
"""
Pydantic schemas for request validation and response serialization.
"""

from pydantic.networks import EmailStr
from typing import Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)


# --------------------------------------------------
# GET /profile/admission_no
# post /admin/add/student
# PUT /admin/students/{admission_no}
# Request Schema
# --------------------------------------------------

class StudentBase(BaseModel):
    model_config = ConfigDict(
        extra="forbid",              # Reject unexpected input fields
        str_strip_whitespace=True,   # Remove leading/trailing whitespace
    )
    admission_no :str = Field(
        min_length=1,
        max_length=100,
    )

    name: str = Field(
        min_length=2,
        max_length=10,
    )

    age: int = Field(
        ge=5,
        le=100,
    )

    course: str = Field(
        min_length=2,
        max_length=100,
    )

    gender: Literal["male", "female", "other"]

    phone_no: str = Field(
        min_length=8,
        max_length=16,
        pattern=r"^\+?[1-9]\d{7,14}$",
    )

    cgpa: float = Field(
        ge=0,
        le=10,
    )

    passing_year: int = Field(
        ge=1900,
        le=2100,
    )



# --------------------------------------------------
# PATCH /admin/students/{admission_no}
# Request schema
# --------------------------------------------------

class StudentPatch(BaseModel):
    """
    Partial update: clients can send only the fields
    they want to modify.
    """

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    admission_no :str = Field(
        min_length=1,
        max_length=100,
    )

    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    age: int | None = Field(
        default=None,
        ge=5,
        le=100,
    )

    course: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    gender: Literal["Male", "Female", "Other"] | None = None

    phone_no: str | None = Field(
        default=None,
        min_length=8,
        max_length=16,
        pattern=r"^\+?[1-9]\d{7,14}$",
    )

    cgpa: float | None = Field(
        default=None,
        ge=0,
        le=10,
    )

    passing_year: int | None = Field(
        default=None,
        ge=1900,
        le=2100,
    )

    @model_validator(mode="after")
    def validate_non_empty(self):
        if not self.model_fields_set:
            raise ValueError("At least one field must be provided")

        return self


# --------------------------------------------------
# General operation response of apis
# --------------------------------------------------

class MessageResponse(BaseModel):
    success: bool
    message: str
