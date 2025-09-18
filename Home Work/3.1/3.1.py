# Зарплата менеджера составляет 200$ + процент от продаж, продажи
# до 500$ — 3%, от 500 до 1000 — 5%, свыше 1000 — 8%. Пользователь
# вводит с клавиатуры уровень продаж для трех менеджеров.
# Определить их зарплату, определить лучшего менеджера,
# начислить ему премию 200$, вывести итоги на экран (в итогах имя
# менеджера и его зарплата с учетом процентов и премии)

# 1. Введем, то что по условию - общая зарплата менеджера (в $), премия и переменные для того, чтобы узнать лучшего
# из лучших, из лучших)
salary = 200
prize = 200
best_manager = ""
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
if first_manager_sale > second_manager_sale and first_manager_sale > third_manager_sale:
    best_manager = first_manager_name
    best_sales = first_manager_sale
    salary1 += prize  # добавляем премию лучшему
    best_salary = salary1
elif second_manager_sale > first_manager_sale and second_manager_sale > third_manager_sale:
    best_manager = second_manager_name
    best_sales = second_manager_sale
    salary2 += prize  # добавляем премию лучшему
    best_salary = salary2
else:
    best_manager = third_manager_name
    best_sales = third_manager_sale
    salary3 += prize  # добавляем премию лучшему
    best_salary = salary3

# Лучший менеджер и его зарплата с учетом процентов и премии
print(f'\n🏆 лучший из лучших, из лучших менеджеров - {best_manager}, ты настоящий бог маркетинга!!!')
print(f'💰 Уровень продажи: {best_sales} $, у специалиста большой талант')
print(f'💵 Зарплата с учетом процентов и премии: {best_salary}$, а вот теперь можно заказать стаканчик колы)))')


