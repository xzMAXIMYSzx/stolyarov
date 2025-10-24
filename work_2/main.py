# from utils import.....
#
#
# questions, levels = get_data_from_file(filepath)
# user_name = input()
# user_lever = input()
# user_questions = get_user_level(questions, user_lever)
# user_answers =base_program(user_questions)
# user_result = get_result(levels, user_answers)
# print(user_result)
# write_result(filepath, user_answers)

from utils import get_data_from_file, get_user_level, base_program, get_result, write_result

filepath = "questions.json"

# Получаем вопросы и уровни из файла
questions, levels = get_data_from_file(filepath)

# Получаем имя пользователя
user_name = input("Введите ваше имя: ").strip()

# Получаем уровень сложности
print("Выберите уровень сложности (легкий, средний, тяжелый):")
user_level = input().strip().lower()

# Получаем вопросы для выбранного уровня
user_questions = get_user_level(questions, user_level)

# Запускаем основную программу тестирования
user_answers = base_program(user_questions)

# Получаем результат
user_result = get_result(levels, user_answers)

# Выводим результат
print(user_result)

# Сохраняем результаты
write_result(filepath, user_answers, user_name)