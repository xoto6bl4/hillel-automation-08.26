"""
Завдання 1:
Візміть два файли з теки ideas_for_test/work_with_csv порівняйте на наявність дублікатів
і приберіть їх. Результат запишіть у файл result_kamalov.csv
"""
import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_A = os.path.join(BASE_DIR, "random.csv")
FILE_B = os.path.join(BASE_DIR, "random-michaels.csv")
RESULT_FILE = os.path.join(BASE_DIR, "result_kamalov.csv")

with open(FILE_A, "r", encoding="utf-8", newline="") as f:
    rows_a = list(csv.reader(f))

with open(FILE_B, "r", encoding="utf-8", newline="") as f:
    rows_b = list(csv.reader(f))

header = rows_a[0]
num_fields = len(header)
all_rows = rows_a[1:] + rows_b[1:]

unique_rows = []
seen = set()
for row in all_rows:
    row = row[:num_fields]
    normalized = tuple(value.strip() for value in row)
    if normalized not in seen:
        seen.add(normalized)
        unique_rows.append(row)

with open(RESULT_FILE, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(unique_rows)

print(f"Рядків всього: {len(all_rows)}")
print(f"Унікальних рядків: {len(unique_rows)}")
print(f"Прибрано дублікатів: {len(all_rows) - len(unique_rows)}")
