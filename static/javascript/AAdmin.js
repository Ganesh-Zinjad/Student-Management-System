// ==========================================
// ADD STUDENT
// ==========================================

const form = document.getElementById("add_student");

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const formData = new FormData(form);
  const studentData = Object.fromEntries(formData.entries());

  // Convert number fields from strings to numbers
  studentData.age = Number(studentData.age);
  studentData.cgpa = Number(studentData.cgpa);
  studentData.passing_year = Number(studentData.passing_year);

  console.log("Sending:", studentData);

  try {
    const response = await fetch("/admin/add_student", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(studentData),
    });

    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.detail || "Failed to add student.");
    }

    alert(result.message || "Student added successfully!");

    form.reset();

    // reset total student value
    const totalStudents = document.getElementById("totalStudents");

    totalStudents.textContent = Number(totalStudents.textContent) - 1;
  } catch (error) {
    console.error("Error adding student:", error);
    alert(error.message);
  }
});

// ==========================================
// SEARCH STUDENT
// ==========================================

const searchForm = document.getElementById("searchForm");

searchForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const admission_no = document.getElementById("search").value.trim();

  if (!admission_no) {
    alert("Please enter an admission number.");
    return;
  }

  try {
    const response = await fetch(
      `/admin/search_student/${encodeURIComponent(admission_no)}`,
    );

    const data = await response.json();

    localStorage.setItem('student', data);
    localStorage.setItem("student", JSON.stringify(data));

    if (!response.ok) {
      throw new Error(data.detail || "Student not found.");
    }else{
      localStorage.setItem('student', data);
      localStorage.setItem("student", JSON.stringify(data));
    }
    // console.log(data)

    // Display student details
    document.getElementById("studentAdmission").textContent = data.admission_no;
    document.getElementById("studentName").textContent = data.name;
    document.getElementById("studentAge").textContent = data.age;
    document.getElementById("studentCourse").textContent = data.course;
    document.getElementById("studentGender").textContent = data.gender;
    document.getElementById("studentPhone").textContent = data.phone_no;
    document.getElementById("studentCGPA").textContent = data.cgpa;
    document.getElementById("studentPassingYear").textContent =
      data.passing_year;

    // Store admission number for edit/delete operations
    document.getElementById("editStudentBtn").dataset.admission =
      data.admission_no;
  } catch (error) {
    console.error("Search error:", error);
    alert(error.message);

    // Clear previous search result
    clearStudentDetails();
  }
});

// ==========================================
// DELETE STUDENT
// ==========================================

const del = document.getElementById("del_btn");

del.addEventListener("click", async (event) => {
  event.preventDefault();

  // Get admission number of searched student
  const admission_no =
    document.getElementById("editStudentBtn").dataset.admission;

  if (!admission_no) {
    alert("Please search for a student first.");
    return;
  }

  // Confirmation before deletion
  const confirmed = confirm("Are you sure you want to delete this student?");

  if (!confirmed) {
    return;
  }

  try {
    const response = await fetch(
      `/admin/delete_student/${encodeURIComponent(admission_no)}`,
      {
        method: "DELETE",
      },
    );

    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.detail || "Failed to delete student.");
    }

    alert(result.message || "Student deleted successfully!");

    // Clear student details
    clearStudentDetails();

    // Clear stored admission number
    document.getElementById("editStudentBtn").dataset.admission = "";

    // Clear search input
    document.getElementById("search").value = "";

    // reset total student value
    const totalStudents = document.getElementById("totalStudents");

    totalStudents.textContent = Number(totalStudents.textContent) - 1;
  } catch (error) {
    console.error("Delete error:", error);
    alert(error.message);
  }
});

// ==========================================
// CLEAR STUDENT DETAILS
// ==========================================

function clearStudentDetails() {
  document.querySelectorAll(".student-details strong").forEach((element) => {
    element.textContent = "---";
  });

  document.getElementById("editStudentBtn").dataset.admission = "";
}


//Edit button

const edit_button = document.getElementById("editStudentBtn");

edit_button.addEventListener("click", function(event) {

    const admission_no = document.getElementById("search").value.trim();

    if (!admission_no) {
        alert("Please enter admission number");
        return;
    }

    window.location.href = `/admin/edit_student/`;

    const student = JSON.parse(localStorage.getItem("student"));

    document.getElementsByName("admission_no").value=student.admission_no
    document.getElementsByName("name").value=student.name
    document.getElementsByName("age").value=student.age
    document.getElementsByName("course").value=student.course
    document.getElementsByName("phone_number").value=student.phone_no
    document.getElementsByName("average_cgpa").value=student.cgpa
    document.getElementsByName("passing_year").value=student.passing_year
    
});
