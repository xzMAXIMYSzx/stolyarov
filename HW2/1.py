# ever_number = 0
# odd_number = 0
#
# user_number = int(input('Введите число или 0 для остановки: '))
#
# while user_number != 0:
#     if user_number % 2 == 0:
#         ever_number += 1
#     else:
#         odd_number += 1
#         user_number = int(input('Введите число или 0 для остановки: '))
#
#         print('количество четных чисел', ever_number)
#         print('Количество не четных чисел', odd_number)

# while True:
#     user_choice = input('Введите 1 - продолжение, 0 - для отключения')
#     if user_choice == 0:
#
#         break
#     elif user_choice == '1':
#     else:
#         print('неверный ввод')


user_input = input('Введите 1 для старта программы по алгоритму ')

while user_input not in ['1', '2']:
    print('Ошибка ввода!')
    user_input = input()
if user_input == '1':
    print('Выполняю программу 1')
else:
    print('Выполняю программу 2')
