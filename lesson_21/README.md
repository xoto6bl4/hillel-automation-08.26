# Управління студентами (SQLite)

Потрібен тільки Python 3: SQLite уже входить до стандартної бібліотеки.
Основний файл завдання — `homework_21.py`. З папки `lesson_21` запустіть:

1. `python homework_21.py init` — створить `students.db`, п'ять курсів,
   20 студентів і випадкові реєстрації (по 2–3 курси кожному студенту).
2. `python homework_21.py add "Olena Koval" olena@example.com 1` — додасть
   студентку на курс 1. Команда поверне її ID.
3. `python homework_21.py students 1` — студенти курсу 1.
4. `python homework_21.py courses 21` — курси студентки з ID 21 (якщо це
   перший доданий студент; інакше використайте ID з кроку 2).
5. `python homework_21.py enroll 21 2` — додасть її на другий курс.
6. `python homework_21.py update-student 21 "Olena K." olena.k@example.com`
   або `python homework_21.py update-course 2 "SQL Basics"` — оновлення.
7. `python homework_21.py delete-student 21` — видалить студентку та її
   реєстрації на курси.

У DBeaver виберіть **New Database Connection → SQLite** і вкажіть файл
`lesson_21/students.db` (він з'являється після `init`). Якщо програма
запропонує завантажити драйвер SQLite, погодьтеся. У списку таблиць будуть
`students`, `courses`, `enrollments`; `queries.sql` містить два приклади
запитів для SQL Editor. Після команд Python оновіть таблицю в DBeaver.

Для перевірки коду: `python -B -m unittest -v test_homework_21`.
Файл бази не додається до Git: `init` створює його на вашому комп'ютері.