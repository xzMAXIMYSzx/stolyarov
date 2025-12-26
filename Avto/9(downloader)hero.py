# File Download (File Downloader) Скачать файл
# ----Подключение библиотек---
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Настройка опций для скачивания файлов
chrome_options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": os.path.join(os.getcwd(), "downloads"),
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
chrome_options.add_experimental_option("prefs", prefs)

# Инициализация Webdriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Создаем папку для скачиваний если ее нет
download_dir = os.path.join(os.getcwd(), "downloads")
os.makedirs(download_dir, exist_ok=True)

# Основной блок
try:
    driver.get("https://the-internet.herokuapp.com/download")
    driver.maximize_window()

    # Ждем загрузки страницы
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "a")))

    # 1. Для 20 строки использовать иной метод, например XPATH
    # Оригинальная строка: download = driver.find_element(By.LINK_TEXT, 'tmpvienx1kd.txt').click()

    # Вариант 1: Использование XPATH с текстом ссылки
    # download = driver.find_element(By.XPATH, "//a[text()='tmpvienx1kd.txt']").click()

    # 2. Для 20 строки использовать сложно составной XPATH через родительский элемент: div class="example"
    # 3. Вы скачиваете новый файл, отличный от текущего примера

    # Выбираем другой файл для скачивания (например, первый доступный файл, не tmpvienx1kd.txt)
    # Ищем все ссылки для скачивания
    all_links = driver.find_elements(By.XPATH, "//div[@class='example']//a")

    # Находим файл, отличный от 'tmpvienx1kd.txt'
    target_file = None
    for link in all_links:
        filename = link.text
        if filename != 'tmpvienx1kd.txt' and filename != '':
            target_file = filename
            # Сложный XPATH через родительский элемент div class="example"
            download_link = driver.find_element(
                By.XPATH, f"//div[@class='example']//a[text()='{filename}']"
            )
            print(f"Начинаем скачивание файла: {filename}")
            download_link.click()
            break

    if target_file:
        # Ждем некоторое время для скачивания файла
        time.sleep(5)

        # 4. Добавить print в конце теста используя конструкцию
        print(f"Тест завершен, файл успешно скачен={target_file}")

        # Проверяем, скачался ли файл
        downloaded_file = os.path.join(download_dir, target_file)
        if os.path.exists(downloaded_file):
            print(f"Файл сохранен в: {downloaded_file}")
            file_size = os.path.getsize(downloaded_file)
            print(f"Размер файла: {file_size} байт")
        else:
            print("Файл не найден в папке загрузок")
    else:
        print("Не найден подходящий файл для скачивания")

finally:
    time.sleep(3)
    driver.quit()