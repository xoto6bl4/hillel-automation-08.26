"""Завдання 1

Створіть клас Employee, який має атрибути name та salary.
Далі створіть два класи, Manager та Developer, які успадковуються від Employee.
Клас Manager повинен мати додатковий атрибут department,
а клас Developer - атрибут programming_language.

Тепер створіть клас TeamLead, який успадковується як від Manager, так і від Developer.
Цей клас представляє керівника з команди розробників.
Клас TeamLead повинен мати всі атрибути як Manager (ім'я, зарплата, відділ),
а також атрибут team_size, який вказує на кількість розробників у команді, якою керує керівник.

Напишіть тест, який перевіряє наявність атрибутів з Manager та Developer у класі TeamLead"""

class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary


class Developer(Employee):
    def __init__(self, programming_language, **kwargs):
        super().__init__(**kwargs)
        self.programming_language = programming_language


class Manager(Employee):
    def __init__(self, department, **kwargs):
        super().__init__(**kwargs)
        self.department = department


class TeamLead(Developer, Manager):
    def __init__(self, name, salary, programming_language, department, team_size):
        super(). __init__(
            name=name,
            salary=salary,
            programming_language=programming_language,
            department=department
        )
        self.team_size = team_size

team_lead = TeamLead("Antharas", 1488, "C#", "LowIQBoys", 322)

print(vars(team_lead))
if hasattr(team_lead, "department") and hasattr(team_lead, "programming_language"):
    print("U r Max Verstappen(ur test was successful)")
else:
    print("U r lence stroll(ur test failed)!")


"""Завдання 2

Створіть абстрактний клас "Фігура" з абстрактними методами для отримання площі та периметру.
Наслідуйте від нього декілька (> 2) інших фігур, та реалізуйте математично вірні для них методи для площі та периметру.
Властивості по типу “довжина сторони” й т.д. повинні бути приватними, та ініціалізуватись через конструктор.
Створіть Декілька різних об’єктів фігур, та у циклі порахуйте та виведіть в консоль площу та периметр кожної."""

from abc import ABC, abstractmethod
import math


class Figure(ABC):
    @abstractmethod
    def get_area(self):
        pass
    @abstractmethod
    def get_perimeter(self):
        pass


class Circle(Figure):
    def __init__(self, radius):
        self.__radius = radius

    def get_area(self):
        return math.pi * self.__radius**2

    def get_perimeter(self):
        return 2 * math.pi * self.__radius


class Rectangle(Figure):
    def __init__(self, width, height):
        self.__width = width
        self.__height = height

    def get_area(self):
        return self.__width * self.__height

    def get_perimeter(self):
        return 2 * (self.__width + self.__height)


class Triangle(Figure):
    def __init__(self, a, b, c):
        self.__a = a
        self.__b = b
        self.__c = c

    def get_perimeter(self):
        return self.__a + self.__b + self.__c

    def get_area(self):
        s = self.get_perimeter() / 2
        return math.sqrt(s * (s - self.__a) * (s - self.__b) * (s - self.__c))

figures = [
    Circle(5),
    Rectangle(4, 6),
    Triangle(3, 4, 5)
]

for figure in figures:
    print(f"Area: {figure.get_area():.2f}")
    print(f"Perimeter: {figure.get_perimeter():.2f}")
    print()