# Написать программу, которая по выбору пользователя возводит
# введенное им число в степень от нулевой до седьмой
# включительно
# 1. Введем число, тип float так как можно ввести любое
num = float(input('Введите число '))
# 2. Введем в степень, тип данных int так как строго от 0-7
degree = int(input('Введите степень - 0, 1, 2, 3, 4, 5, 6, 7: '))
# 3. Вывод результата
if degree == 0:
    finish = num / num
    print(f'Число {num} в 0 степени = {finish}')
elif degree == 1:
    finish = num
    print(f'Число {num} в 1 степени = {finish}')
elif degree == 2:
    finish = num * num
    print(f'Число {num} во 2 степени = {finish}')
elif degree == 3:
    finish = num * num * num
    print(f'Число {num} в 3 степени = {finish}')
elif degree == 4:
    finish = num * num * num * num
    print(f'Число {num} в 4 степени = {finish}')
elif degree == 5:
    finish = num * num * num * num * num
    print(f'Число {num} в 5 степени = {finish}')
elif degree == 6:
    finish = num * num * num * num * num * num
    print(f'Число {num} в 6 степени = {finish}')
elif degree == 7:
    finish = num * num * num * num * num * num * num
    print(f'Число {num} в 7 степени = {finish}')
else:
    print('Введите нужную степень')
