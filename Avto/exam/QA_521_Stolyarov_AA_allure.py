# Объектно-ориентированный СТИЛЬ
# Сценарий: Поиск товара используя поиск, добавление в корзину, оформление заказа и отзыв
# Подключение библиотек
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import logging
from faker import Faker
import time
import os

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Подключение сторонней библиотеки Faker
fake = Faker(["ru_RU"])


# ============================================================
# ФУНКЦИЯ ПРИКРЕПЛЕНИЯ СКРИНШОТА К ОТЧЕТУ ALLURE
# ============================================================
def attach_screenshot(driver, step_name):
    try:
        screenshot = driver.get_screenshot_as_png()
        allure.attach(screenshot, name=f"Screenshot: {step_name}",
                      attachment_type=allure.attachment_type.PNG)
        logger.info(f"Скриншот {step_name} прикреплен к отчету Allure")
    except Exception as e:
        logger.warning(f"Не удалось прикрепить скриншот: {e}")


# ============================================================
# Pytest Fixture для драйвера (УПРОЩЕННАЯ ВЕРСИЯ)
# ============================================================
@pytest.fixture(scope="function")
def driver():
    logger.info("=" * 50)
    logger.info("ИНИЦИАЛИЗАЦИЯ ВЕБДРАЙВЕРА")
    logger.info("=" * 50)

    driver = None
    try:
        with allure.step("Инициализация веб-драйвера Chrome"):
            # Минимальные опции для стабильной работы
            chrome_options = webdriver.ChromeOptions()

            # Только основные опции
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")

            # Добавляем опции для стабильности
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")

            # Убираем экспериментальные опции, которые могут вызывать проблемы

            # Автоматическая установка драйвера
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)

            # Простой скрипт для обхода автоматизации
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

            logger.info("WebDriver успешно инициализирован")
            attach_screenshot(driver, "Инициализация_драйвера")

        yield driver

    except Exception as e:
        logger.error(f"Ошибка при инициализации драйвера: {e}")
        raise
    finally:
        if driver:
            with allure.step("Закрытие веб-драйвера"):
                logger.info("Закрытие браузера...")
                try:
                    attach_screenshot(driver, "Финальный_скриншот")
                except:
                    pass
                driver.quit()
                logger.info("Браузер закрыт")


# ============================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ============================================================
def generate_test_data():
    """Блок с рандомными переменными для заказа"""
    data = {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "street_address": fake.street_address(),
        "city": fake.city(),
        "state_county": fake.region(),
        "postcode": fake.postcode(),
        "phone": fake.phone_number(),
        "email": fake.email()
    }
    logger.debug(f"Сгенерированы тестовые данные для заказа")
    return data


def generate_review_data():
    """Блок с рандомными переменными для отзыва"""
    data = {
        "review_text": fake.text(max_nb_chars=200),
        "author": "КоТвМешке",
        "email": fake.email()
    }
    logger.debug(f"Сгенерированы данные для отзыва: автор={data['author']}")
    return data


# ============================================================
# БАЗОВЫЕ БЕЗОПАСНЫЕ ФУНКЦИИ
# ============================================================
def safe_wait_for_element(driver, by, value, timeout=10):
    """Безопасное ожидание элемента"""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        logger.debug(f"Элемент найден: {by}={value}")
        return element
    except TimeoutException:
        logger.error(f"Элемент не найден за {timeout}с: {by}={value}")
        raise


def safe_wait_for_clickable(driver, by, value, timeout=10):
    """Безопасное ожидание кликабельного элемента"""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )
        logger.debug(f"Элемент кликабелен: {by}={value}")
        return element
    except TimeoutException:
        logger.error(f"Элемент не кликабелен за {timeout}с: {by}={value}")
        raise


def safe_wait_for_visible(driver, by, value, timeout=10):
    """Безопасное ожидание видимого элемента"""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((by, value))
        )
        logger.debug(f"Элемент видим: {by}={value}")
        return element
    except TimeoutException:
        logger.error(f"Элемент не видим за {timeout}с: {by}={value}")
        raise


def safe_click(driver, by, value, max_attempt=3):
    """Безопасное выполнение клика по элементу с повторными попытками"""
    for attempt in range(max_attempt):
        try:
            element = safe_wait_for_clickable(driver, by, value)
            element.click()
            logger.info(f"Успешный клик по элементу: {by}={value}")
            return True
        except Exception as e:
            logger.warning(f"Попытка {attempt + 1}/{max_attempt} не удалась: {str(e)}")
            time.sleep(1)
    logger.error(f"Не удалось кликнуть по элементу после {max_attempt} попыток")
    raise Exception(f"Элемент {by}={value} не кликабелен")


def safe_send_keys(driver, by, value, text, clear_first=True):
    """Безопасный ввод текста в поле ввода"""
    try:
        element = safe_wait_for_visible(driver, by, value)
        if clear_first:
            element.clear()
        element.send_keys(text)
        logger.info(f"Успешно введен текст в элемент: {by}={value}")
        return element
    except Exception as e:
        logger.error(f"Ошибка при вводе текста: {str(e)}")
        raise Exception(f"Элемент {by}={value} не доступен для ввода")


def safe_scroll_to_element(driver, by, value, timeout=10):
    """Безопасная прокрутка к элементу"""
    try:
        element = safe_wait_for_element(driver, by, value, timeout)
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", element)
        logger.info(f"Прокрутка к элементу выполнена: {by}={value}")
        time.sleep(1)
        return element
    except Exception as e:
        logger.error(f"Ошибка при прокрутке: {str(e)}")
        raise


def safe_get_text(driver, by, value, timeout=10):
    """Безопасное получение текста элемента"""
    try:
        element = safe_wait_for_element(driver, by, value, timeout)
        text = element.text
        logger.debug(f"Текст элемента {by}={value}: {text}")
        return text
    except Exception as e:
        logger.error(f"Ошибка при получении текста: {str(e)}")
        raise


# ============================================================
# ФУНКЦИИ ДЕЙСТВИЙ (с шагами Allure)
# ============================================================
@allure.step("Открытие сайта: {url}")
def open_website(driver, url):
    logger.info(f"Открытие сайта: {url}")
    driver.get(url)
    safe_wait_for_element(driver, By.XPATH, "//nav")
    logger.info("Сайт успешно открыт")
    attach_screenshot(driver, "Открытие_сайта")


@allure.step("Поиск товара 'Шляпы'")
def search_for_hats(driver):
    logger.info("Поиск товара 'Шляпы'")

    input_field = safe_wait_for_element(driver, By.XPATH, "//*[@id='main-header6']//input[2]")
    input_field.clear()
    input_field.send_keys("Шляпы")
    logger.info("Текст 'Шляпы' введен в поле поиска")
    time.sleep(2)

    button = driver.find_element(By.XPATH, "//button[contains(@class, 'header-search-button')]")
    button.click()
    logger.info("Клик по кнопке поиска выполнен")

    time.sleep(3)
    safe_wait_for_element(driver, By.XPATH, "//input[@type='number']")
    logger.info("Страница товара загружена")
    attach_screenshot(driver, "Результаты_поиска")


@allure.step("Установка количества товара: {quantity}")
def set_product_quantity(driver, quantity=1):
    logger.info(f"Установка количества товара: {quantity}")
    safe_send_keys(driver, By.XPATH, "//input[@type='number']", str(quantity), clear_first=True)
    logger.info(f"Количество товара установлено на {quantity}")


@allure.step("Добавление товара в корзину")
def click_add_to_cart(driver):
    logger.info("Добавление товара в корзину")
    safe_click(driver, By.XPATH, "//button[@name='add-to-cart']")
    safe_wait_for_visible(driver, By.XPATH, "//i[@class='fa fa-shopping-cart']")
    logger.info("Товар успешно добавлен в корзину")
    attach_screenshot(driver, "Товар_в_корзине")


@allure.step("Переход в корзину")
def click_cart_main(driver):
    logger.info("Открытие корзины")

    safe_click(driver, By.XPATH, "//i[@class='fa fa-shopping-cart']")
    logger.info("Клик по иконке корзины выполнен")

    safe_click(driver, By.XPATH, "//a[@class='cart-ft-btn button btn btn-primary cart-ft-btn-cart']")
    logger.info("Переход на страницу корзины выполнен")
    attach_screenshot(driver, "Страница_корзины")

    safe_wait_for_element(driver, By.PARTIAL_LINK_TEXT, "Proceed to check")


@allure.step("Переход к оформлению заказа")
def click_proceed_to_checkout(driver):
    logger.info("Переход к оформлению заказа")
    safe_click(driver, By.PARTIAL_LINK_TEXT, "Proceed to check")
    safe_wait_for_element(driver, By.NAME, "billing_first_name")
    logger.info("Переход на страницу оформления заказа выполнен")
    attach_screenshot(driver, "Оформление_заказа")


@allure.step("Заполнение формы заказа")
def checkout(driver, test_data):
    logger.info("Начало заполнения формы заказа")

    safe_wait_for_element(driver, By.NAME, "billing_first_name")

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
        safe_send_keys(driver, By.NAME, field_name, value, clear_first=True)
        logger.debug(f"Поле {field_name} заполнено")

    logger.info("Все поля формы успешно заполнены")
    attach_screenshot(driver, "Форма_заполнена")


@allure.step("Оформление заказа (Place Order)")
def place_order(driver):
    logger.info("Оформление заказа")

    place_order_button = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH,
                                        "//button[@id='place_order'] | " +
                                        "//button[contains(@class, 'place-order')] | " +
                                        "//button[@type='submit' and contains(text(), 'Place order')] | " +
                                        "//button[@class='button alt']"))
    )

    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", place_order_button)
    time.sleep(1)

    try:
        place_order_button.click()
        logger.info("Клик по кнопке выполнен (обычный клик)")
    except:
        driver.execute_script("arguments[0].click();", place_order_button)
        logger.info("Клик по кнопке выполнен (JavaScript)")

    time.sleep(2)
    attach_screenshot(driver, "Заказ_оформлен")


@allure.step("Оставление отзыва")
def leave_review(driver, review_data):
    logger.info("Начало процесса оставления отзыва")

    safe_scroll_to_element(driver, By.XPATH, "//a[@href='#tab-reviews']")
    safe_click(driver, By.XPATH, "//a[@href='#tab-reviews']")
    logger.info("Переход на вкладку с отзывами выполнен")

    logger.info("Установка рейтинга 3 звезды")
    try:
        safe_click(driver, By.XPATH, "//a[@class='star-3']")
        logger.info("Рейтинг star-3 найден по классу")
    except:
        safe_click(driver, By.XPATH, "//span/a[3]")
        logger.info("Рейтинг 3 звезды найден по индексу")

    safe_send_keys(driver, By.ID, "comment", review_data["review_text"], clear_first=False)
    safe_send_keys(driver, By.ID, "author", review_data["author"], clear_first=True)
    safe_send_keys(driver, By.ID, "email", review_data["email"], clear_first=True)

    safe_scroll_to_element(driver, By.ID, "submit")
    safe_click(driver, By.ID, "submit")
    logger.info("Отзыв отправлен")
    time.sleep(2)
    attach_screenshot(driver, "Отзыв_отправлен")


@allure.step("Проверка автора отзыва: {expected_author}")
def verify_review_author(driver, expected_author):
    logger.info(f"Поиск автора '{expected_author}' среди всех отзывов")

    try:
        safe_wait_for_element(driver, By.XPATH, "//p[@class='meta']", timeout=15)

        authors = driver.find_elements(By.XPATH, "//p[@class='meta']//strong[@class='woocommerce-review__author']")
        logger.info(f"Найдено отзывов: {len(authors)}")

        for i, author_element in enumerate(authors, 1):
            author_text = author_element.text
            logger.info(f"Отзыв {i}: автор '{author_text}'")

            if author_text == expected_author:
                logger.info(f"✅ Найден нужный автор '{expected_author}' в отзыве №{i}")
                attach_screenshot(driver, f"Найден_автор_{expected_author}")
                return True

        all_authors = [a.text for a in authors]
        logger.error(f"❌ Автор '{expected_author}' не найден. Все авторы: {all_authors}")
        raise AssertionError(f"Автор '{expected_author}' не найден в списке отзывов")

    except TimeoutException:
        logger.error("Отзывы не загрузились")
        driver.save_screenshot(f"no_reviews_{time.strftime('%Y%m%d_%H%M%S')}.png")
        raise


# ============================================================
# ТЕСТОВЫЙ КЛАСС
# ============================================================
@allure.feature("Магазин")
@allure.story("Оформление заказа и отзыв")
class TestShop:

    @allure.title("Тест: Поиск шляп, оформление заказа и отзыв")
    @allure.description(
        "Тест проверяет полный цикл: поиск товара -> добавление в корзину -> оформление заказа -> отзыв")
    def test_full_order_flow(self, driver):
        start_time = time.time()

        with allure.step("Подготовка тестовых данных"):
            order_data = generate_test_data()
            review_data = generate_review_data()

            logger.info(f"Данные заказа: {order_data['first_name']} {order_data['last_name']}")
            logger.info(f"Данные отзыва: автор={review_data['author']}")

        with allure.step("Часть 1: Оформление заказа"):
            open_website(driver, "http://qa228.karpin74.beget.tech/")
            search_for_hats(driver)
            set_product_quantity(driver, 1)
            click_add_to_cart(driver)
            click_cart_main(driver)
            click_proceed_to_checkout(driver)
            checkout(driver, order_data)
            place_order(driver)
            time.sleep(2)

        with allure.step("Часть 2: Оставление отзыва"):
            logger.info("Возврат на главную страницу")
            driver.get("http://qa228.karpin74.beget.tech/")
            time.sleep(2)

            search_for_hats(driver)
            leave_review(driver, review_data)

        with allure.step("Часть 3: Проверка отзыва"):
            verify_review_author(driver, review_data["author"])

        elapsed_time = time.time() - start_time
        logger.info(f"✅ ТЕСТ УСПЕШНО ЗАВЕРШЕН за {elapsed_time:.2f} секунд")
        attach_screenshot(driver, "Тест_успешно_завершен")


# ============================================================
# ТОЧКА ВХОДА (для запуска через pytest)
# ============================================================
if __name__ == "__main__":
    # Запуск теста через pytest
    pytest.main([__file__, "-v", "-s", "--alluredir=allure-results"])
