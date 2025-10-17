# 1. Запись в файл (из первого задания)
def write_poem_to_file(filename):
    """Записывает стихотворение в файл"""
    poem_lines = [
        "Если б мишки были пчелами,",
        "То они бы нипочем,",
        "Никогда и не подумали,",
        "Так высоко строить дом."
    ]

    with open(filename, 'w', encoding='utf-8') as file:
        for line in poem_lines:
            file.write(line + '\n')
    print(f"Стихотворение записано в файл '{filename}'")


# 2. Чтение из файла
def read_poem_from_file(filename):
    """
    Читает текст из файла и выводит результат в консоль,
    сохраняя оригинальное форматирование.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()

            print("Содержимое файла:")
            print("=" * 35)
            for line in lines:
                print(line, end='')  # ключевой момент - end=''
            print("=" * 35)

    except FileNotFoundError:
        print(f"Ошибка: Файл '{filename}' не найден!")
    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")


# 3. Основная программа
if __name__ == "__main__":
    filename = "мишки_пчелы.txt"

    # Сначала создаем файл (если его нет)
    write_poem_to_file(filename)



    # Затем читаем и выводим содержимое
    read_poem_from_file(filename)