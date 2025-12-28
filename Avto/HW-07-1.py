7(context_menu)hero.py
1.	Добавить print(ОР) + print(ФР) для каждого шага!

8(dynamic)hero.py
1.	Для строки 22 используйте конструкцию представленную в строке: 18
2.	Для строки 22 используйте иной метод отличный от XPATH, например: ID

7.
#Проверка авторизации
#----Подключение библиотек---
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import time

# Инициализация Webdriver
print("ОР: Браузер успешно открыт, страница загружена")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://the-internet.herokuapp.com/context_menu")
driver.maximize_window()
print(f"ФР: Браузер открыт, URL: {driver.current_url}")

# Парсинг поля для контекстного меню
print("ОР: Элемент с ID 'hot-spot' найден на странице")
context_box = driver.find_element(By.ID, 'hot-spot')
print(f"ФР: Элемент найден: {context_box.tag_name}")

# Правый клик в поле :context_box
print("ОР: Выполнен правый клик по элементу, появилось контекстное меню")
action = ActionChains(driver)
action.context_click(context_box).perform()
time.sleep(3)
print("ФР: Правый клик выполнен, контекстное меню открыто")

# Переключиться на alert (popup) + проверка утверждения
print("ОР: Alert окно появилось с текстом 'You selected a context menu'")
alert = driver.switch_to.alert
alert_text = alert.text
print(f"ФР: Alert текст: '{alert_text}'")

assert "You selected a context menu" in alert_text, "Алерт не соответствует ожидаемому"
alert1 = alert.text
print(f"Тест и проверка успешно завершены, алерт={alert1}")
alert.accept()
print("ФР: Alert окно закрыто")


8.
# Проверка динамической загрузки
#----Подключение библиотек---
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Инициализация Webdriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://the-internet.herokuapp.com/dynamic_loading/1")
driver.maximize_window()

# Парсинг кнопки "Start" и клик по ней
# start_button = driver.find_element(By.TAG_NAME, "button").click() #Рабочий вариант!
start_button = driver.find_element(By.XPATH, "//div[contains(@id, 'start')]//button[text()='Start']").click() #Рабочий вариант!

# Ожидание появления динамического контента
wait = WebDriverWait(driver, 10)

# 1. Используем конструкцию, представленную в строке 18 (с явным сохранением элемента)
load_element = wait.until(EC.visibility_of_element_located((By.XPATH, "//h4[text()='Hello World!']")))

# 2. Используем иной метод отличный от XPATH - ID (предполагая, что у элемента есть id)
# Поскольку на указанной странице у элемента с текстом "Hello World!" нет ID,
# можно использовать CSS_SELECTOR с атрибутом id, если бы он был
# Пример альтернативных локаторов:
# load_element = wait.until(EC.visibility_of_element_located((By.ID, "finish"))) # Если бы был id="finish"
# load_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#finish h4"))) # CSS селектор
load_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div#finish h4"))) # Более конкретный CSS селектор

# Блок проверки
assert "Hello World!" in load_element.text, "Элемент не загрузился"
load_element1 = load_element.text
print(f"Тест завершен, текст проверки={load_element1}")

time.sleep(3)

# Дополнительный вывод для завершения теста
print("\nОР: Все шаги выполнены успешно, тест пройден")
print("ФР: Все проверки пройдены, браузер можно закрыть")

# Закрытие браузера (опционально, но рекомендуется)
driver.quit()
