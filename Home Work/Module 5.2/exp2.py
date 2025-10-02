# У нас есть текст в нем необходимо посчитать:
winnie_the_pooh ="""
Если б мишки были пчёлами,
То они бы нипочём
Никогда и не подумали
Так высоко строить дом
"""
print(winnie_the_pooh)
# 1. Количество пробелов:
space_winnie_the_pooh = winnie_the_pooh.count(' ')
print(f'количество пробелов: {space_winnie_the_pooh}')
# 2. Количество слов:
words_winnie_the_pooh = winnie_the_pooh.split()
words_len = len(words_winnie_the_pooh)
print(f"количество слов: {words_len}")
# - Количество букв 'о':
# - O O O O O
# - Леонид Ильич, это же Олимпийские игры!
# - Я вижу: O O O O O:
count_o_winnie_the_pooh = winnie_the_pooh.count('о')
print(f"количество букв о: {count_o_winnie_the_pooh}")
# 4. Cписок из слов больше 3х букв:

list_words = [word for word in words_winnie_the_pooh if len(word) > 3]
print(f"Слова больше 3х букв: {list_words}")

# 5. Полученный список list_words преобразовать в строку list_words_string при помощи .join():
list_words_string = ' '.join(list_words)

print(f"Объединенная строка: {list_words_string}")
