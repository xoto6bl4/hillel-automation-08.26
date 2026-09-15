# task 1
""" Задача - надрукувати табличку множення на задане число, але
лише до максимального значення для добутку - 25.
Код майже готовий, треба знайти помилки та випраавити\доповнити.
"""
def multiplication_table(number):
    # Initialize the appropriate variable
    multiplier = 1

    # Complete the while loop condition.
    while True:
        result = number * multiplier
        # десь тут помила, а може не одна
        if  result > 25:
            # Enter the action to take if the result is greater than 25
            break

        print(str(number) + "x" + str(multiplier) + "=" + str(result))

        # Increment the appropriate variable
        multiplier += 1

multiplication_table(3)
# Should print:
# 3x1=3
# 3x2=6
# 3x3=9
# 3x4=12
# 3x5=15


# task 2
"""  Написати функцію, яка обчислює суму двох чисел.
"""
def sum_of_digits(number1, number2):
    return number1 + number2

result = sum_of_digits(55, 16)
print(result)


# task 3
"""  Написати функцію, яка розрахує середнє арифметичне списку чисел.
"""
def average_number(numbers):
    return sum(numbers) / len(numbers)

print(average_number([55, 16]))

# task 4
"""  Написати функцію, яка приймає рядок та повертає його у зворотному порядку.
"""
def str_inside_out(text):
    return text[::-1]
print(str_inside_out("Fuck_McLaren"))

# task 5
"""  Написати функцію, яка приймає список слів та повертає найдовше слово у списку.
"""
def longest_word(text):
    return max(text, key=len)

print(longest_word(["Harry", "Potter", "Halfblood", "Prince", "Dobbi"]))
# task 6
"""  Написати функцію, яка приймає два рядки та повертає індекс першого входження другого рядка
у перший рядок, якщо другий рядок є підрядком першого рядка, та -1, якщо другий рядок
не є підрядком першого рядка."""
def find_substring(str1, str2):

    return str1.find(str2)

str1 = "Hello, world!"
str2 = "world"
print(find_substring(str1, str2)) # поверне 7

str1 = "The quick brown fox jumps over the lazy dog"
str2 = "cat"
print(find_substring(str1, str2)) # поверне -1

# task 7-
"""Порахувати кількість унікальних символів в строці.
Якщо їх більше 10 - вивести в консоль True, інакше - False.
Строку отримати за допомогою функції input()"""
def count_unique(text):
    return len(set(text))

def is_more_than_10(text):
    if count_unique(text) > 10:
        return True
    else:
        return False


symbol = input("Напишіть щось, будь ласка\n")
print(is_more_than_10(symbol))

# task 9
""""Є list з даними lst1 = ['1', '2', 3, True, 'False', 5, '6', 7, 8, 'Python', 9, 0, 'Lorem Ipsum'].
Напишіть код, який свормує новий list (наприклад lst2), який містить лише змінні типу стрінг, які присутні в lst1.
Данні в лісті можуть бути будь якими"""
def only_strings(lst):
    return [i for i in lst if type(i) == str]
print(only_strings([1, "a", 2, "b"]))
# task 10
"""
Площа Чорного моря становить 436 402 км2, а площа Азовського
моря становить 37 800 км2. Яку площу займають Чорне та Азов-
ське моря разом?
"""
def total_area(sea1, sea2):
    return sea1 + sea2

print(total_area(436402, 37800), "км²")

"""  Оберіть будь-які 4 таски з попередніх домашніх робіт та
перетворіть їх у 4 функції, що отримують значення та повертають результат.
Обоязково документуйте функції та дайте зрозумілі імена змінним.
"""