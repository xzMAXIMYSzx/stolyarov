# 1. Введите число, тип int так как работа с целыми числами
a = int(input('Введите число: '))
# 2. Проверка на кратность:
if a % 7 == 0:
    print(f'{a} - Number is multiple 7')
else:
    print(f'{a} - Number is not multiple 7')
