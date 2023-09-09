import requests
import os 
import csv
import json
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()

login = os.getenv("LOGIN")
password = os.getenv("PASSWORD")

# ф-я сбора данных 
def collect_data():
    proxies = {
        "https" : f"http://{login}:{password}@85.195.81.154:11655"
    }

    # текущая дата  в формате день, месяц, год для того чтобы скрипт не перезаписывал, если был запущен в разные дни
    t_date = datetime.now().strftime("%d_%m_%Y")

    # отправляем запрос с прокси 
    response = requests.get(
        url = "https://www.lifetime.plus/api/analysis2", 
        proxies = proxies
    ) 
    print(response)
    
    # сохраняем ответ в json - файл 
    with open(f"info_{t_date}.json", "w", encoding="utf-8") as file:
        json.dump(
            response.json(), # полученные данные
            file, # файл
            indent = 4, # формат отступа
            ensure_ascii = False
        )

    # забираем все категории 
    categories = response.json()["categories"]

    result = [] # массив, в который будут записываться все данные 

    for cat in categories:
        # название категории
        cat_name = cat.get("name").strip() # .strip() - обрезание пробелов слева и справа 
        # получаем все тесты в категории
        cat_items = cat.get("items")

        for item in cat_items: # смотрим тесты в каждой категории
            item_name = item.get("name").strip()
            item_price = item.get("price")
            item_desc = item.get("description").strip()

            if "β" in item_desc:
                item_desc = item_desc.replace("β", "B")

            if "" in item_desc:
                item_desc = item_desc.replace("γ", "Y")

            item_wt = item.get("days")
            item_bio = item.get("biomaterial")

            result.append( # записываем результат по каждому тесту
                [
                    cat_name, 
                    cat_items,
                    item_bio,
                    item_desc,
                    item_price,
                    item_wt
                ]
            )

    # записываем результат в csv файл
    with open(f"result_{t_date}.csv", "a", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow( # записываем название колонок 
            (
                "Категория",
                "Анализ",
                "Биоматериал",
                "Описание",
                "Стоимость",
                "Готовность в течении дня",
            )
        )

        writer.writerows(
            result
        )
                


def main():
    collect_data()


if __name__ == "__main__":
    main()