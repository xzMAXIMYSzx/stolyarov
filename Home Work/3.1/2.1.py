# Написать программу подсчета стоимости разговора для разных
# мобильных операторов. Пользователь вводит время разговора в
# минутах и выбирает с какого на какой оператор он звонит. Вывести
# стоимость на экран. Тарифы указаны в таблице за 1 минуту

# 1. Введите время разговора
t = int(input('Сколько минут общался? 🕐: '))
cost = 0
# 2. Выберите своего оператора;
print('Пожалуйста, выберите своего оператора: ')
my_operator = input('1 - от МТС /2 - от Билайн/3 - от Мегафон: ')
# 3. Оператор собеседника:
print('Пожалуйста, выберите оператор собеседника: ')
other_operator = input('1 - на МТС/2 - на Билайн/3 - на Мегафон: ')
# 3. Проверка минут и расчет стоимости
if t < 0:
    print('⏰ Назад в будущее фильм классный, но не тут... время не идет назад...')
elif t == 0:
    print('🤔 Тот момент, когда все входящие и исходящие бесплатно - МТС (1-ый закон Кирхгофа)')
elif t > 1000:
    print('😲 плейбой, миллиардер, филантроп')
else:
   if my_operator == '1' and other_operator == '1':
       cost = t * 50
       my_operator = 'МТС'
       other_operator = 'МТС'
   elif my_operator == '1' and other_operator == '2':
       cost = t * 100
       my_operator = 'МТС'
       other_operator = 'Билайн'
   elif my_operator == '1' and other_operator == '3':
       cost = t * 150
       my_operator = 'МТС'
       other_operator = 'Мегафон'
   elif my_operator == '2' and other_operator == '1':
       cost = t * 90
       my_operator = 'Билайн'
       other_operator = 'Мтс'
   elif my_operator == '2' and other_operator == '2':
       cost = t * 60
       my_operator = 'Билайн'
       other_operator = 'Билайн'
   elif my_operator == '2' and other_operator == '3':
       cost = t * 140
       my_operator = 'Билайн'
       other_operator = 'Мегафон'
   elif my_operator == '3' and other_operator == '1':
       cost = t * 180
       my_operator = 'Мегафон'
       other_operator = 'Мтс'
   elif my_operator == '3' and other_operator == '2':
       cost = t * 200
       my_operator = 'Мегафон'
       other_operator = 'Билайн'
   elif my_operator == '3' and other_operator == '3':
       cost = t * 30
       my_operator = 'Мегафон'
       other_operator = 'Мегафон'
   else:
       print('Ошибка: выберите корректные номера операторов (1-3)')
       my_operator = None
       other_operator = None
# 4. Вывод результата
print(f'\nБыл совершен вызов от оператора "{my_operator}"  на оператор "{other_operator}"')
print(f'Время: {t} минут')
print(f'Стоимость разговора: {cost} рублей')

