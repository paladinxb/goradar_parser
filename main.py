import json
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import os

# 1. smart faith 2. NENG YUAN 3. ZHE HAI 507
imo_numbers = ["9506344 ", "9185762", "9416513"]  # Добавь нужные IMO сюда

def get_vessel_info(imo):
    url = f"https://goradar.ru/vessels_map.php?imo={imo}"

    options = Options()
    options.add_argument("--headless")  # Запуск без GUI
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    service = Service('D:/chromedriver-win64/chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)
    time.sleep(3)  # Даем странице загрузиться

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

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

def save_to_json(data, filename="vessel_data.json"):
    """Перезаписывает JSON-файл с новыми данными."""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Данные успешно сохранены в {filename}")
    except Exception as e:
        print(f"Ошибка при сохранении JSON: {e}")

# Основной процесс
vessels_data = []
for imo in imo_numbers:
    vessel_data = get_vessel_info(imo)
    vessels_data.append(vessel_data)

# Сохранение всех данных в JSON-файл
save_to_json(vessels_data)
