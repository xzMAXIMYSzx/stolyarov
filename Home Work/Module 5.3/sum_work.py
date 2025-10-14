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

# 8. Шаг 5: использование функций:
# 9. Функция в котором юзер получает желаемый уровень:
def get_user_level(user_input):
    """
    Получает желаемый уровень от пользователя и возвращает словарь слов
    """
    user_input = user_input.strip().lower()

    if user_input == "средний":
        words = words_medium
        print("Выбран уровень сложности: средний")
    elif user_input == "сложный" or user_input == "тяжелый":
        words = words_hard
        print("Выбран уровень сложности: сложный")
    else:
        words = words_easy
        print("Выбран уровень сложности: легкий")

    print()
    return words


# 10. Функция на входе получает список слов в зависимости от сложности
def base_program(words):
    """
    Задает вопросы, получает ответы и возвращает словарь с результатами
    """
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

    return answers

# 11. Функция принимает на вход словарь с результатами ответов и словарь уровня знаний

def get_result(answers, levels_dict):
    """
    Выводит результаты и возвращает показатель уровня знаний
    """
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

    # Определение ранга пользователя
    correct_count = len(correct_words)
    rank = levels_dict.get(correct_count)

    return rank


# 12. Основной код программы:
if __name__ == '__main__':
    user_lvl = input("Выберите уровень сложности \nлегкий, средний, сложный.\n").lower()
    user_words = get_user_level(user_lvl)
    user_answers = base_program(user_words)
    result = get_result(user_answers, levels)
    print(f"\nВаш ранг:\n{result}")