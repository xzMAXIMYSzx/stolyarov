# Утвердительный рейтинг
# 1. Введем переменные:
residency = float(input('Время жизни на одном месте: '))
salary = float(input('Зарплата: '))
experience = float(input('Стаж работы: '))
i = 0
if residency >= 2:
    i += 1
if salary >= 50000:
    i += 1
if experience >= 2:
    i += 1
if i == 3:
    print('Идеальный кандидат))')
else:
    print('Тренируйтесь дальше')
print('Финальный рейтинг: ', i)
