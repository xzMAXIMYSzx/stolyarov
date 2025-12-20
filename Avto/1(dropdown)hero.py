# 🎄 Dropdown List - Новогодняя версия 🎅
# ----Подключение библиотек---
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
import time

print("❄️" * 40)
print("🎁 ДЕМОНСТРАЦИЯ РАБОТЫ С DROPDOWN СПИСКОМ 🎁")
print("🎄" * 40)

# Инициализация Webdriver
print("\n✨ Инициализация новогоднего драйвера...")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://the-internet.herokuapp.com/dropdown")
print("🦌 Открыта страница с Dropdown списком")
driver.maximize_window()
print("🌟 Окно браузера развернуто на весь экран")

print("\n" + "❄️" * 30)
print("🎯 ОСНОВНОЙ БЛОК КОДА")
print("🎄" * 30)

# 1) Находим элемент Dropdown
print("\n🎅 ШАГ 1: Поиск элемента Dropdown")
dropdown = driver.find_element(By.ID, "dropdown")
select = Select(dropdown)
print("✅ Элемент Dropdown найден успешно!")

# 2) Блок работы с массивом данных переменной select
print("\n🦌 ШАГ 2: Проверка всех доступных опций")
option = [option.text for option in select.options]
print(f"🎁 Найдено опций: {len(option)}")
print(f"✨ Список опций: {option}")

# Проверка наличия всех опций с праздничными сообщениями
print("\n🌟 Проверка корректности опций:")

if "Please select an option" in option:
    print("✅ Опция 'Please select an option' - ПРИСУТСТВУЕТ 🎄")
else:
    print("❌ Опция 'Please select an option' - ОТСУТСТВУЕТ 💔")

if "Option 1" in option:
    print("✅ Опция 'Option 1' - ПРИСУТСТВУЕТ 🎁")
else:
    print("❌ Опция 'Option 1' - ОТСУТСТВУЕТ 💔")

if "Option 2" in option:
    print("✅ Опция 'Option 2' - ПРИСУТСТВУЕТ ✨")
else:
    print("❌ Опция 'Option 2' - ОТСУТСТВУЕТ 💔")

# 3) Выбираем Option 1
print("\n🎅 ШАГ 3: Выбор Option 1")
select.select_by_visible_text("Option 1")
time.sleep(1)
print("🔄 Выбрана Option 1")
if select.first_selected_option.text == "Option 1":
    print("✅ Проверка: выбрана опция 'Option 1' - УСПЕХ! 🎉")
else:
    print("❌ Проверка: выбрана неверная опция")

# 4) Выбираем Option 2
print("\n🦌 ШАГ 4: Выбор Option 2")
select.select_by_visible_text("Option 2")
time.sleep(1)
print("🔄 Выбрана Option 2")
if select.first_selected_option.text == "Option 2":
    print("✅ Проверка: выбрана опция 'Option 2' - УСПЕХ! 🎉")
else:
    print("❌ Проверка: выбрана неверная опция")

print("\n" + "❄️" * 40)
print("✨ ТЕСТ УСПЕШНО ЗАВЕРШЕН! ✨")
print("🎄" * 40)
print("\n" + " " * 15 + "🎄 🎁 🎅")
print(" " * 10 + "Все опции на месте!")
print(" " * 15 + "🦌 ❄️ ✨")

# ДЗ: Проведение негативных тестов
print("\n" + "💔" * 30)
print("🎯 ДОМАШНЕЕ ЗАДАНИЕ: НЕГАТИВНЫЕ ТЕСТЫ")
print("❄️" * 30)

print("\n🌟 Негативные проверки с фейковыми утверждениями:")

try:
    # Негативный тест 1 - проверка несуществующей опции
    print("\n🎅 Негативный тест 1: Проверка несуществующей опции 'Option 3'")
    assert "Option 3" in option, "❌ Опция 'Option 3' должна отсутствовать"
    print("💔 Этот код не должен выполниться!")
except AssertionError as e:
    print(f"✅ Ожидаемая ошибка: {e}")

try:
    # Негативный тест 2 - проверка пустой строки
    print("\n🦌 Негативный тест 2: Проверка пустой строки")
    assert "" in option, "❌ Пустая строка должна отсутствовать"
    print("💔 Этот код не должен выполниться!")
except AssertionError as e:
    print(f"✅ Ожидаемая ошибка: {e}")

try:
    # Негативный тест 3 - проверка заглавных букв
    print("\n🎄 Негативный тест 3: Проверка 'OPTION 1' (заглавные)")
    assert "OPTION 1" in option, "❌ Опция 'OPTION 1' должна отсутствовать"
    print("💔 Этот код не должен выполниться!")
except AssertionError as e:
    print(f"✅ Ожидаемая ошибка: {e}")

try:
    # Негативный тест 4 - проверка с пробелом в конце
    print("\n❄️ Негативный тест 4: Проверка 'Option 1 ' (с пробелом)")
    assert "Option 1 " in option, "❌ Опция 'Option 1 ' должна отсутствовать"
    print("💔 Этот код не должен выполниться!")
except AssertionError as e:
    print(f"✅ Ожидаемая ошибка: {e}")

try:
    # Негативный тест 5 - проверка числа
    print("\n🎁 Негативный тест 5: Проверка числа 1")
    assert "1" in option, "❌ Число '1' должно отсутствовать"
    print("💔 Этот код не должен выполниться!")
except AssertionError as e:
    print(f"✅ Ожидаемая ошибка: {e}")

print("\n" + "✨" * 40)
print("🎉 ВСЕ НЕГАТИВНЫЕ ТЕСТЫ ВЫПОЛНЕНЫ!")
print("🎄" * 40)
print("\n" + " " * 10 + "❄️ Итоговая проверка завершена! ❄️")
print(" " * 8 + "С новогодним настроением тестирования!")
print("\n" + " " * 12 + "🎄 🎅 🦌 ❄️ 🎁 ✨")
print(" " * 10 + "До встречи в следующем уроке!")
print(" " * 12 + "🎄 🎅 🦌 ❄️ 🎁 ✨")

time.sleep(5)
driver.quit()
print("\n✨ Браузер закрыт. Счастливого Нового Года! 🎉")