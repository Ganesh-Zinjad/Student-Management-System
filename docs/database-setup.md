# PostgreSQL Database Setup

This project uses PostgreSQL as its relational database and SQLAlchemy as its ORM.

The database and student table must be created before running the application.

## 1. Create the Database

Open pgAdmin and connect to your PostgreSQL server.

Right-click Databases → Create → Database.

Use the following database name:

`student_management`

Alternatively, execute:

```sql
CREATE DATABASE student_management;
```

## 2. Create the Student Table

Open the Query Tool for the `student_management` database and execute:

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

## 3. Verify the Table

Execute:

```sql
SELECT * FROM student;
```

You should see the student table with the columns defined above.

## 4. Configure Database Credentials

Create a `.env` file in the project root and configure your PostgreSQL credentials.

Refer to `.env.example` for the expected environment variables.

## 5. Database Connection

The application uses SQLAlchemy to connect to PostgreSQL.

The connection configuration is defined in `database.py`.

SQLAlchemy uses the Psycopg 3 driver to communicate with PostgreSQL.

**Note:** This project currently uses manual database creation through pgAdmin. Database migrations using Alembic are a possible future improvement.