"""Створіть клас "Студент" з атрибутами "ім'я", "прізвище", "вік" та "середній бал".
Створіть об'єкт цього класу, представляючи студента.'
Потім додайте метод до класу "Студент", який дозволяє змінювати середній бал студента.'
Виведіть інформацію про студента та змініть його середній бал."""

class Person:
    def __init__(self, first_name, last_name, age):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age

class Student(Person):
    def __init__(self, first_name, last_name, age, average_score):
        super().__init__(first_name, last_name, age)
        self.average_score = average_score

    def change_average_score(self, new_average_score):
        self.average_score = new_average_score

student = Student("Ronald", "Weasley", 16, 4.5)
print(f'Name: {student.first_name}\nLast name: {student.last_name}\nAge: {student.age}\nAvg.Score: {student.average_score}')

new_avg_score = float(input("Enter new average score: "))
student.change_average_score(new_avg_score)

print(f"New Avg. Score = {student.average_score}")