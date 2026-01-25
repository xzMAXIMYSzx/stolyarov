# ПРОЦЕДУРНЫЙ СТИЛЬ
# Сценарий: Поиск товара "Будильники "используя поисковую строку сайта + написание отзыва и выставление рейтинга
# Подключение библиотек
import random
import string

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from faker import Faker
import time

# 1.Инициализация Webdriver
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
browser.get('https://demoblaze.com')
browser.maximize_window()

time.sleep(3)

# 2. Генерация случайных данных
# 2.1 Данные для регистрации и авторизации на сайте
user_name = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
my_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

# user_name = "cfkj000"
# my_password = "12345678"

# 2.2. Данные для получения ордера
my_name = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
my_country = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
my_city = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
my_credicard = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
now_month = ''.join(random.choices(string.ascii_letters + string.digits, k=2))
now_year = ''.join(random.choices(string.ascii_letters + string.digits, k=4))

# 3. Прокрутка страницы к кнопке Sign up
sign_up_button = WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.ID, "signin2")))
time.sleep(1)
browser.execute_script("arguments[0].scrollIntoView(true);", sign_up_button)
time.sleep(3)
sign_up_button.click()
time.sleep(1)
print(f'{my_password}')

# 4. Ввод данных для регистрации
WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.ID, "sign-username"))).send_keys(user_name)
print(f'{my_password}')
WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.ID, "sign-password"))).send_keys(my_password)
WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[text()= 'Sign up']"))).click()
time.sleep(3)

alert = browser.switch_to.alert
alert.accept()

# 5. Авторизация на сайте
print("Попытка кликнуть в поле поиска сайта")
WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.ID, "login2"))).click()
print("Строка поиска открыта")
#---Заполнение формы
print("Заполнение полей формы")
WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.ID, "loginusername"))).send_keys(user_name)
WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.ID, "loginpassword"))).send_keys(my_password)
WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[text()= 'Log in']"))).click()
time.sleep(3)

# 6. Работа с категориями товаров
# 6.1. Выбор категории
browser.find_element(By.PARTIAL_LINK_TEXT, "Phones").click()

# 6.2. Выбор товара: 1) Samsung galaxy s6
product = browser.find_element(By.XPATH, "//*[@id='tbodyid']/div[1]/div/a/img").click()
time.sleep(2)

# 6.3. Добавить товар в корзину
WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//a[@onclick='addToCart(1)']"))).click()
time.sleep(1)

# 6.4. Закрываем аллерт после добавления в корзину
alert = browser.switch_to.alert
alert.accept()

# 6.5. Возврат на главную страницу
WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="navbarExample"]/ul/li[1]/a'))).click()
time.sleep(1)

# 6.6. Выбор товара: 2 Nokia lumia 1520
product = browser.find_element(By.XPATH, "//*[@id='tbodyid']/div[2]/div/a/img").click()
time.sleep(2)

# 6.7. Добавить товар в корзину
WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//a[@onclick='addToCart(2)']"))).click()
time.sleep(1)

# 6.8. Закрываем аллерт после добавления в корзину
alert = browser.switch_to.alert
alert.accept()

# 7. Переход в корзину товара
WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.ID, "cartur"))).click()

# 8. Переход на страницу оформления ордера
WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[text()='Place Order']"))).click()
time.sleep(2)

# 9. Заполнение и отправка формы
print("Заполнение полей формы")
WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.ID, "name"))).send_keys(my_name)
WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.ID, "country"))).send_keys(my_country)
WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.ID, "city"))).send_keys(my_city)
WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.ID, "card"))).send_keys(my_credicard)
WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.ID, "month"))).send_keys(now_month)
WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.ID, "year"))).send_keys(now_year)
WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[text()= 'Purchase']"))).click()

# 10. Проверить что покупка совершилась
conf = WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.CLASS_NAME, "sweet-alert"))).text
assert "Thank you for your purchase!" in conf, "Покупка не удалась"
print('Тест завершен')
time.sleep(10)

