# 1. Введем, то что по условию - общая зарплата менеджера (в $), премия и переменные для того, чтобы узнать лучшего
# из лучших, из лучших)
salary = 200
prize = 200
best_managers = []
best_sales = 0
best_salary = 0
salary_all = 0
# 2. Введем 3х менеджеров и их уровень:
first_manager_name = input('Введите имя 1-го менеджера: ')
first_manager_sale = float(input(f'Введите уровень продажи для {first_manager_name}: ' '$'))

second_manager_name = input('Введите имя 2-го менеджера: ')
second_manager_sale = float(input(f'Введите уровень продажи для {second_manager_name}: ' '$'))

third_manager_name = input('Введите имя 3-го менеджера: ')
third_manager_sale = float(input(f'Введите уровень продажи для {third_manager_name}: ' '$'))
# 3. Вводим для каждого менеджера
# 3.1. Для первого менеджера
if first_manager_sale < 500:
    salary1 = salary + first_manager_sale * 0.03
elif 500 <= first_manager_sale < 1000:
    salary1 = salary + first_manager_sale * 0.05
else:
    salary1 = salary + first_manager_sale * 0.08
# 3.2. Для второго менеджера
if second_manager_sale < 500:
    salary2 = salary + second_manager_sale * 0.03
elif 500 <= second_manager_sale < 1000:
    salary2 = salary + second_manager_sale * 0.05
else:
    salary2 = salary + second_manager_sale * 0.08
# 3.3. Для третьего менеджера
if third_manager_sale < 500:
    salary3 = salary + third_manager_sale * 0.03
elif 500 <= third_manager_sale < 1000:
    salary3 = salary + third_manager_sale * 0.05
else:
    salary3 = salary + third_manager_sale * 0.08
# 4. Определение лучшего
max_sale = max(first_manager_sale, second_manager_sale, third_manager_sale)
if first_manager_sale == max_sale:
    best_managers.append(first_manager_name)
    best_sales = first_manager_sale
    salary1 += prize  # добавляем премию лучшему
    best_salary = salary1
if second_manager_sale == max_sale:
    best_managers.append(second_manager_name)
    best_sales = second_manager_sale
    salary2 += prize  # добавляем премию лучшему
    best_salary = salary2
if third_manager_sale == max_sale:
    best_managers.append(third_manager_name)
    best_sales = third_manager_sale
    salary3 += prize  # добавляем премию лучшему
    best_salary = salary3

best_sales = max_sale
# Вывод результата:
if len(best_managers) == 1:
  print(f'\n🏆 лучший из лучших, из лучших менеджеров {best_managers} ')
  print(f'💰 Уровень продажи: {best_sales} $ - герой нашего времени')
  print(f'💵 Зарплата с учетом процентов и премии: {best_salary}$ можно гулять)))')
elif len(best_managers) > 1:
  print(f'\n🏆 Ничья! Лучшие менеджеры: {best_managers}')
  print(f'💰 Уровень продаж: {best_sales} $')
  print(f'💵 Каждый получает премию! {salary} $')
  print(f'💵 Зарплата с учетом процентов и премии: {best_salary}$ можно гулять)))')
else:
    print('❌ Ошибка: не удалось определить лучшего менеджера')