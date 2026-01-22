# Объектно-ориентированный СТИЛЬ
# Сценарий: Поиск товара используя меню Магазин, добавление товара в корзину, проверка корзины, Оформление ОРДЕРА(заказа)
# Подключение библиотек
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
from faker import Faker
import time

# Подключение сторонней библиотеки Faker
fake = Faker(["ru_RU"])

def setup_browser():
    "Инициализация вебдрайвера"
    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service)
    browser.maximize_window()
    return browser

def generate_test_data():
    "Блок с рандомными переменными"
    return {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "street_address": fake.street_address(),
        "city": fake.city(),
        "state_county": fake.region(),
        "postcode": fake.postcode(),
        "phone": fake.phone_number(),
        "email": fake.email()
    }
def open_website(browser, url):
    "Открытие страницы браузера"
    #print("Попытка открыть страницу сайта")
    browser.get(url)
    #print("Страница открыта")

def navigate_to_shop(browser):
    try:
        "Навигация целевого сайта"
        browser.find_element(By.XPATH, "//nav//li[1]/a").click()

    except Exception as e:
        logging.error(f"Ошибка клика по элементу: {browser}")
        raise

def select_product_category(browser):
    # Выбор категории товара
    print("Категория товара доступна для выбора")
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Все товары"))).click()
    print("Переход на страницу выбранной нами категории")

def select_product(browser):
    # Выбор товара Будильники (Окончание 1-й части)
    print("Превью карточки товара доступно для выбора")
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='product-img']//a[3]/img"))).click()
    print("Переход на страницу карточки товара")

def set_product_quantity(browser, quantity=4):
    # Вариативное действие (очистка количества товара, quantity)
    print("quantity доступен для выбора")
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@type='number']"))).clear()
    browser.find_element(By.XPATH, "//input[@type='number']").send_keys(quantity)
    print("Поле quantity очищено")

def click_add_to_cart(browser):
    # Клик по кнопке 'add-to-cart'/Добавление товара в корзину
    print("Кнопка 'add-to-cart' доступна")
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@name='add-to-cart']"))).click()
    print("Клик по кнопке успешно выполнен, товар в корзине, редирект на страницу")

def click_cart_main(browser):
    # Клик по кнопке 'cart-main' в правом верхнем углу экрана
    print("Кнопка 'cart-main' доступна")
    time.sleep(1)
    browser.find_element(By.XPATH, "//i[@class='fa fa-shopping-cart']").click()
    print("Клик по кнопке успешно выполнен, появился pop-up")
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@class='cart-ft-btn button btn btn-primary cart-ft-btn-cart']"))).click()
    print("Переход на страницу корзины")

def click_proceed_to_checkout(browser):
    # Клик по кнопке 'Proceed to checkout'
    print("Кнопка 'Proceed to checkout' доступна")
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Proceed to check"))).click()
    print("Переход на страницу оформление заказа")


# ДЗ:Заполнить поля fields
def checkout(browser, test_data):
    # ---Заполнение формы
    print("Заполнение полей формы")
    # time.sleep(1)
    fields = [
        ('billing_first_name', test_data["first_name"]),
        ('billing_last_name', test_data["last_name"]),
        ('billing_address_1', test_data["street_address"]),
        ('billing_city', test_data["city"]),
        ('billing_state', test_data["state_county"]),
        ('billing_postcode', test_data["postcode"]),
        ('billing_phone', test_data["phone"]),
        ('billing_email', test_data["email"]),
    ]
    for name, value in fields:
        browser.find_element(By.NAME, name).send_keys(value)
    for field_name, value in fields:
        browser.find_element(By.NAME, field_name).send_keys(value)
    print("Поля формы заполнены")
    time.sleep(5)


# ДЗ:Выполнить клик по кнопке place_order
def place_order(browser):
    # Добавьте код для клика по кнопке place_order
    print("Кнопка Place Order доступна")
    try:
        place_order_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.ID, "place_order")))
        place_order_button.click()
        print("Клик по кнопке Place Order выполнен")
    except Exception as e:
        print(f"Ошибка при клике на Place Order: {e}")
        raise


def main():
    "Основная функция выполнения теста"
    try:
        # Инициализация
        browser = setup_browser()
        test_data = generate_test_data()

        # Шаги теста
        open_website(browser, "http://qa228.karpin74.beget.tech/")
        navigate_to_shop(browser)
        select_product_category(browser)
        select_product(browser)
        set_product_quantity(browser)
        click_add_to_cart(browser)
        click_cart_main(browser)
        click_proceed_to_checkout(browser)
        checkout(browser, test_data)
        place_order(browser)  # Добавлен вызов функции place_order
    finally:
        time.sleep(5)
        browser.quit()  # Рекомендую добавить закрытие браузера


if __name__ == "__main__":
    main()
