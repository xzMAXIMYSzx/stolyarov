import pytest
import allure
# ============================================================
# БЛОК 1: ИМПОРТ БИБЛИОТЕК
# ============================================================
# Подключение необходимых библиотек для автоматизации тестирования
from selenium import webdriver  # Основной модуль Selenium для управления браузером
from selenium.webdriver.common.by import By  # Стратегии поиска элементов (XPath, CSS, ID и т.д.)
from selenium.webdriver.chrome.service import Service  # Управление сервисом драйвера Chrome
from selenium.webdriver.support.ui import WebDriverWait  # Явные ожидания элементов
from selenium.webdriver.support import expected_conditions as EC  # Условия ожидания
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import \
    ActionChains  # Выполнение сложных действий (наведение, перетаскивание)
from webdriver_manager.chrome import ChromeDriverManager  # Автоматическая установка драйвера Chrome
from faker import Faker  # Генерация случайных тестовых данных
import logging  # Модуль для логирования событий теста
import time  # Модуль для добавления пауз между действиями
import traceback

# ============================================================
# БЛОК 2: НАСТРОЙКА ЛОГИРОВАНИЯ + Faker
# ============================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
fake = Faker("ru_RU")


# ============================================================
# БЛОК 3: НАСТРОЙКА ALLURE
# ============================================================
def attach_screenshot(driver, step_name):
    """Прикрепляет скриншот к отчету Allure с таймстампом"""
    try:
        screenshot = driver.get_screenshot_as_png()
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        allure.attach(
            screenshot, 
            name=f"{step_name} ({timestamp})", 
            attachment_type=allure.attachment_type.PNG
        )
        logger.info(f"✅ Скриншот '{step_name}' прикреплен к отчету Allure")
        return True
    except Exception as e:
        logger.warning(f"⚠️ Не удалось прикрепить скриншот '{step_name}': {e}")
        return False


def setup_browser():
    """Инициализация вебдрайвера"""
    logger.info("Запуск браузера Chrome")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    logger.info("Браузер успешно запущен и развернут на весь экран")
    return driver


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


def open_website(driver, url):
    """Открытие страницы браузера"""
    logger.info(f"Открытие сайта: {url}")
    driver.get(url)
    safe_wait_for_element(driver, By.TAG_NAME, "body", timeout=15)
    logger.info("Сайт успешно открыт")


# ============================================================
# ТЕСТ 1: Проверка заголовка сайта
# ============================================================
@allure.feature("Главная страница")
@allure.story("Открытие сайта")
@allure.title("Проверка наличия слова 'Автосуши' в заголовке")
@allure.description("Тест проверяет, что сайт открывается и в заголовке есть слово Автосуши")
def test_site_title():
    """Тест проверяет, что сайт открывается и в заголовке есть слово Автосуши"""
    
    driver = None
    try:
        # Шаг 1: Запуск браузера
        with allure.step("Запуск браузера"):
            driver = setup_browser()
        
        # Шаг 2: Открытие сайта
        with allure.step("Открытие сайта: https://new-tb.avtosushi.ru"):
            open_website(driver, "https://new-tb.avtosushi.ru/")
        
        # Шаг 3: Скриншот после загрузки
        attach_screenshot(driver, "Сайт загружен")
        
        # Шаг 4: Получаем заголовок страницы
        with allure.step("Получение заголовка страницы"):
            title = driver.title
            logger.info(f"Заголовок страницы: {title}")
            allure.attach(
                title,
                name="Заголовок страницы",
                attachment_type=allure.attachment_type.TEXT
            )
        
        # Шаг 5: Проверяем заголовок
        with allure.step("Проверка наличия слова 'Автосуши' в заголовке"):
            assert "Автосуши" in title, f"Ожидалось 'Автосуши' в заголовке, но получено: {title}"
            logger.info("✓ Тест пройден: слово 'Автосуши' найдено в заголовке")
        
        # Шаг 6: Финальный скриншот
        attach_screenshot(driver, "Тест успешно завершен")
        
        # Шаг 7: Небольшая пауза
        time.sleep(2)
        
    except Exception as e:
        logger.error(f"✗ Тест упал с ошибкой: {str(e)}")
        # Скриншот при ошибке
        if driver:
            attach_screenshot(driver, "Ошибка выполнения теста")
        raise
    finally:
        # Шаг 8: Закрытие браузера
        if driver:
            with allure.step("Закрытие браузера"):
                driver.quit()
                logger.info("Браузер закрыт")


# ============================================================
# ТОЧКА ВХОДА (для отладки - закомментировано для pytest)
# ============================================================
# if __name__ == "__main__":
#     test_site_title()
