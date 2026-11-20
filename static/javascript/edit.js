const student = JSON.parse(localStorage.getItem("student"));
const form = document.querySelector("form");

// Populate form with existing student details
if (student) {
  for (const [key, value] of Object.entries(student)) {
    const input = document.getElementsByName(key)[0];

    if (input) {
      input.value = value;
    }
  }
}

document.getElementsByName("phone_no")[0].value = student.phone_no;
document.getElementsByName("cgpa")[0].value = student.cgpa;
document.getElementsByName("gender")[0].value = student;

const admission_no=document.getElementsByName("admission_no")[0].value;

form.addEventListener("submit", async (event) => {
  event.preventDefault();

//   const form = document.getElementById("update_student");

  const formData = new FormData(form);
  const studentData = Object.fromEntries(formData.entries());
    
  console.log(studentData)

  try{
    const response = await fetch(`/admin/update_student/${encodeURIComponent(admission_no)}`, {
      method: "PATCH",
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
  } catch(error) {
        alert(error.message);
  }

});


