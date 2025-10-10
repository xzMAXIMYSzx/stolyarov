# Функция, которая отображает все четные числа между двух чисел x и y:

def math_number(x, y):
    start = min(x, y)
    end = max(x, y)
    print(f'Все четные числа между {x} и {y}')
    for num in range(start, end):

        if num % 2 == 0:
            print(num)
    return


math_number(x=3, y=10)
