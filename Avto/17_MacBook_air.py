# ООП стиль
# Сценарий: Авторизация и оформление покупки при помощи рандомизатора Faker
# Подключение библиотек
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker
import logging
import time

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

#Инициализация Faker
fake = Faker()

def generate_credentials():
    "Генерация тестовых данных"
    username = fake.user_name()[:10]
    password = fake.password(length=12, special_chars=True, digits=True)  # Генерация пароля
    logger.info(f"Сгенерированы: UserName={username}, Password={password}")
    return username, password

def int_driver():
    "Инициализация WebDriver"
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        driver.maximize_window()
        logger.info("WebDriver успешно инициализирован")
        return driver
    except Exception as e:
        logger.error(f"Ошибка при инициализации WebDriver: {str(e)}")
        raise

def safe_click(driver, by, value, max_attempt=3):
    "Безопасный клик"
    for attempt in range(max_attempt):
        try:
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((by, value)))
            element.click()
            logger.info(f"Успешный клик по элементу: {by}={value}")
            return True
        except Exception as e: # Проверить целесообразность использования str в отношении e
            logger.warning(f"Попытка {attempt + 1}/{max_attempt} не удалось: {str(e)}")
            time.sleep(1)
    logger.error(f"Не удалось кликнуть по элементу после: {max_attempt} попыток")
    raise Exception(f"Элемент {by}={value} не кликабелен")

def safe_send_keys(driver, by, value, text):
    "Безопасный ввод текста"
    try:
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((by, value)))
        element.clear()
        element.send_keys(text)
        logger.info(f"Успешно введен текст в элемент: {by}={value}")
    except Exception as e:
        logger.error(f"Ошибка при вводе текста: {e}")
        raise Exception(f"Элемент {by}={value} не доступен для ввода")

def handle_alert(driver, timeout=5):
    "Обработка алертов"
    try:
        WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert_text = alert.text
        alert.accept()
        logger.info(f"Обработан алерт с текстом: {alert_text}")
        return alert_text
    except Exception as e:
        logger.warning(f"Алерт не появился: {str(e)}")
        return None
def register_user(driver, username, password):
    "Процесс регистрации"
    logger.info("Начало процесса регистрации")
    safe_click(driver, By.ID, "signin2")
    safe_send_keys(driver, By.ID, "sign-username", username)
    safe_send_keys(driver, By.ID, "sign-password", password)
    safe_click(driver, By.XPATH, "//button[text()='Sign up']")
    handle_alert(driver)
    logger.info("Регистрация прошла успешно")

def login_user(driver, username, password):
    "Процесс авторизации"
    logger.info("Начало процесса авторизации")
    #time.sleep(1)
    safe_click(driver, By.ID, "login2")
    safe_send_keys(driver, By.ID, "loginusername", username)
    safe_send_keys(driver, By.ID, "loginpassword", password)
    safe_click(driver, By.XPATH, "//button[text()='Log in']")
    handle_alert(driver)
    logger.info("Авторизация прошла успешно")

def purchase_flow(driver):
    "Процесс оформления покупки"
    logger.info("Начало процесса покупки")

    # Выбор товара
    safe_click(driver, By.PARTIAL_LINK_TEXT, "Laptops")

    safe_click(driver, By.PARTIAL_LINK_TEXT, "MacBook air")

    safe_click(driver, By.XPATH, "//a[@onclick='addToCart(11)']")

    handle_alert(driver)

    #Оформление заказа(клик по корзине)
    safe_click(driver, By.ID, "cartur")
    safe_click(driver, By.XPATH, "//button[text()='Place Order']")

    #Заполнение формы
    safe_send_keys(driver, By.ID, "name", fake.first_name())
    safe_send_keys(driver, By.ID, "country", fake.country())
    safe_send_keys(driver, By.ID, "city", fake.city())
    safe_send_keys(driver, By.ID, "card", fake.credit_card_number())
    month = str(fake.random_int(min=1, max=12)).zfill(2)
    safe_send_keys(driver, By.ID, "month", month)
    safe_send_keys(driver, By.ID, "year", str(fake.random_int(min=24, max=34)))

    #Завершение покупки(клик по кнопке purchase)
    safe_click(driver, By.XPATH, "//button[text()='Purchase']")

    #Проверка
    confirmation = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "sweet-alert"))).text
    assert "Thank you for your purchase!" in confirmation
    logger.info("Покупка успешно завершена")

    safe_click(driver, By.XPATH, "//button[@class='confirm btn btn-lg btn-primary']")
def main():
    try:
        #Инициализация
        driver = int_driver()
        username, password = generate_credentials()

        #Основной поток
        driver.get("https://demoblaze.com")
        register_user(driver, username, password)
        login_user(driver, username, password)
        purchase_flow(driver)

        logger.info("Тест успешно завершен!")

    except Exception as e:
        logger.error(f"Тест завершился с ошибкой: {str(e)}, exc_info=True")
    finally:
        if 'driver' in locals():
            #time.sleep(5)
            driver.quit()
            logger.info("Браузер закрыт")

if __name__ == "__main__":
    main()
