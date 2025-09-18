# Скопируйте данный код себе в редактор, программу пишите в
# середине:
word_list = []
while len(word_list) < 5:
    word = input("Введите слово состоящее не менее чем из 5 букв: ")
    if len(word) < 5:
        print(f"Неверно! В слове '{word}' {len(word)} букв, введите не менее чем из 5ти:")
    else:
        word_list.append(word)

for word in word_list:
    print(f"Вы ввели слово {word}")