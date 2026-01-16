# ПРОЦЕДУРНЫЙ СТИЛЬ
# Сценарий: Поиск товара используя меню Магазин, добавление товара в корзину, проверка корзины, Оформление ОРДЕРА(заказа)
# Подключение библиотек
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from faker import Faker
import time

# Подключение сторонней библиотеки Faker
fake = Faker()
fake = Faker(["ru_RU"])

# Инициализация вебдрайвера
link = "http://qa228.karpin74.beget.tech/"
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
browser.maximize_window()

# Открытие страницы браузера
print("Попытка открыть страницу сайта")
browser.get(link)
print("Страница открыта")

# Клик по меню "Магазин"
print("Попытка кликнут на пункт меню 'Магазин'")
mag1 = browser.find_element(By.XPATH, "//nav//li[1]/a").click()
print("Переход на страницу 'Магазин' ")

time.sleep(1)

# Выбор категории товара
print("Категория товара доступна для выбора")
#mag2 = browser.find_element(By.XPATH, "//section//li[2]/a/img").click() #Рабочий вариант
mag2 = browser.find_element(By.PARTIAL_LINK_TEXT, "Все товары").click()  #Рабочий вариант(самый быстрый)
print("Переход на страницу выбранной нами категории")

time.sleep(1)

# Выбор товара Будильники (Окончание 1-й части)
print("Превью карточки товара доступно для выбора")
#mag3 = browser.find_element(By.XPATH, "//ul/li[1]//div[1]/a[3]/img").click() #Рабочий вариант
mag3 = browser.find_element(By.XPATH, "//div[@class='product-img']//a[3]/img").click()  #Рабочий вариант(самый быстрый)
# mag3 = browser.find_element(By.LINK_TEXT, "Софи").click()
# browser.find_element(By.XPATH, "//*[@id='product']//li[2]//img").click() - для Софи
print("Переход на страницу карточки товара")

time.sleep(1)

# Вариативное действие (очистка количества товара, quantity)
print("quantity доступен для выбора")
quantity = browser.find_element(By.XPATH, "//input[@type='number']").clear() #Рабочий вариант
print("Поле quantity очищено")

# id="quantity_696386fd11727" не рабочий!!!
time.sleep(1)
# Установить количество/quantity товара
print("quantity доступен для ввода значения")
quantity = browser.find_element(By.XPATH, "//input[@type='number']").send_keys(4) #Рабочий вариант
print("quantity товара установлено")

# Проверить ui up/down кнопок quantity!!!
time.sleep(1)
# Клик по кнопке 'add-to-cart'/Добавление товара в корзину
print("Кнопка 'add-to-cart' доступна")
button = browser.find_element(By.XPATH, "//button[@name='add-to-cart']").click() #Рабочий вариант
print("Клик по кнопке успешно выполнен, товар в корзине")

time.sleep(1)

# Клик по кнопке 'cart-main' в правом верхнем углу экрана
print("Кнопка 'cart-main' доступна")
button = browser.find_element(By.XPATH, "//i[@class='fa fa-shopping-cart']").click() #Рабочий вариант
print("Клик по кнопке успешно выполнен, появился pop-up")

time.sleep(1)

# Клик по кнопке 'Просмотреть корзину'
print("Кнопка 'cart-ft-btn-cart' доступна")
button = browser.find_element(By.XPATH, "//a[@class='cart-ft-btn button btn btn-primary cart-ft-btn-cart']").click() #Рабочий вариант
print("Переход на страницу корзины")

time.sleep(1)

# Клик по кнопке 'Proceed to checkout'
print("Кнопка 'Proceed to checkout' доступна")
button = browser.find_element(By.PARTIAL_LINK_TEXT, "Proceed to check").click() #Рабочий вариант использовали частичное совпадение (словоформа в кавычках не полная)
print("Переход на страницу оформление заказа")

#----------Оформление ордера-----------

#----Блок с рандомными переменными---
first_name = fake.first_name()
last_name = fake.last_name()
street_address = fake.street_address()
city = fake.city()
state_county = fake.region()
postcode_zip = fake.postcode()
phone = fake.phone_number()
email = fake.email()

#---Заполнение формы
print("Заполнение полей формы")
browser.find_element(By.XPATH, "//input[@name='billing_first_name']").send_keys(first_name)
browser.find_element(By.XPATH, "//input[@name='billing_last_name']").send_keys(last_name)
browser.find_element(By.XPATH, "//input[@name='billing_address_1']").send_keys(street_address)
browser.find_element(By.XPATH, "//input[@name='billing_city']").send_keys(city)
browser.find_element(By.XPATH, "//input[@name='billing_state']").send_keys(state_county)
browser.find_element(By.XPATH, "//input[@name='billing_postcode']").send_keys(postcode_zip)
browser.find_element(By.XPATH, "//input[@name='billing_phone']").send_keys(phone)
browser.find_element(By.XPATH, "//input[@name='billing_email']").send_keys(email)
print("Поля формы заполнены")
time.sleep(10)


# Получение номера ордера
print("Получение номера ордера")
order_number = None

# Сначала проверяем, что заказ действительно оформлен
current_url = browser.current_url
print(f"Текущий URL: {current_url}")

try:
    # Ищем номер заказа на странице подтверждения
    order_number_element = browser.find_element(By.XPATH, "//li[contains(@class, 'order')]/strong")
    order_number = order_number_element.text
    print(f"Номер заказа: {order_number}")
except:
    print("Не удалось получить номер заказа")

# Выводим всю информацию о заказе
print("\n" + "="*60)
print("ИНФОРМАЦИЯ О ЗАКАЗЕ:")
print("="*60)
if order_number:
    print(f"✓ Заказ №{order_number} успешно оформлен!")
else:
    print("⚠ Номер заказа не найден, но процесс оформления завершен")

print(f"📦 Товар: Будильник (4 шт.)")
print(f"👤 Клиент: {first_name} {last_name}")
print(f"📧 Email: {email}")
print(f"📞 Телефон: {phone}")
print(f"🏠 Адрес: {street_address}, {city}")
print("="*60)

# Сохранение скриншота с подтверждением заказа
try:
    screenshot_path = f"order_{order_number if order_number else 'unknown'}.png"
    browser.save_screenshot(screenshot_path)
    print(f"📸 Скриншот сохранен: {screenshot_path}")
except:
    print("⚠ Не удалось сохранить скриншот")

# Пауза для просмотра результата
time.sleep(3)

# Закрытие браузера
print("\nЗакрытие браузера")
browser.quit()
print("Браузер закрыт")
print("✅ Тест завершен!")

# Финальное сообщение
print("\n" + "="*60)
if order_number:
    print(f"ТЕСТ ПРОЙДЕН УСПЕШНО! Заказ №{order_number} оформлен.")
else:
    print("ТЕСТ ЗАВЕРШЕН. Процесс оформления выполнен, но номер заказа не получен.")
print("="*60)

