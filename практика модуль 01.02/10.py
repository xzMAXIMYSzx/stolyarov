# 1. Введите 3 числа. Тип данных float
a = float(input('Первое число = '))
b = float(input('Второе число = '))
c = float(input('Третье число = '))
# 2. Предположим, что a - самое большое число
max_number = a
# 3. Проверка
if b > a:
    max_number = b
if c > max_number:
    max_number = c
# 4. Вывод результата с самым большим числом
print(f'Наибольшее число: {max_number}')
