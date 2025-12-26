# Проверка авторизации
# ----Подключение библиотек---
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Инициализация Webdriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://the-internet.herokuapp.com/login")
driver.maximize_window()

# Основной блок кода
try:
    # 1. Использовать метод: (By.NAME) для строк: 22 и 23
    # Ввод учетных данных
    driver.find_element(By.NAME, "username").send_keys("tomsmith")
    driver.find_element(By.NAME, "password").send_keys("SuperSecretPassword!")

    # 2. Использовать метод: (By.XPATH) для строк: 26
    # 3. Использовать для 22 строки сложный XPath с and, or
    # Раскомментируйте нужный вариант:
    # driver.find_element(By.XPATH, "//input[@id='username' or @name='username']").send_keys("tomsmith") # with or
    # driver.find_element(By.XPATH, "//input[@id='username' and @name='username']").send_keys("tomsmith") # with and
    # driver.find_element(By.XPATH, "//input[@type='text' and @id='username' and @name='username']").send_keys("tomsmith") # сложный with and

    # Клик по кнопке "Login"
    # driver.find_element(By.XPATH, "//button[@class='radius']").click()
    driver.find_element(By.XPATH, "//button[@class='radius' or @type='submit']").click()

    # 4. Использовать WebDriverWait вместо time.sleep()
    # Ожидание появления элемента с приветствием
    wait = WebDriverWait(driver, 10)
    welcome_element = wait.until(
        EC.presence_of_element_located((By.XPATH, "//h4[@class='subheader']"))
    )

    welcome = welcome_element.text
    assert "Welcome to the Secure Area. When you are done click logout below." in welcome, "Текст приветствия не найден"
    print(f"Проверка пройдена, искомый текст проверки найден = {welcome}")

    # 5. Дописать код клик по кнопке 'Logout'
    # Клик по кнопке Logout
    logout_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[@class='button secondary radius']"))
    )
    logout_button.click()

    # Проверка, что мы вернулись на страницу логина
    login_button = wait.until(
        EC.presence_of_element_located((By.XPATH, "//button[@type='submit']"))
    )
    print("Успешно разлогинились, вернулись на страницу логина")

finally:
    time.sleep(2)
    driver.quit()