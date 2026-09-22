"""Створіть клас геометричної фігури "Ромб". Клас повинен мати наступні атрибути:

сторона_а (довжина сторони a).
кут_а (кут між сторонами a і b).
кут_б (суміжний з кутом кут_а).
Необхідно реалізувати наступні вимоги:

Значення сторони сторона_а повинно бути більше 0.
Кути кут_а та кут_б повинні задовольняти умову: кут_а + кут_б = 180
Протилежні кути ромба завжди рівні, тому при заданому значенні кут_а, значення кут_б обчислюється автоматично.
Для встановлення значень атрибутів використовуйте метод __setattr__. """

class Romb:
    def __init__(self, a_long, a_corner):
        self.a_long = a_long
        self.a_corner = a_corner

    def __setattr__(self, key, value):
       if key == "a_long":
           if value > 0:
               self.__dict__[key] = value
           else:
               print("a_long should be > 0")

       elif key == "a_corner":
            if 0 < value < 180:
               self.__dict__["a_corner"] = value
               self.__dict__["b_corner"] = 180 - value
            else:
               print("corner_a and corner_b from 0 to 180")

       elif key == "b_corner":
            if 0 < value < 180:
                self.__dict__["b_corner"] = value
            else:
                print("corner_b from 0 to 180")

       else:
               self.__dict__["b_corner"] = value

rmb = Romb(5, 60)
print(rmb.__dict__)