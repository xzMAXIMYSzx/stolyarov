# a = 0
# b = input('Введите сумму расходов за месяц или нажмите или введите stop для вывода итогов: ')
#
# while b != 'stop':
#     b = abs(float(b))
#     a += b
#     b = input('Введите сумму расходов за месяц или нажмите или введите stop для вывода итогов: ')
#
# print(f'Сумма расходов итого: {a}')

shop_list = []

while True:
    user_good = input('Введите, покупку или стоп: ')
    if user_good == 'стоп':
        break
    else:
        shop_list.append(user_good)
print(shop_list)

for item in shop_list:
    print(item)
    
[print(item) for item in shop_list]
