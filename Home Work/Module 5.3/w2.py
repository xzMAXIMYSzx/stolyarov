# 1. Создали словари:
words_easy = {
    "family": "семья",
    "hand": "рука",
    "people": "люди",
    "evening": "вечер",
    "minute": "минута",
}

words_medium = {
    "believe": "верить",
    "feel": "чувствовать",
    "make": "делать",
    "open": "открывать",
    "think": "думать",
}

words_hard = {
    "rural": "деревенский",
    "fortune": "удача",
    "exercise": "упражнение",
    "suggest": "предлагать",
    "except": "кроме",
}

# 2. Создали уровни сложности:
levels = {
    0: "Нулевой",
    1: "Так себе",
    2: "Можно лучше",
    3: "Норм",
    4: "Хорошо",
    5: "Отлично"
}

# 3. Шаг 1: Получение уровня сложности от пользователя:
print("Выберите уровень сложности:")
print("легкий, средний, тяжелый")
user_input = input().strip().lower()

# 4. После Выбора уровня сложности, получаем список по которому  :
if user_input == "средний":
    words = words_medium
    print("Выбран уровень сложности: средний")
elif user_input == "тяжелый":
    words = words_hard
    print("Выбран уровень сложности: тяжелый")
else:
    words = words_easy
    print("Выбран уровень сложности: легкий")

print()

# 5. Шаг 2: Запуск цикла по словам
answers = {}

for english_word, correct_translation in words.items():
    # Вывод подсказки
    print(f"{english_word}, {len(correct_translation)} букв, начинается на {correct_translation[0]}...")

    # Получение ответа от пользователя
    user_answer = input().strip().lower()

    # Проверка ответа
    if user_answer == correct_translation:
        print(f"Верно. {english_word.capitalize()} — это {correct_translation}.")
        answers[english_word] = True
    else:
        print(f"Неверно. {english_word.capitalize()} — это {correct_translation}.")
        answers[english_word] = False

    print()

# 6. Шаг 3: Вывод результатов
correct_words = []
incorrect_words = []

for word, is_correct in answers.items():
    if is_correct:
        correct_words.append(word)
    else:
        incorrect_words.append(word)

print("Правильно отвечены слова:")
for word in correct_words:
    print(word)

print()

print("Неправильно отвечены слова:")
for word in incorrect_words:
    print(word)

print()

# 7. Шаг 4: Определение ранга пользователя
correct_count = len(correct_words)
rank = levels.get(correct_count)

print(f"Ваш ранг:")
print(rank)