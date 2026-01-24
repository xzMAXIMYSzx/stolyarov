# ПРОЦЕДУРНЫЙ СТИЛЬ
# Сценарий: Поиск товара "Будильники "используя поисковую строку сайта + написание отзыва и выставление рейтинга
# Подключение библиотек
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker
import time

# Подключение сторонней библиотеки Faker
fake = Faker()
fake = Faker(["ru_RU"])

# Рандомные данные
text_review = fake.text()
author = fake.first_name()
email = fake.email()

# Инициализация вебдрайвера
link = "http://qa228.karpin74.beget.tech/"
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
browser.maximize_window()

# Открытие страницы браузера
print("Попытка открыть страницу сайта")
browser.get(link)
print("Страница открыта")

# Выбор строки поиска
print("Попытка кликнуть в поле поиска сайта")
finde = WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[class*=header-search-input]")))
finde.click()
print("Строка поиска открыта")


# Пищем в поисковой строке слово "Будильники" + клик по "type="submit" - кнопка поиска
print("Попытка набрать текст в поле поиска")
browser.find_element(By.CSS_SELECTOR, "input[class*=header-search-input]").send_keys("Будильники")
print("Текст успешно набран")

print("Поиск кнопки 'type='submit'")
button = browser.find_element(By.XPATH, "//button[@type='submit']").click()
print("Текст успешно набран")

# Переход во вкладку 'Reviews'

#ДЗ: Используя метод XPATH выполнить клик по Reviews используя текст "Reviews"
print("\nКладка 'Reviews' найдена")
reviews = WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Reviews')]")))
reviews.click()
print("Вкладка 'Reviews' успешно открыта")

#Выбор рейтинга 3 звезды
print("\nЭлемент рейтинга star-3 доступен")
star = WebDriverWait(browser, 10).until(
    #EC.element_to_be_clickable((By.XPATH, "//a[@class='star-3']"))) #Рабочий вариант
    #EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "3"))) #Рабочий вариант
    EC.element_to_be_clickable((By.XPATH, "//span/a[3]"))) #Рабочий вариант
star.click()
print("Рецйтинг star-3 установлен")

#Заполнение поля ваш комментарий
print("\nПоле comment доступно для ввода")
comment1 = WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.ID, "comment"))) #Рабочий вариант
comment1.send_keys(text_review)
print(f"Рандомный текст успешно напечатан:{text_review}")

#Заполнение поля name
print("\nПоле comment доступно для ввода")
author1 = WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.ID, "author"))) #Рабочий вариант
author1.send_keys(author)
print(f"Рандомный текст успешно напечатан:{author}")

#Заполнение поля email
print("\nПоле comment доступно для ввода")
email1 = WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.ID, "email"))) #Рабочий вариант
email1.send_keys(email)
print(f"Рандомный текст успешно напечатан:{email}")
time.sleep(3)
# Клик по кнопке 'Submit'
print("Кнопка 'Proceed to Submit' доступна")
submit = browser.find_element(By.ID, "submit").click() #Рабочий вариант использовали частичное совпадение (словоформа в кавычках не полная)
print("Отзыв отправлен")

time.sleep(8)
#Блок проверки
proverka1 = author
print(f"Ожидаемый автор: '{proverka1}'")
all_authors = browser.find_elements(By.XPATH, "//strong[@class='woocommerce-review__author']")
# Берем последнего (самого свежего)
your_author = all_authors[-1].text  # или all_authors[0] если первый
time.sleep(5)
assert your_author == proverka1, f"Тест проверку не прошел, но есть альтернатива {your_author}"
time.sleep(3)

time.sleep(10)
