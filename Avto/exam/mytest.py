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
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    return driver


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


def open_website(driver, url):
    "Открытие страницы браузера"
    print(f"Попытка открыть страницу сайта: {url}")
    driver.get(url)
    print("Страница открыта")


def navigate_to_shop(driver):
    "Навигация целевого сайта"
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//nav//li[1]/a"))).click()
        print("Навигация в магазин выполнена")
    except Exception as e:
        logging.error(f"Ошибка клика по элементу: {e}")
        raise


def select_product_category(driver):
    # Выбор категории товара
    print("Категория товара доступна для выбора")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Электроника"))).click()
    print("Переход на страницу выбранной нами категории")


def select_product(driver):
    # Выбор товара Будильники (Окончание 1-й части)
    print("Превью карточки товара доступно для выбора")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='product-img']//a[3]/img"))).click()
    print("Переход на страницу карточки товара")


def set_product_quantity(driver, quantity=1):
    # Вариативное действие (очистка количества товара, quantity)
    print("Поле quantity доступно для выбора")
    quantity_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@type='number']")))
    quantity_input.clear()
    quantity_input.send_keys(str(quantity))
    print(f"Поле quantity очищено и установлено значение {quantity}")


def click_add_to_cart(driver):
    # Клик по кнопке 'add-to-cart'/Добавление товара в корзину
    print("Кнопка 'add-to-cart' доступна")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@name='add-to-cart']"))).click()
    print("Клик по кнопке успешно выполнен, товар в корзине")


def click_cart_main(driver):
    # Клик по кнопке 'cart-main' в правом верхнем углу экрана
    print("Кнопка 'cart-main' доступна")
    time.sleep(2)  # Небольшая задержка для уверенности

    # Клик по иконке корзины
    driver.find_element(By.XPATH, "//i[@class='fa fa-shopping-cart']").click()
    print("Клик по кнопке корзины выполнен")

    # Ожидание появления pop-up и клик по кнопке перехода в корзину
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//a[@class='cart-ft-btn button btn btn-primary cart-ft-btn-cart']"))).click()
    print("Переход на страницу корзины")


def click_proceed_to_checkout(driver):
    # Клик по кнопке 'Proceed to checkout'
    print("Кнопка 'Proceed to checkout' доступна")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Proceed to check"))).click()
    print("Переход на страницу оформления заказа")


def checkout(driver, test_data):
    # Заполнение полей формы
    print("Начало заполнения полей формы")
    time.sleep(2)  # Даем время на загрузку формы

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

    for field_name, value in fields:
        try:
            # Ждем появления поля и заполняем его
            field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, field_name))
            )
            field.clear()
            field.send_keys(value)
            print(f"Поле {field_name} заполнено значением: {value}")
        except Exception as e:
            print(f"Ошибка при заполнении поля {field_name}: {e}")

    print("Все поля формы заполнены")
    time.sleep(3)


def place_order(driver):
    # Клик по кнопке place_order
    print("Поиск кнопки Place Order")
    try:
        # Пробуем разные локаторы для кнопки Place Order
        place_order_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH,
                                        "//button[@id='place_order'] | //button[contains(@class, 'place-order')] | //button[@type='submit' and contains(text(), 'Place order')] | //button[@class='button alt']"))
        )

        # Прокрутка к кнопке
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", place_order_button)
        time.sleep(2)

        # Пробуем кликнуть через JavaScript, если обычный клик не работает
        try:
            place_order_button.click()
        except:
            driver.execute_script("arguments[0].click();", place_order_button)

        print("Клик по кнопке Place Order выполнен")

    except Exception as e:
        print(f"Ошибка при клике на Place Order: {e}")

        # Дополнительная диагностика
        print("Поиск всех кнопок на странице:")
        buttons = driver.find_elements(By.TAG_NAME, "button")
        for i, button in enumerate(buttons):
            print(
                f"Кнопка {i}: текст='{button.text}', класс='{button.get_attribute('class')}', id='{button.get_attribute('id')}'")
        raise


def main():
    "Основная функция выполнения теста"
    driver = None
    try:
        # Инициализация
        driver = setup_browser()
        test_data = generate_test_data()

        print("Начало выполнения теста")
        print(f"Сгенерированные тестовые данные: {test_data}")

        # Шаги теста
        open_website(driver, "http://qa228.karpin74.beget.tech/")
        navigate_to_shop(driver)
        select_product_category(driver)
        select_product(driver)
        set_product_quantity(driver, 1)  # Устанавливаем количество 1
        click_add_to_cart(driver)
        click_cart_main(driver)
        click_proceed_to_checkout(driver)
        checkout(driver, test_data)
        place_order(driver)

        print("Тест успешно завершен!")

    except Exception as e:
        print(f"Тест завершился с ошибкой: {e}")
        if driver:
            # Делаем скриншот при ошибке
            driver.save_screenshot("error_screenshot.png")
            print("Скриншот ошибки сохранен как error_screenshot.png")
    finally:
        if driver:
            time.sleep(5)
            driver.quit()
            print("Браузер закрыт")


if __name__ == "__main__":
    main()
