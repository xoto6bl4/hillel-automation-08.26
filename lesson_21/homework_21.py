"""Student and course management with a local SQLite database."""

import argparse
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from random import Random


DB_PATH = Path(__file__).with_name("students.db")
COURSES = ("Python", "SQL", "Testing", "Git", "Web Development")


@contextmanager
def open_database(db_path=DB_PATH):
    db = sqlite3.connect(db_path)
    try:
        db.execute("PRAGMA foreign_keys = ON")
        db.row_factory = sqlite3.Row
        with db:
            yield db
    finally:
        db.close()


def initialize_database(db_path=DB_PATH):
    """Create the tables and seed 20 students on the first run."""
    with open_database(db_path) as db:
        db.executescript("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            );
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE
            );
            CREATE TABLE IF NOT EXISTS enrollments (
                student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
                course_id INTEGER NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
                PRIMARY KEY (student_id, course_id)
            );
        """)
        if db.execute("SELECT COUNT(*) FROM students").fetchone()[0]:
            return

        db.executemany("INSERT OR IGNORE INTO courses (name) VALUES (?)",
                       [(name,) for name in COURSES])
        db.executemany("INSERT INTO students (name, email) VALUES (?, ?)",
                       [(f"Student {n:02d}", f"student{n:02d}@example.com")
                        for n in range(1, 21)])
        student_ids = [row[0] for row in db.execute("SELECT id FROM students ORDER BY id")]
        course_ids = [row[0] for row in db.execute("SELECT id FROM courses ORDER BY id")]
        rng = Random(21)
        enrollments = [
            (student_id, course_id)
            for student_id in student_ids
            for course_id in rng.sample(course_ids, rng.randint(2, 3))
        ]
        db.executemany("INSERT INTO enrollments (student_id, course_id) VALUES (?, ?)",
                       enrollments)


def add_student(name, email, course_id, db_path=DB_PATH):
    """Add a student and enroll them in one course in the same transaction."""
    with open_database(db_path) as db:
        student_id = db.execute(
            "INSERT INTO students (name, email) VALUES (?, ?)", (name, email)
        ).lastrowid
        db.execute("INSERT INTO enrollments (student_id, course_id) VALUES (?, ?)",
                   (student_id, course_id))
        return student_id


def enroll_student(student_id, course_id, db_path=DB_PATH):
    with open_database(db_path) as db:
        db.execute("INSERT INTO enrollments (student_id, course_id) VALUES (?, ?)",
                   (student_id, course_id))


def students_on_course(course_id, db_path=DB_PATH):
    with open_database(db_path) as db:
        rows = db.execute("""
            SELECT s.id, s.name, s.email
            FROM students s
            JOIN enrollments e ON e.student_id = s.id
            WHERE e.course_id = ?
            ORDER BY s.id
        """, (course_id,)).fetchall()
        return [dict(row) for row in rows]


def courses_for_student(student_id, db_path=DB_PATH):
    with open_database(db_path) as db:
        rows = db.execute("""
            SELECT c.id, c.name
            FROM courses c
            JOIN enrollments e ON e.course_id = c.id
            WHERE e.student_id = ?
            ORDER BY c.id
        """, (student_id,)).fetchall()
        return [dict(row) for row in rows]


def update_student(student_id, name, email, db_path=DB_PATH):
    with open_database(db_path) as db:
        result = db.execute("UPDATE students SET name = ?, email = ? WHERE id = ?",
                            (name, email, student_id))
        return result.rowcount == 1


def update_course(course_id, name, db_path=DB_PATH):
    with open_database(db_path) as db:
        result = db.execute("UPDATE courses SET name = ? WHERE id = ?", (name, course_id))
        return result.rowcount == 1


def delete_student(student_id, db_path=DB_PATH):
    with open_database(db_path) as db:
        result = db.execute("DELETE FROM students WHERE id = ?", (student_id,))
        return result.rowcount == 1


def main():
    parser = argparse.ArgumentParser(description="Manage students and courses")
    parser.add_argument("--db", type=Path, default=DB_PATH, help="SQLite database file")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("init", help="Create and seed the database")
    add = commands.add_parser("add", help="Add a student to a course")
    add.add_argument("name")
    add.add_argument("email")
    add.add_argument("course_id", type=int)
    enroll = commands.add_parser("enroll", help="Add an existing student to another course")
    enroll.add_argument("student_id", type=int)
    enroll.add_argument("course_id", type=int)
    students = commands.add_parser("students", help="List students on a course")
    students.add_argument("course_id", type=int)
    courses = commands.add_parser("courses", help="List a student's courses")
    courses.add_argument("student_id", type=int)
    update_s = commands.add_parser("update-student")
    update_s.add_argument("student_id", type=int)
    update_s.add_argument("name")
    update_s.add_argument("email")
    update_c = commands.add_parser("update-course")
    update_c.add_argument("course_id", type=int)
    update_c.add_argument("name")
    delete = commands.add_parser("delete-student")
    delete.add_argument("student_id", type=int)
    args = parser.parse_args()

    if args.command == "init":
        initialize_database(args.db)
        return f"Database ready: {args.db}"
    if args.command == "add":
        return f"Student added with ID {add_student(args.name, args.email, args.course_id, args.db)}"
    if args.command == "enroll":
        enroll_student(args.student_id, args.course_id, args.db)
        return "Enrollment added"
    if args.command == "students":
        rows = students_on_course(args.course_id, args.db)
        return "\n".join(f"{row['id']}: {row['name']} ({row['email']})" for row in rows) or "No students"
    if args.command == "courses":
        rows = courses_for_student(args.student_id, args.db)
        return "\n".join(f"{row['id']}: {row['name']}" for row in rows) or "No courses"
    if args.command == "update-student":
        return "Student updated" if update_student(args.student_id, args.name, args.email, args.db) else "Student not found"
    if args.command == "update-course":
        return "Course updated" if update_course(args.course_id, args.name, args.db) else "Course not found"
    return "Student deleted" if delete_student(args.student_id, args.db) else "Student not found"


if __name__ == "__main__":
    print(main())