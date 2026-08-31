alice_in_wonderland = ('"Would you tell me, please, which way I ought to go from here?" ' 
                       '"That depends a good deal on where you want to get to," said the Cat. '
                       '"I don\'t much care where ——" said Alice."'
                       '"Then it doesn\'t matter which way you go," said the Cat. '
                       '"—— so long as I get somewhere," Alice added as an explanation. '
                       '"Oh, you\'re sure to do that," said the Cat, "if you only walk long enough."')
print(alice_in_wonderland)
print(alice_in_wonderland.count("'"))
# task 01 == Розділіть змінну alice_in_wonderland так, щоб вона займала декілька фізичних лінії
# task 02 == Знайдіть та відобразіть всі символи одинарної лапки (') у тексті
# task 03 == Виведіть змінну alice_in_wonderland на друк


"""
    # Задачі 04 -10:
    # Переведіть задачі з книги "Математика, 5 клас"
    # на мову пітон і виведіть відповідь, так, щоб було
    # зрозуміло дитині, що навчається в п'ятому класі
"""

# task 04
"""
Площа Чорного моря становить 436 402 км2, а площа Азовського
моря становить 37 800 км2. Яку площу займають Чорне та Азов-
ське моря разом?
"""
black_sea = 436402
azov_sea = 37800
total = black_sea + azov_sea
print(total, "км²")

# task 05
"""
Мережа супермаркетів має 3 склади, де всього розміщено
375 291 товар. На першому та другому складах перебуває
250 449 товарів. На другому та третьому – 222 950 товарів.
Знайдіть кількість товарів, що розміщені на кожному складі.
"""
total = 375291
storage_1_and_2 = 250449
storage_2_and_3 = 222950
storage_1 = total - storage_2_and_3
storage_3 = total - storage_1_and_2
storage_2 = total - storage_1 - storage_3
print(storage_1, storage_2, storage_3)

# task 06
"""
Михайло разом з батьками вирішили купити комп’ютер, ско-
риставшись послугою «Оплата частинами». Відомо, що сплачу-
вати необхідно буде півтора року по 1179 грн/місяць. Обчисліть
вартість комп’ютера.
"""
per_month = 1179
term = 18
total = per_month * term
print(total)

# task 07
"""
Знайди остачу від діленя чисел:
a) 8019 : 8     d) 7248 : 6
b) 9907 : 9     e) 7128 : 5
c) 2789 : 5     f) 19224 : 9
"""
num_1 = 8019 % 8
num_2 = 9907 % 9
num_3 = 2789 % 5
num_4 = 7248 % 6
num_5 = 7128 % 5
num_6 = 19224 % 9
print(num_1, num_2, num_3, num_4, num_5, num_6)

# task 08
"""
Іринка, готуючись до свого дня народження, склала список того,
що їй потрібно замовити. Обчисліть, скільки грошей знадобиться
для даного її замовлення.
Назва товару    Кількість   Ціна
Піца велика     4           274 грн
Піца середня    2           218 грн
Сік             4           35 грн
Торт            1           350 грн
Вода            3           21 грн
"""
big_pizza = 274 * 4
mid_pizza = 218 * 2
juice = 35 * 4
cake = 350
water = 21 * 3
total = big_pizza + mid_pizza + juice + cake + water
print(total)

# task 09
"""
Ігор займається фотографією. Він вирішив зібрати всі свої 232
фотографії та вклеїти в альбом. На одній сторінці може бути
розміщено щонайбільше 8 фото. Скільки сторінок знадобиться
Ігорю, щоб вклеїти всі фото?
"""
total = 232
one_page_max = 8
pages = total // one_page_max
print(pages)

# task 10
"""
Родина зібралася в автомобільну подорож із Харкова в Буда-
пешт. Відстань між цими містами становить 1600 км. Відомо,
що на кожні 100 км необхідно 9 літрів бензину. Місткість баку
становить 48 літрів.
1) Скільки літрів бензину знадобиться для такої подорожі?
2) Скільки щонайменше разів родині необхідно заїхати на зап-
равку під час цієї подорожі, кожного разу заправляючи пов-
ний бак?
"""
distance = 1600
tank = 48
expenses_per_100km = 9
expenses = distance / 100 * expenses_per_100km
stops = expenses / tank -1
print(expenses)
print(stops)