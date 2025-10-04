# 1. Пользователь вводит строку:
my_text = input('Введите текст: ')

# 2. Убираем пробелы и преобразовываем текст в нижнем регистре:
switch_text = my_text.replace(" ", "").lower()

# 3. Делаем текст наоборот:
reverse_text = switch_text[::-1]

# 4. Проверка текста на обратный текст и вывод результата:
if reverse_text == switch_text:
    print(f'слово {my_text} это Палиндром')
else:
    print(f'слово {my_text} не является Палиндром')


