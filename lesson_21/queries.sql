-- Students enrolled in course 1 (Python).
SELECT s.id, s.name, s.email
FROM students s
JOIN enrollments e ON e.student_id = s.id
WHERE e.course_id = 1
ORDER BY s.id;

-- Courses attended by student 1.
SELECT c.id, c.name
FROM courses c
JOIN enrollments e ON e.course_id = c.id
WHERE e.student_id = 1
ORDER BY c.id;