# Показать на экран все простые числа в диапазоне, указанном
# пользователем. Число называется простым, если оно делится без
# остатка только на себя и на единицу. Например, три — это простое
# число, а четыре нет.
# 1. Введем диапазон чисел:
first_number = int(input('Введите начало диапазона: '))
second_number = int(input('Введите конец диапазона: '))

start = min(first_number, second_number)
end = max(first_number, second_number)

print(f"Простые числа от {start} до {end}:")
for num in range(start, end + 1):
    if num < 2:
        continue
    count = 0
    for j in range(1, num + 1):
        if num % j == 0:
            count += 1
    if count == 2:  # Простое число имеет ровно 2 делителя
        print(num, end=" ")





