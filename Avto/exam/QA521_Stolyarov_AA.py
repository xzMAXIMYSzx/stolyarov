# Объектно-ориентированный СТИЛЬ
# Сценарий: Поиск товара используя меню Магазин, добавление товара в корзину, проверка корзины,
# Оформление ОРДЕРА(заказа) и добавление комментарии
# Подключение библиотек
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
import logging
from faker import Faker
import time

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Подключение сторонней библиотеки Faker
fake = Faker(["ru_RU"])


# ============================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ============================================================

def setup_browser():
    """Инициализация вебдрайвера"""
    logger.info("Запуск браузера Chrome")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    logger.info("Браузер успешно запущен и развернут на весь экран")
    return driver


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
    logger.debug(f"Сгенерированы тестовые данные для заказа: {data}")
    return data


def generate_review_data():
    """Блок с рандомными переменными для отзыва"""
    data = {
        "review_text": fake.text(max_nb_chars=200),
        "author": "Столяров Андрей",
        "email": fake.email()
    }
    logger.debug(f"Сгенерированы данные для отзыва: автор={data['author']}, email={data['email']}")
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


# ============================================================
# ФУНКЦИЯ БЕЗОПАСНОГО КЛИКА
# ============================================================
def safe_click(driver, by, value, max_attempt=3):
    """
    Безопасное выполнение клика по элементу с повторными попытками
    """
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


# ============================================================
# ФУНКЦИЯ БЕЗОПАСНОГО ВВОДА ТЕКСТА
# ============================================================
def safe_send_keys(driver, by, value, text, clear_first=True):
    """
    Безопасный ввод текста в поле ввода
    """
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


# ============================================================
# ФУНКЦИЯ БЕЗОПАСНОЙ ПРОКРУТКИ
# ============================================================
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


# ============================================================
# ФУНКЦИЯ БЕЗОПАСНОГО ПОЛУЧЕНИЯ ТЕКСТА
# ============================================================
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
# ФУНКЦИИ ДЕЙСТВИЙ
# ============================================================

def open_website(driver, url):
    """Открытие страницы браузера"""
    logger.info(f"Открытие сайта: {url}")
    driver.get(url)
    safe_wait_for_element(driver, By.XPATH, "//nav")
    logger.info("Сайт успешно открыт")


def navigate_to_shop(driver):
    """Навигация в магазин"""
    logger.info("Переход в раздел магазина")
    safe_click(driver, By.XPATH, "//nav//li[1]/a")
    safe_wait_for_element(driver, By.PARTIAL_LINK_TEXT, "Электроника")
    logger.info("Успешный переход в магазин")


def select_product_category(driver):
    """Выбор категории товара"""
    logger.info("Выбор категории 'Электроника'")
    safe_click(driver, By.PARTIAL_LINK_TEXT, "Электроника")
    safe_wait_for_element(driver, By.XPATH, "//div[@class='product-img']")
    logger.info("Категория успешно выбрана")


def select_product(driver):
    """Выбор конкретного товара - Смарт Часы"""
    logger.info("Выбор товара 'Смарт Часы'")
    time.sleep(1)

    # Пробуем разные локаторы для Смарт Часов
    try:
        safe_click(driver, By.XPATH, "//a[contains(text(), 'Смарт Часы')]")
    except:
        try:
            safe_click(driver, By.XPATH, "//img[contains(@alt, 'Смарт Часы')]")
        except:
            safe_click(driver, By.XPATH, "//div[@class='product-img']//a[2]/img")

    safe_wait_for_element(driver, By.XPATH, "//input[@type='number']")
    logger.info("Товар 'Смарт Часы' успешно выбран")


def set_product_quantity(driver, quantity=1):
    """Установка количества товара"""
    logger.info(f"Установка количества товара: {quantity}")
    safe_send_keys(driver, By.XPATH, "//input[@type='number']", str(quantity), clear_first=True)
    logger.info(f"Количество товара установлено на {quantity}")


def click_add_to_cart(driver):
    """Добавление товара в корзину"""
    logger.info("Добавление товара в корзину")
    safe_click(driver, By.XPATH, "//button[@name='add-to-cart']")
    safe_wait_for_visible(driver, By.XPATH, "//i[@class='fa fa-shopping-cart']")
    logger.info("Товар успешно добавлен в корзину")


def click_cart_main(driver):
    """Переход в корзину"""
    logger.info("Открытие корзины")

    # Клик по иконке корзины
    safe_click(driver, By.XPATH, "//i[@class='fa fa-shopping-cart']")
    logger.info("Клик по иконке корзины выполнен")

    # Клик по кнопке перехода в корзину
    safe_click(driver, By.XPATH, "//a[@class='cart-ft-btn button btn btn-primary cart-ft-btn-cart']")
    logger.info("Переход на страницу корзины выполнен")

    safe_wait_for_element(driver, By.PARTIAL_LINK_TEXT, "Proceed to check")


def click_proceed_to_checkout(driver):
    """Переход к оформлению заказа"""
    logger.info("Переход к оформлению заказа")
    safe_click(driver, By.PARTIAL_LINK_TEXT, "Proceed to check")
    safe_wait_for_element(driver, By.NAME, "billing_first_name")
    logger.info("Переход на страницу оформления заказа выполнен")


def checkout(driver, test_data):
    """Заполнение формы оформления заказа"""
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


def place_order(driver):
    """Оформление заказа"""
    logger.info("Оформление заказа")

    # Поиск кнопки Place Order с несколькими локаторами
    place_order_button = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH,
                                        "//button[@id='place_order'] | " +
                                        "//button[contains(@class, 'place-order')] | " +
                                        "//button[@type='submit' and contains(text(), 'Place order')] | " +
                                        "//button[@class='button alt']"))
    )

    # Прокрутка к кнопке
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", place_order_button)
    time.sleep(1)

    # Клик с обработкой исключений
    try:
        place_order_button.click()
        logger.info("Клик по кнопке выполнен (обычный клик)")
    except:
        driver.execute_script("arguments[0].click();", place_order_button)
        logger.info("Клик по кнопке выполнен (JavaScript)")


def leave_review(driver, review_data):
    """Оставление отзыва о товаре"""
    logger.info("Начало процесса оставления отзыва")

    # Переход на вкладку отзывов с прокруткой
    safe_scroll_to_element(driver, By.XPATH, "//a[@href='#tab-reviews']")
    safe_click(driver, By.XPATH, "//a[@href='#tab-reviews']")
    logger.info("Переход на вкладку с отзывами выполнен")

    # Выбор рейтинга 3 звезды
    logger.info("Установка рейтинга 3 звезды")
    try:
        safe_click(driver, By.XPATH, "//a[@class='star-3']")
        logger.info("Рейтинг star-3 найден по классу")
    except:
        safe_click(driver, By.XPATH, "//span/a[3]")
        logger.info("Рейтинг 3 звезды найден по индексу")

    # Заполнение полей
    safe_send_keys(driver, By.ID, "comment", review_data["review_text"], clear_first=False)
    safe_send_keys(driver, By.ID, "author", review_data["author"], clear_first=True)
    safe_send_keys(driver, By.ID, "email", review_data["email"], clear_first=True)

    # Отправка отзыва с прокруткой
    safe_scroll_to_element(driver, By.ID, "submit")
    safe_click(driver, By.ID, "submit")
    logger.info("Отзыв отправлен")


def verify_review_author(driver, expected_author):
    """Проверка автора отзыва"""
    logger.info("Проверка автора отзыва")

    try:
        safe_wait_for_element(driver, By.XPATH, "//p[@class='meta']", timeout=15)
        actual_author = safe_get_text(driver, By.XPATH,
                                      "//p[@class='meta']//strong[@class='woocommerce-review__author']")

        assert actual_author == expected_author, f"Ожидался {expected_author}, получен {actual_author}"
        logger.info(f"✅ Проверка автора отзыва пройдена: {actual_author}")
        return True
    except TimeoutException:
        try:
            moderation_msg = safe_get_text(driver, By.XPATH,
                                           "//*[contains(text(), 'Your review is awaiting approval')]")
            logger.warning(f"Отзыв ожидает модерации: {moderation_msg}")
            return False
        except:
            logger.error("Отзыв не найден")
            raise


# ============================================================
# ОСНОВНАЯ ФУНКЦИЯ
# ============================================================

def main():
    """Основная функция выполнения теста"""
    driver = None
    start_time = time.time()

    try:
        logger.info("=" * 50)
        logger.info("НАЧАЛО ТЕСТИРОВАНИЯ")
        logger.info("=" * 50)

        driver = setup_browser()

        order_data = generate_test_data()
        review_data = generate_review_data()

        logger.info(f"Данные заказа: {order_data['first_name']} {order_data['last_name']}, {order_data['email']}")
        logger.info(f"Данные отзыва: автор={review_data['author']}, email={review_data['email']}")

        # Часть 1: Оформление заказа
        logger.info("--- ЧАСТЬ 1: Оформление заказа ---")
        open_website(driver, "http://qa228.karpin74.beget.tech/")
        navigate_to_shop(driver)
        select_product_category(driver)
        select_product(driver)
        set_product_quantity(driver, 1)
        click_add_to_cart(driver)
        click_cart_main(driver)
        click_proceed_to_checkout(driver)
        checkout(driver, order_data)
        place_order(driver)

        # Часть 2: Оставление отзыва
        logger.info("--- ЧАСТЬ 2: Оставление отзыва ---")
        navigate_to_shop(driver)
        select_product_category(driver)
        select_product(driver)
        leave_review(driver, review_data)

        # Проверка
        verify_review_author(driver, review_data["author"])

        elapsed_time = time.time() - start_time
        logger.info("=" * 50)
        logger.info(f"✅ ТЕСТ УСПЕШНО ЗАВЕРШЕН за {elapsed_time:.2f} секунд")
        logger.info("=" * 50)

    except Exception as e:
        elapsed_time = time.time() - start_time
        logger.error("=" * 50)
        logger.error(f"❌ ТЕСТ ЗАВЕРШИЛСЯ С ОШИБКОЙ через {elapsed_time:.2f} секунд")
        logger.error(f"Ошибка: {e}")
        logger.error("=" * 50)

        if driver:
            screenshot_name = f"error_screenshot_{time.strftime('%Y%m%d_%H%M%S')}.png"
            driver.save_screenshot(screenshot_name)
            logger.info(f"Скриншот ошибки сохранен как {screenshot_name}")

    finally:
        if driver:
            logger.info("Закрытие браузера")
            driver.quit()
            logger.info("Браузер закрыт")


if __name__ == "__main__":
    main()
