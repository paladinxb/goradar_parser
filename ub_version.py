import json
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# 1. smart faith 2. NENG YUAN 3. ZHE HAI 507
imo_numbers = ["9506344 ", "9185762", "9416513"]  # Добавь нужные IMO сюда

def get_vessel_info(imo):
    url = f"https://goradar.ru/vessels_map.php?imo={imo}"

    # Настройки для Chrome на Linux (сервер без GUI)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Без графики
    chrome_options.add_argument("--no-sandbox")  # Важно для сервера!
    chrome_options.add_argument("--disable-dev-shm-usage")  # Избегаем проблем с памятью
    chrome_options.binary_location = "/usr/bin/google-chrome"  # Путь к Chrome

    # Указываем путь к chromedriver (если он в PATH, можно не указывать)
    service = Service(executable_path="/usr/local/bin/chromedriver")

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    time.sleep(3)  # Ожидание загрузки

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    # Дальше парсинг как в твоём коде...
    coordinates_div = soup.find("div", id="vesCoordinates")

    if not coordinates_div:
        return {"imo": imo, "error": "Не удалось извлечь данные о судне."}

    coordinates_text = coordinates_div.get_text("\n", strip=True)
    match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\n\(.*?\)\n, ([\d.]+), ([\d.]+), курс: (\d+), скорость: (\d+)', coordinates_text)
    
    if match:
        return {
            "imo": imo,
            "time": match.group(1),
            "latitude": float(match.group(2)),
            "longitude": float(match.group(3)),
            "course": int(match.group(4)),
            "speed": float(match.group(5))
        }
    else:
        return {"imo": imo, "error": "Не удалось распарсить данные."}

# Сохранение данных в JSON (как у тебя)
vessels_data = [get_vessel_info(imo) for imo in imo_numbers]
with open("vessel_data.json", "w") as f:
    json.dump(vessels_data, f, indent=4, ensure_ascii=False)