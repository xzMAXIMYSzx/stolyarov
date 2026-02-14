import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from faker import Faker
import logging

# Шаг 2.1
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Шаг 2.2
fake = Faker("ru_RU")
logger.info("Генерация рандомных данных настроена!")

# Шаг 2.3
if __name__ == "__main__":
    logger.info("Тест логирования работает!")
    print(f"Случайное имя: {fake.first_name()}")

# Шаг 3.1 (создаем фикстуру)
@pytest.fixture(scope="function")
def driver():
    logger.info("Инициализация браузера")
    chrome_option = webdriver.ChromeOptions()
    chrome_option.add_argument("--start-maximized")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_option)
    # driver.maximize_window() # Уже есть в аргументе --start-maximized

    logger.info("Браузер открыт!")
    yield driver

    logger.info("Закрытие браузера")
    driver.quit()
    logger.info("Браузер закрыт!")

# Шаг 3.2
def test_open_browser(driver):
    driver.get("https://demo1wp.shoporg.ru/")
    logger.info("Сайт открыт")
    # time.sleep(3) # Заменяем на явное ожидание (например, заголовка страницы)
    WebDriverWait(driver, 10).until(EC.title_contains("Магазин"))
    logger.info("Заголовок страницы загружен")

# Блок Закрытие информационного окна
def close_window_before(driver):
    try:
        # Ожидание появления элемента и клик по нему
        close_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".woocommerce-store-notice.demo_store a"))
        )
        close_button.click()
        logger.info("Всплывающее окно успешно закрыто")
    except Exception as e:
        logger.info(f"Всплывающее окно не обнаружено или не закрылось: {e}")

# Шаг 4.1 Функция безопасного клика
def safe_click(driver, by, value, max_attempt=3):
    for attempt in range(max_attempt):
        try:
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((by, value))
            )
            # Прокрутка для надежности
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            element.click()
            logger.info(f"Успешный клик по элементу: {by}={value}")
            return True
        except Exception as e:
            logger.warning(f"Попытка {attempt + 1}/{max_attempt} не удалась: {e}")
    logger.error(f"Не удалось кликнуть по элементу после {max_attempt} попыток")
    raise Exception(f"Элемент {by}={value} не кликабелен")

def test_click_catalog(driver):
    driver.get("https://demo1wp.shoporg.ru/")
    close_window_before(driver) # Добавили закрытие окна для чистоты
    safe_click(driver, By.XPATH, "//button[@class='cat-nav-trigger']")
    logger.info("Каталог открыт!")
    # time.sleep(2) # Заменяем на ожидание появления меню каталога
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//li[@id='menu-item-927']"))
    )
    logger.info("Меню каталога загружено")

# Шаг 5.1 Функция Перехода в категорию женская одежда
def safe_hover(driver, by, value):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((by, value))
        )
        ActionChains(driver).move_to_element(element).perform()
        logger.info(f"Успешное наведение на элемент: {by}={value}")
        return element
    except Exception as e:
        logger.error(f"Ошибка при наведении на элемент: {e}")
        raise Exception(f"Элемент {by}={value} не доступен для наведения")

# Шаг 5.2 Функция навигации
def navigate_to_category(driver):
    logger.info("Начало: Навигация по категориям")

    # Наведение на меню "Одежда"
    logger.info("Наведение на меню 'Одежда'")
    safe_hover(driver, By.XPATH, "//li[@id='menu-item-927']")

    # Ожидаем появления подменю и делаем элемент видимым
    submenu_item = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "menu-item-920"))
    )

    # Клик по "Женская одежда" (исправлено с "Мужская" на "Женская" для консистентности)
    logger.info("Клик по меню 'Женская одежда'")
    safe_click(driver, By.ID, "menu-item-920")  # Убедитесь, что это правильный ID для "Женская одежда"
    logger.info("Успешный переход в категорию 'Женская одежда'")

# Шаг 6.1 Тестируем фильтр
def apply_price_filter(driver):
    logger.info("Начало: Применение фильтра по цене")

    # Ждем появления слайдеров
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'ui-slider-handle')]"))
    )

    sliders = driver.find_elements(By.XPATH, "//span[contains(@class, 'ui-slider-handle')]")
    if len(sliders) >= 2:
        right_slider = sliders[1]
        logger.info(f"Найдено ползунков: {len(sliders)}. Используем правый ползунок (индекс 1)")

        # Ждем, пока ползунок станет интерактивным
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable(right_slider))

        ActionChains(driver).drag_and_drop_by_offset(right_slider, -200, 0).perform()
        logger.info("Правый ползунок успешно перетащен влево")

        # Ждем обновления результатов фильтрации
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//li[contains(@class, 'product')]"))
        )
        logger.info("Результаты фильтрации обновлены")
    else:
        logger.warning(f"Найдено только {len(sliders)} ползунка(ов). Используем первый ползунок")

# Шаг 7.1 Создадим функцию выбора товара
def select_product(driver):
    logger.info("Выбор товара...")

    # Ждем появления продукта и кликаем
    product_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH,
                                    "//h2[contains(text(), 'Черное спортивное платье приталенного кроя')]/parent::a"))
    )
    product_link.click()
    logger.info("Товар выбран")

    # Ждем загрузки страницы товара
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[@name='add-to-cart']"))
    )
    logger.info("Страница товара загружена")

# Шаг 8.1 Создадим функцию очистки/установки поля количества товара
def safe_send_keys(driver, by, value, text):
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((by, value))
    )
    element.clear()
    element.send_keys(text)
    logger.info(f"Введен текст: {text}")

# Шаг 8.2
def set_product_quantity(driver, quantity="1"):
    logger.info(f"Установка количества товара: {quantity}")
    safe_send_keys(driver, By.XPATH, "//input[@name='quantity']", quantity)
    logger.info(f"Количество товара установлено: {quantity}")

# Шаг 9.1 Создаем функцию добавления в корзину
def add_to_cart(driver):
    logger.info("Начало: Добавление товара в корзину")
    safe_click(driver, By.XPATH, "//button[@name='add-to-cart']")
    logger.info("Товар успешно добавлен в корзину")

    # Ждем появления сообщения о добавлении в корзину или перехода к корзине
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'woocommerce-message')]"))
    )
    logger.info("Подтверждение добавления в корзину получено")

# Шаг 10.1 Создаем функцию перехода к оформлению заказа
def proceed_to_checkout(driver):
    logger.info("Переход к оформлению заказа")

    # Ищем ссылку "Оформление заказа" в сообщении
    checkout_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'checkout-button')]"))
    )
    checkout_link.click()
    logger.info("Перешли к оформлению заказа")

    # Ждем загрузки страницы оформления заказа
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "billing_first_name"))
    )
    logger.info("Страница оформления заказа загружена")

# Шаг 10.2 Создаем функцию заполнения формы
def fill_order_form(driver):
    logger.info("Заполнение формы заказа")

    order_data = {
        "billing_first_name": fake.first_name(),
        "billing_last_name": fake.last_name(),
        "billing_address_1": fake.street_address(),
        "billing_city": fake.city(),
        "billing_postcode": fake.postcode(),
        "billing_phone": fake.phone_number(),
        "billing_email": fake.email(),
    }

    for field, value in order_data.items():
        logger.info(f"Заполнение поля '{field}'")
        safe_send_keys(driver, By.XPATH, f"//input[@id='{field}']", value)
        logger.info(f"Поле '{field}' успешно заполнено значением '{value}'")

    logger.info("Форма заказа успешно заполнена")

# Шаг 11.1 Создаем функцию установки чекбокса
def accept_terms_and_conditions(driver):
    logger.info("Начало: Установка чекбокса согласия с условиями")

    try:
        # Сначала пробуем найти по ID
        terms_checkbox = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "terms"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", terms_checkbox)
        terms_checkbox.click()
        logger.info("Чекбокс успешно установлен по ID 'terms'")
        return
    except:
        logger.warning("Чекбокс по ID 'terms' не найден, пробуем другие варианты")

    try:
        # Пробуем через лейбл
        terms_label = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//label[@for='terms']"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", terms_label)
        terms_label.click()
        logger.info("Чекбокс успешно установлен через лейбл")
        return
    except:
        logger.warning("Чекбокс через лейбл не найден")

    try:
        # Последняя попытка - поиск по типу и части имени
        terms_checkbox = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH,
                                        "//input[@type='checkbox' and contains(@id, 'term') or contains(@name, 'term')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", terms_checkbox)
        terms_checkbox.click()
        logger.info("Чекбокс успешно установлен по типу checkbox")
        return
    except Exception as e:
        logger.error(f"Не удалось найти и установить чекбокс согласия: {e}")
        raise Exception("Чекбокс согласия не найден")

# Шаг 12.1 Создаем функцию клик по кнопке place_order
def place_order(driver):
    logger.info("Оформление заказа")

    # Ждем, когда кнопка станет кликабельной
    place_order_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'place_order'))
    )

    # Прокручиваем страницу к кнопке
    logger.info("Прокрутка страницы к кнопке оформления заказа")
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", place_order_button)

    # Даем время на анимацию прокрутки
    WebDriverWait(driver, 2).until(lambda d: True)  # небольшая задержка

    # Кликаем по кнопке
    logger.info("Клик по кнопке 'Оформить заказ'")
    place_order_button.click()

    # Ждем подтверждения заказа
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH,
                                        "//div[contains(@class, 'woocommerce-order')] | //p[contains(text(), 'Спасибо')]"))
    )
    logger.info("Заказ успешно оформлен! Получено подтверждение.")

# Шаг 12.2 Основной поток покупки
def purchase_flow(driver):
    driver.get("https://demo1wp.shoporg.ru/")
    close_window_before(driver)
    test_click_catalog(driver)  # Здесь уже есть ожидания внутри
    navigate_to_category(driver)
    apply_price_filter(driver)
    select_product(driver)
    set_product_quantity(driver)
    add_to_cart(driver)
    proceed_to_checkout(driver)  # Добавили явный переход к оформлению
    fill_order_form(driver)
    accept_terms_and_conditions(driver)
    place_order(driver)
    logger.info("Полный цикл покупки успешно завершен")

# Шаг 13. Декорируем тест для Allure отчета
@allure.feature("Покупка товара")
@allure.story("Полный сценарий покупки товара")
@allure.title("Тест покупки 'Черное спортивное платье приталенного кроя'")
@allure.description("""
1. Открытие сайта и закрытие всплывающих окон
2. Открытие каталога товаров
3. Навигация в категорию 'Женская одежда'
4. Применение фильтра по цене
5. Выбор товара 'Черное спортивное платье приталенного кроя'
6. Изменение количества товара
7. Добавление товара в корзину
8. Переход к оформлению заказа
9. Заполнение формы заказа случайными данными
10. Принятие условий соглашения
11. Оформление заказа
""")
@allure.severity(allure.severity_level.CRITICAL)
def test_full_purchase(driver):
    purchase_flow(driver)
