# Пользователь вводит с клавиатуры два числа (начало и конец
# диапазона). Требуется проанализировать все числа в этом
# диапазоне по следующему правилу: если число кратно 7, его надо
# выводить на экран.

first_number = int(input('Введите начало диапазона: '))
second_number = int(input('Введите конец диапазона: '))

start = min(first_number, second_number)
end = max(first_number, second_number)

for num in range(start, end + 1):
    if num % 7 == 0:
        print(f'число {num} кратно 7')

