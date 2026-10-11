#1
def calculate_total_area(black_sea, azov_sea):
    return black_sea + azov_sea

#2
def check_symbols(symbol):
    symbols = len(set(symbol))
    return symbols > 10

#3
def has_h_letter(word):
    return "H" in word or "h" in word

#4
def sum_even_numbers(lst):
    lst2 = []

    for i in lst:
        if i % 2 == 0:
            lst2.append(i)

    return sum(lst2)

#5
def str_inside_out(text):
    return text[::-1]