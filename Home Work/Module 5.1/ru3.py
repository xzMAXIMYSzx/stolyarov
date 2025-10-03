# 1. Пользователь вводит текст:

text = input("Введите текст: ")

# 2. Добавим счетчик для подсчета предложений:
count = 0

# 3. Поиск в тексте предложений завершенных знаков
for completion_sign in text:
    if completion_sign == '.' or completion_sign == '!' or completion_sign == '?':
        count += 1

# 4. Вывод количество предложений:
print(f"Количество предложений в тексте: {count}")
