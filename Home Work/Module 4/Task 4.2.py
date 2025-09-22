# Пользователь вводит с клавиатуры два числа (начало и конец
# диапазона). Требуется проанализировать все числа в этом
# диапазоне. Нужно вывести на экран (по выбору пользователя):
# 1.Все числа диапазона;
# 2.Все числа диапазона в убывающем порядке;
# 3.Все числа, кратные 7;
# 4.Количество чисел, кратных 5

first_number = int(input('Введите начало диапазона: '))
second_number = int(input('Введите конец диапазона: '))

start = min(first_number, second_number)
end = max(first_number, second_number)

count = 0
print('Нажмите на нужное число: ')
what_u_want = input('1 - все числа диапазона/2 - Все числа диапазона в убывающем порядке / 3- Все числа, кратные 7 '
                    '/4 - Количество чисел, кратных 5: ')
if what_u_want == '1':
    for num in range(start, end + 1):
        print(num, end='\t')
elif what_u_want == '2':
    for num in range(end, start, -1):
        print(num, end='\t')
elif what_u_want == '3':
    for num in range(start, end + 1):
        if num % 7 == 0:
            print(num, end='\t')
elif what_u_want == '4':
    for num in range(start, end + 1):
        if num % 5 == 0:
            count += 1

    print(f'Количество чисел в диапазоне [{start};{end}], кратных 5: {count}')
else:
    print('Выберите правильный вариант:(1-4)')
