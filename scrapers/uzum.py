import requests
from bs4 import BeautifulSoup
import re

def clean_price(price_text: str) -> str:
    return re.sub(r"[^\d\s]", "", price_text).strip()

def search_uzum(product_name: str) -> dict:
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    url = f"https://uzum.uz/uz/search?query={product_name.replace(' ', '%20')}"
    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code != 200:
        return {"error": "Uzum.uz dan javob olinmadi"}

    soup = BeautifulSoup(response.text, "html.parser")
    products = soup.select("div.product-card")

    if not products:
        return {"error": "Mahsulot topilmadi"}

    try:
        first = products[0]
        title = first.select_one(".product-card__title").get_text(strip=True)
        price = first.select_one(".product-card__price").get_text(strip=True)
        link = "https://uzum.uz" + first.select_one("a")["href"]

        return {
            "title": title,
            "price": clean_price(price) + " so‘m",
            "link": link
        }
    except Exception as e:
        return {"error": f"Parslashda xatolik: {e}"}