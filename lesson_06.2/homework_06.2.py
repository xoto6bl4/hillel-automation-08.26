# Напишіть цикл, який буде вимагати від користувача ввести слово, в якому є літера "h" (враховуються як великі так і маленькі).
# Цикл не повинен завершитися, якщо користувач ввів слово без букви "h".

while True:
    Carlos_Sainz = input("Enter word with letter H or h\n")

    if "H" in Carlos_Sainz or "h" in Carlos_Sainz:
        print("Good boy")
        break