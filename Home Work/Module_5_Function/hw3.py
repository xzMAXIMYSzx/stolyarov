# Функция, которая отображает пустой или заполненный квадрат

def square(len_square, symbol, log):
    for i in range(len_square):
        for j in range(len_square):
            if log:
                print(symbol, end=' ')
            else:
                if i == 0 or i == len_square - 1 or j == 0 or j == len_square - 1:
                    print(symbol, end=' ')
                else:
                    print(' ', end=' ')
        print()


print("Заполненный квадрат 3x3:")
square(3, '*', True)

print("\nПустой квадрат 4x4:")
square(3, '#', False)
