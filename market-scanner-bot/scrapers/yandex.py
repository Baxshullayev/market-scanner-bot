import requests
from bs4 import BeautifulSoup
import re

def clean_price(price_text: str) -> str:
    return re.sub(r"[^\d\s]", "", price_text).strip()

def search_yandex(product_name: str) -> dict:
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    url = f"https://market.yandex.ru/search?text={product_name.replace(' ', '+')}"
    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code != 200:
        return {"error": "Yandex Market dan javob olinmadi"}

    soup = BeautifulSoup(response.text, "html.parser")
    products = soup.select("article[data-autotest-id='product-snippet']")

    if not products:
        return {"error": "Mahsulot topilmadi"}

    try:
        first = products[0]
        title = first.select_one("h3 span").get_text(strip=True)
        price = first.select_one("span._1ArMm").get_text(strip=True)
        link = "https://market.yandex.ru" + first.select_one("a")["href"]

        return {
            "title": title,
            "price": clean_price(price) + " so‘m",
            "link": link
        }
    except Exception as e:
        return {"error": f"Parslashda xatolik: {e}"}
