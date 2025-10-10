# Функция, которая находит произведения чисел между num1 и num2:

def multi_num(num1, num2):
    start = min(num1, num2)
    end = max(num1, num2)
    result = 1
    for multi in range(start, end + 1):
        result *= multi
    return result


print(multi_num(num1=1, num2=4))
print(multi_num(num1=-8, num2=10))
