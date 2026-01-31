# Блок1 Импорт библиотек
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from faker import Faker
import time
import logging

# Блок2 Инициализация Faker
fake = Faker("ru_RU")

# Блок3 Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Блок4 Вспомогательные функции
def init_driver():
    """Инициализация драйвера"""
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get("https://demo1wp.shoporg.ru/")
        driver.maximize_window()
        time.sleep(3)
        logger.info("Драйвер инициализирован, сайт загружен")
        return driver, WebDriverWait(driver, 10)
    except Exception as e:
        logger.error(f"Ошибка инициализации драйвера: {e}")
        raise


def nuke_notice(driver):
    """Полное уничтожение уведомления через JS"""
    driver.execute_script("""
        // 1. Удаляем ВСЕ возможные уведомления
        var notices = document.querySelectorAll('.woocommerce-store-notice, [data-notice-id]');
        notices.forEach(el => el.remove());

        // 2. Удаляем все кнопки закрытия
        var closeBtns = document.querySelectorAll('a.woocommerce-store-notice__dismiss-link, a[href="#"]');
        closeBtns.forEach(el => el.remove());

        // 3. Скрываем через CSS (на всякий случай)
        var allElements = document.querySelectorAll('body > *');
        allElements.forEach(el => {
            var text = el.textContent || el.innerText;
            if (text.includes('демонстрационный') || text.includes('тестирования')) {
                el.style.display = 'none';
                el.remove();
            }
        });

        // 4. Удаляем родительский контейнер, если есть
        var container = document.querySelector('body > p');
        if (container && container.textContent.includes('демонстрационный')) {
            container.remove();
        }

        console.log('Уведомление уничтожено');
    """)
    print("✅ Баннер принудительно удалён")


def close_demo_notice(driver):
    """Закрытие демо-уведомления"""
    try:
        notice = driver.find_element(By.XPATH, "/html/body/p[1]")
        close_btn = driver.execute_script("""
            return arguments[0].nextElementSibling;
        """, notice)

        if close_btn and close_btn.tag_name == 'a':
            driver.execute_script("arguments[0].click();", close_btn)
            logger.info("Демо-уведомление закрыто")
            return True
    except:
        logger.info("Демо-уведомление не найдено")
        return False


def safe_click(driver, wait, by, selector):
    """Безопасный клик по элементу"""
    try:
        element = wait.until(EC.element_to_be_clickable((by, selector)))
        element.click()
        return element
    except Exception as e:
        logger.error(f"Ошибка клика на элемент {selector}: {e}")
        raise


def safe_send_keys(driver, wait, by, selector, text):
    """Безопасный ввод текста"""
    try:
        element = wait.until(EC.presence_of_element_located((by, selector)))
        element.clear()
        element.send_keys(text)
        return element
    except Exception as e:
        logger.error(f"Ошибка ввода в элемент {selector}: {e}")
        raise


def safe_hover(driver, wait, by, selector):
    """Безопасное наведение курсора"""
    try:
        element = wait.until(EC.visibility_of_element_located((by, selector)))
        ActionChains(driver).move_to_element(element).perform()
        return element
    except Exception as e:
        logger.error(f"Ошибка наведения на элемент {selector}: {e}")
        raise


def generate_order_data():
    """Генерация случайных данных для заказа"""
    return {
        "billing_first_name": fake.first_name(),
        "billing_last_name": fake.last_name(),
        "billing_city": fake.city(),
        "billing_address_1": fake.street_address(),
        "billing_postcode": fake.postcode(),
        "billing_phone": fake.phone_number(),
        "billing_email": fake.email()
    }


# Блок5 Основные шаги теста
def step_open_catalog(driver, wait):
    """Шаг 1: Открытие каталога"""
    safe_click(driver, wait, By.XPATH, "//button[@class='cat-nav-trigger']")


def step_hover_clothing_menu(driver, wait):
    """Шаг 2: Наведение на меню 'Одежда'"""
    safe_hover(driver, wait, By.XPATH, "//li[@id='menu-item-927']")


def step_click_men_clothing(driver, wait):
    """Шаг 3: Клик по 'Мужская одежда'"""
    safe_click(driver, wait, By.XPATH, "//li[@id='menu-item-924']")


def step_adjust_price_filter(driver, wait):
    """Шаг 4: Настройка фильтра по цене"""
    slider = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//span[@class='ui-slider-handle ui-corner-all ui-state-default']")))
    ActionChains(driver).drag_and_drop_by_offset(slider, 30, 0).perform()


def step_select_grey_suit(driver, wait):
    """Шаг 5: Выбор товара"""
    safe_click(driver, wait, By.XPATH, "//*//h2[text()='Мужской серый костюм в свободном стиле']")


def step_set_quantity(driver, wait, quantity="1"):
    """Шаг 6: Установка количества товара"""
    safe_send_keys(driver, wait, By.XPATH, "//input[@name='quantity']", quantity)


def step_add_to_cart(driver, wait):
    """Шаг 7: Добавление в корзину"""
    safe_click(driver, wait, By.XPATH, "//button[@name='add-to-cart']")


def step_go_to_checkout(driver):
    """Переход к оформлению заказа"""
    try:
        checkout_btn = driver.find_element(
            By.XPATH, "//a[contains(text(), 'Оформление заказа') or contains(@class, 'checkout')]")
        checkout_btn.click()
    except:
        driver.get("https://demo1wp.shoporg.ru/checkout/")
    time.sleep(2)


def step_fill_order_form(driver, wait, order_data):
    """Шаг 8-9: Заполнение формы заказа"""
    for field, value in order_data.items():
        safe_send_keys(driver, wait, By.XPATH, f"//input[@id='{field}']", value)


def step_check_terms(driver, wait):
    """Шаг 10: Активация чекбокса terms"""
    try:
        term = wait.until(EC.element_to_be_clickable((By.ID, "terms")))
    except:
        term = driver.find_element(By.XPATH, "//input[@name='terms']")
    driver.execute_script("arguments[0].click();", term)


def step_place_order(driver, wait):
    """Шаг 11: Оформление заказа"""
    safe_click(driver, wait, By.ID, "place_order")

    time.sleep(3)
    try:
        driver.find_element(By.XPATH, "//h2[contains(text(), 'Заказ получен')]")
        return True
    except:
        return False


# Блок6 Основная функция
def main():
    """Основной поток выполнения теста"""
    driver = None
    try:
        logger.info("=" * 50)
        logger.info("НАЧАЛО ТЕСТА: Покупка мужского серого костюма")
        logger.info("=" * 50)

        driver, wait = init_driver()
        close_demo_notice(driver)

        order_data = generate_order_data()
        logger.info(f"Сгенерированы данные для заказа")
        nuke_notice(driver)
        step_open_catalog(driver, wait)
        step_hover_clothing_menu(driver, wait)
        step_click_men_clothing(driver, wait)
        step_adjust_price_filter(driver, wait)
        step_select_grey_suit(driver, wait)
        step_set_quantity(driver, wait, "1")
        step_add_to_cart(driver, wait)
        step_go_to_checkout(driver)
        step_fill_order_form(driver, wait, order_data)
        step_check_terms(driver, wait)

        success = step_place_order(driver, wait)

        if success:
            logger.info("ТЕСТ УСПЕШНО ЗАВЕРШЕН!")
        else:
            logger.warning("ТЕСТ ЗАВЕРШЕН С ПРЕДУПРЕЖДЕНИЯМИ")

    except Exception as e:
        logger.error(f"ОШИБКА ВО ВРЕМЯ ТЕСТА: {e}")
        if driver:
            try:
                driver.save_screenshot("test_error.png")
                logger.info("Скриншот ошибки сохранен")
            except:
                pass
        raise
    finally:
        if driver:
            time.sleep(5)
            driver.quit()
            logger.info("Драйвер закрыт")


# Блок7 Запуск
if __name__ == "__main__":
    main()
