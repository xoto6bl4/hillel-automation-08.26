# Порахувати кількість унікальних символів в строці.
# Якщо їх більше 10 - вивести в консоль True, інакше - False.
# Строку отримати за допомогою функції input()
symbol = input("Напишить щось, бум ласка: ")
symbols = len(set(symbol))
if symbols > 10:
  print(True)
else:
      print(False)