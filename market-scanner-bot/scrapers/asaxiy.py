import requests
from bs4 import BeautifulSoup
import re

def clean_price(price_text: str) -> str:
    """Narxni matndan tozalash (raqam va bo‘shliq qoldirib)"""
    return re.sub(r"[^\d\s]", "", price_text).strip()

def search_asaxiy(product_name: str) -> dict:
    """Asaxiy.uz saytida mahsulotni qidirish va birinchi natijani qaytarish"""

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    # Qidiruv URL
    url = f"https://asaxiy.uz/product?key={product_name.replace(' ', '+')}"
    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code != 200:
        return {"error": "Saytdan javob olinmadi"}

    soup = BeautifulSoup(response.text, "html.parser")

    # Mahsulot kartalari
    products = soup.select("div.product__item")

    if not products:
        return {"error": "Mahsulot topilmadi"}

    first = products[0]

    try:
        title = first.select_one(".product__item__info-title").get_text(strip=True)
        price = first.select_one(".product__item-price").get_text(strip=True)
        link = "https://asaxiy.uz" + first.select_one("a")["href"]

        return {
            "title": title,
            "price": clean_price(price) + " so‘m",
            "link": link
        }

    except Exception as e:
        return {"error": f"Parslashda xatolik: {e}"}
