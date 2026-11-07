"""Tests for the student and course database."""

import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

from homework_21 import (
    add_student, courses_for_student, delete_student, enroll_student,
    initialize_database, students_on_course, update_course, update_student,
)


class StudentDatabaseTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.db_path = Path(self.folder.name) / "students.db"
        initialize_database(self.db_path)

    def test_seed_and_relationships(self):
        with closing(sqlite3.connect(self.db_path)) as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM students").fetchone()[0], 20)
            self.assertEqual(db.execute("SELECT COUNT(*) FROM courses").fetchone()[0], 5)
            counts = db.execute("""
                SELECT COUNT(*) FROM enrollments GROUP BY student_id ORDER BY student_id
            """).fetchall()
            self.assertEqual(len(counts), 20)
            self.assertTrue(all(2 <= count[0] <= 3 for count in counts))
            self.assertEqual(db.execute("PRAGMA foreign_key_check").fetchall(), [])
            first_course = db.execute("SELECT course_id FROM enrollments WHERE student_id = 1 LIMIT 1").fetchone()[0]
        self.assertIn(1, [s["id"] for s in students_on_course(first_course, self.db_path)])
        self.assertIn(first_course, [c["id"] for c in courses_for_student(1, self.db_path)])
        initialize_database(self.db_path)
        with closing(sqlite3.connect(self.db_path)) as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM students").fetchone()[0], 20)

    def test_add_enroll_update_and_delete(self):
        student_id = add_student("Oksana", "oksana@example.com", 1, self.db_path)
        self.assertIn(student_id, [s["id"] for s in students_on_course(1, self.db_path)])
        enroll_student(student_id, 2, self.db_path)
        self.assertEqual([c["id"] for c in courses_for_student(student_id, self.db_path)], [1, 2])
        self.assertTrue(update_student(student_id, "Oksana K.", "oksana.k@example.com", self.db_path))
        self.assertEqual(students_on_course(1, self.db_path)[-1]["name"], "Oksana K.")
        self.assertTrue(update_course(2, "Advanced SQL", self.db_path))
        self.assertEqual(courses_for_student(student_id, self.db_path)[1]["name"], "Advanced SQL")
        self.assertTrue(delete_student(student_id, self.db_path))
        self.assertEqual(courses_for_student(student_id, self.db_path), [])
        with closing(sqlite3.connect(self.db_path)) as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM enrollments WHERE student_id = ?", (student_id,)).fetchone()[0], 0)

    def test_invalid_course_rolls_back_new_student(self):
        with self.assertRaises(sqlite3.IntegrityError):
            add_student("Nobody", "nobody@example.com", 999, self.db_path)
        with closing(sqlite3.connect(self.db_path)) as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM students").fetchone()[0], 20)
        with self.assertRaises(sqlite3.IntegrityError):
            enroll_student(1, 999, self.db_path)


if __name__ == "__main__":
    unittest.main()