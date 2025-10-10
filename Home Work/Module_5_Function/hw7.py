# Напишите функцию, которая определяет, является число палиндромом или нет:

def pali_num(num):
    num_str = str(num)
    return num_str == num_str[::-1]


print(pali_num(num=121))
