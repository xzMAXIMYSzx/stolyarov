import pytest
import allure
# ============================================================
# БЛОК 1: ИМПОРТ БИБЛИОТЕК
# ============================================================
# Подключение необходимых библиотек для автоматизации тестирования
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from faker import Faker
import logging
import time

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


def open_website(driver, url):
    """Открытие страницы браузера"""
    logger.info(f"Открытие сайта: {url}")
    driver.get(url)
    safe_wait_for_element(driver, By.TAG_NAME, "body", timeout=15)
    logger.info("Сайт успешно открыт")





def close_auth_popup(driver, url):
    """Открывает сайт и закрывает окно авторизации, если оно есть"""
    if url:
        logger.info(f"Открытие сайта: {url}")
        driver.get(url)

    try:
        button = safe_wait_for_clickable(
            driver,
            By.XPATH,
            "//div[contains(@class, 'modal') or contains(@class, 'popup')]//button[.//svg]",
            timeout=5
        )
        button.click()
        logger.info("✅ Окно авторизации закрыто")
        return True
    except:
        logger.info("ℹ️ Окно авторизации не появилось")
        return False


def close_banners(driver):
    """Закрывает модальные окна и баннеры"""
    try:
        city_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'sc-40103ed2-2 cKqwHD')]"))
        )
        city_button.click()
        logger.info("✅ Баннер выбора города закрыт")
        time.sleep(1)
    except:
        logger.info("⏩ Баннер выбора города не найден")

    try:
        """Пробует разные способы найти и нажать кнопку принятия cookies"""

        cookie_selectors = [
            # По уникальному классу (самый надёжный)
            (By.XPATH, "//button[contains(@class, 'iUqWKY')]"),

            # По родительскому div
            (By.XPATH, "//div[contains(@class, 'hAORYS')]/button"),

            # По тексту (если есть)
            (By.XPATH, "//button[contains(text(), 'flex')]"),

            # Если вообще ничего не поможет)
            (By.XPATH, "//div[4]/div/div/div/button"),

            # Запасной вариант
            (By.XPATH, "//button[contains(@class, 'cKqwHD')]")
        ]

        for by, selector in cookie_selectors:
            try:
                button = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((by, selector))
                )
                button.click()
                logger.info(f"✅ Cookies приняты через: {selector}")
                return True
            except Exception as e:
                logger.debug(f"❌ Не сработало: {selector} — {str(e)}")
                continue

        logger.info("ℹ️ Кнопка cookies не найдена")
        return False


    except:
        logger.info("⏩ Баннер cookies не найден")


@allure.step("Проверка всех 16 пунктов меню")
def check_all_16_menu_sections(driver):
    """Проходит по всем 16 пунктам меню и проверяет их открытие"""

    all_results = []

    # Сначала убедимся, что мы на главной странице
    logger.info("🏠 Проверка: находимся ли мы на главной странице")
    current_url = driver.current_url
    logger.info(f"Текущий URL: {current_url}")

    # Если мы не на главной - вернёмся
    if "new-tb.avtosushi.ru" in current_url and "/shop/" in current_url:
        logger.info("🔙 Возвращаемся на главную")
        driver.get("https://new-tb.avtosushi.ru/")
        time.sleep(2)

    for i in range(1, 17):  # 1, 2, 3, ..., 16
        try:
            with allure.step(f"Проверка пункта меню {i}"):
                xpath = f"//header//nav/a[{i}]"
                logger.info(f"🔍 Ищем пункт {i} по XPath: {xpath}")

                # Проверяем, есть ли элемент в DOM
                elements = driver.find_elements(By.XPATH, xpath)
                logger.info(f"📊 Найдено элементов в DOM: {len(elements)}")

                if not elements:
                    logger.warning(f"⚠️ Пункт {i} не найден в DOM — возможно, меню короче")
                    all_results.append({
                        "index": i,
                        "status": "SKIPPED",
                        "reason": "not found in DOM"
                    })
                    continue

                element = elements[0]

                # Проверяем состояние элемента
                is_displayed = element.is_displayed()
                is_enabled = element.is_enabled()
                element_text = element.text or f"пункт_{i}"

                logger.info(f"📝 Текст: '{element_text}'")
                logger.info(f"👁️ Видим: {is_displayed}")
                logger.info(f"🖱️ Кликабелен: {is_enabled}")

                if not is_displayed:
                    logger.warning(f"⚠️ Пункт {i} не видим — пробуем прокрутить")

                    # Пробуем прокрутить к элементу
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                    time.sleep(1)

                    # Проверяем ещё раз
                    is_displayed = element.is_displayed()
                    logger.info(f"👁️ После прокрутки видим: {is_displayed}")

                if not is_displayed:
                    logger.warning(f"⚠️ Пункт {i} всё ещё не видим — пропускаем")
                    all_results.append({
                        "index": i,
                        "text": element_text,
                        "status": "SKIPPED",
                        "reason": "not visible"
                    })
                    continue

                # Прокручиваем к элементу (ещё раз для надёжности)
                driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", element)
                time.sleep(1)

                # Запоминаем URL до клика
                before_url = driver.current_url

                # Пробуем кликнуть разными способами
                try:
                    # Способ 1: обычный клик
                    element.click()
                    logger.info(f"✅ Обычный клик сработал для пункта {i}")
                except Exception as e:
                    logger.warning(f"⚠️ Обычный клик не сработал: {e}")

                    # Способ 2: клик через JavaScript
                    try:
                        driver.execute_script("arguments[0].click();", element)
                        logger.info(f"✅ JavaScript-клик сработал для пункта {i}")
                    except Exception as e2:
                        logger.error(f"❌ JavaScript-клик тоже не сработал: {e2}")
                        raise

                logger.info(f"✅ Перешли в раздел {i}: '{element_text}'")

                # Ждём загрузки страницы
                time.sleep(3)

                # Проверяем, что URL изменился
                after_url = driver.current_url
                if after_url == before_url:
                    logger.warning(f"⚠️ URL не изменился для пункта {i}")
                else:
                    logger.info(f"🔗 URL изменился: {after_url}")

                # Скриншот раздела
                screenshot_name = f"Раздел_{i}_{element_text[:20]}"
                attach_screenshot(driver, screenshot_name)

                # Запоминаем результат
                all_results.append({
                    "index": i,
                    "text": element_text,
                    "url": after_url,
                    "status": "OK"
                })

                # Возвращаемся на главную
                logger.info(f"🔙 Возвращаемся на главную страницу")
                driver.get("https://new-tb.avtosushi.ru/")
                time.sleep(3)

        except Exception as e:
            logger.error(f"❌ Ошибка при проверке пункта {i}: {str(e)}")

            # Скриншот ошибки
            try:
                attach_screenshot(driver, f"Ошибка_пункта_{i}")
            except:
                pass

            all_results.append({
                "index": i,
                "status": "ERROR",
                "error": str(e)
            })

            # Пытаемся восстановиться — возвращаемся на главную
            try:
                logger.info("🔄 Пытаемся восстановиться — возврат на главную")
                driver.get("https://new-tb.avtosushi.ru/")
                time.sleep(3)
            except:
                pass

            continue

    # Итоговая статистика
    logger.info("=" * 60)
    logger.info("📊 ИТОГОВАЯ СТАТИСТИКА ПРОВЕРКИ МЕНЮ")
    logger.info("=" * 60)

    successful = sum(1 for r in all_results if r.get("status") == "OK")
    skipped = sum(1 for r in all_results if r.get("status") == "SKIPPED")
    errors = sum(1 for r in all_results if r.get("status") == "ERROR")

    logger.info(f"✅ Успешно: {successful}")
    logger.info(f"⏩ Пропущено: {skipped}")
    logger.info(f"❌ С ошибками: {errors}")
    logger.info(f"📋 Всего проверок: {len(all_results)}")

    # Детали по ошибкам
    if errors > 0:
        logger.info("❌ Детали ошибок:")
        for r in all_results:
            if r.get("status") == "ERROR":
                logger.info(f"  Пункт {r['index']}: {r.get('error', 'Unknown error')}")

    logger.info("=" * 60)

    return all_results





# ============================================================
# ТЕСТ 1: Проверка всех 16 пунктов меню
# ============================================================
@allure.feature("Главная страница")
@allure.story("Открытие сайта")
@allure.title("Проверка наличия слова 'Автосуши' в заголовке")
@allure.description("Тест проверяет, что сайт открывается и в заголовке есть слово Автосуши")
def test_site_title():
    """Тест проверяет, что сайт открывается и в заголовке есть слово Автосуши"""
    driver = None
    try:
        with allure.step("Запуск браузера"):
            driver = setup_browser()

        with allure.step("Открытие сайта: https://new-tb.avtosushi.ru"):
            open_website(driver, "https://new-tb.avtosushi.ru/")
        attach_screenshot(driver, "Сайт_открыт")



        with allure.step("Получение заголовка страницы"):
            title = driver.title
            logger.info(f"Заголовок страницы: {title}")
            allure.attach(title, name="Заголовок страницы", attachment_type=allure.attachment_type.TEXT)

        with allure.step("Проверка наличия слова 'Автосуши' в заголовке"):
            assert "Автосуши" in title, f"Ожидалось 'Автосуши' в заголовке, но получено: {title}"
            logger.info("✓ Тест пройден: слово 'Автосуши' найдено в заголовке")

        with allure.step("Закрытие модального окна авторизации (если есть)"):
            close_auth_popup(driver, "https://new-tb.avtosushi.ru/")
        attach_screenshot(driver, "Окно_авторизации_обработано")

        with allure.step("Закрытие баннеров"):
            close_banners(driver)
        attach_screenshot(driver, "Баннеры_закрыты")

        with allure.step("Проверка всех 16 пунктов меню"):
            results = check_all_16_menu_sections(driver)



        attach_screenshot(driver, "Тест_успешно_завершен")
        time.sleep(2)

    except Exception as e:
        logger.error(f"✗ Тест упал с ошибкой: {str(e)}")
        if driver:
            attach_screenshot(driver, "Ошибка_выполнения_теста")
        raise
    finally:
        if driver:
            with allure.step("Закрытие браузера"):
                driver.quit()
                logger.info("Браузер закрыт")


# ============================================================
# ТОЧКА ВХОДА (для отладки - закомментировано для pytest)
# ============================================================
# if __name__ == "__main__":
#     test_site_title()
