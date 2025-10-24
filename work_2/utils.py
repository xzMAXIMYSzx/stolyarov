import json
import os
from datetime import datetime


def get_data_from_file(filepath):
    """
    Получает вопросы и уровни из JSON файла
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
            # Извлекаем вопросы из первого элемента массива
            questions = data[0]["questions"]
            # Извлекаем уровни из второго элемента массива
            levels = data[1]["levels"]
            return questions, levels
    except FileNotFoundError:
        print(f"Файл {filepath} не найден!")
        return [], {}
    except (json.JSONDecodeError, KeyError, IndexError) as e:
        print(f"Ошибка чтения файла {filepath}: {e}")
        return [], {}


def get_user_level(questions, user_level):
    """
    Получает вопросы для выбранного уровня сложности
    """
    level_map = {
        "легкий": 0,
        "средний": 1,
        "тяжелый": 2
    }

    level_index = level_map.get(user_level, 0)

    if level_index < len(questions):
        return questions[level_index]
    else:
        return questions[0]  # Возвращаем легкий уровень по умолчанию


def base_program(user_questions):
    """
    Основная программа тестирования
    """
    answers = {}

    for english_word, correct_translation in user_questions.items():
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


def get_result(levels, user_answers):
    """
    Получает результат тестирования
    """
    correct_count = sum(1 for is_correct in user_answers.values() if is_correct)
    total_questions = len(user_answers)

    # Получаем ранг из уровней (преобразуем число в строку для ключа)
    rank = levels.get(str(correct_count), "Неизвестный ранг")

    # Формируем списки правильных и неправильных ответов
    correct_words = [word for word, is_correct in user_answers.items() if is_correct]
    incorrect_words = [word for word, is_correct in user_answers.items() if not is_correct]

    result_text = f"Результаты тестирования:\n"
    result_text += f"Правильных ответов: {correct_count} из {total_questions}\n"
    result_text += f"Ваш ранг: {rank}\n\n"

    result_text += "Правильно отвечены слова:\n"
    for word in correct_words:
        result_text += f"- {word}\n"

    result_text += "\nНеправильно отвечены слова:\n"
    for word in incorrect_words:
        result_text += f"- {word}\n"

    return result_text


def write_result(filepath, user_answers, user_name):
    """
    Записывает результаты в файл
    """
    # Создаем папку для результатов, если ее нет
    results_dir = "results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    # Создаем уникальное имя файла
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{user_name}_{timestamp}.json"
    result_filepath = os.path.join(results_dir, filename)

    # Подготавливаем данные для сохранения
    result_data = {
        "user_name": user_name,
        "test_date": str(datetime.now()),
        "answers": user_answers,
        "correct_count": sum(1 for is_correct in user_answers.values() if is_correct),
        "total_questions": len(user_answers)
    }

    try:
        with open(result_filepath, 'w', encoding='utf-8') as file:
            json.dump(result_data, file, ensure_ascii=False, indent=2)
        print(f"Результаты сохранены в файл: {result_filepath}")
    except Exception as e:
        print(f"Ошибка при сохранении результатов: {e}")