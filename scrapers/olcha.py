import requests
from bs4 import BeautifulSoup
import re

def clean_price(price_text: str) -> str:
    """Narx matnini tozalaydi, faqat raqamlar va bo‘shliq qoldiradi."""
    return re.sub(r"[^\d\s]", "", price_text).strip()

def search_olcha(product_name: str) -> dict:
    """Olcha.uz saytida mahsulotni izlab, birinchi topilgan natijani qaytaradi."""

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    # Qidiruv URL (Olcha’da `search` so‘rov)
    url = f"https://olcha.uz/uz/search?q={product_name.replace(' ', '+')}"
    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code != 200:
        return {"error": "Olcha.uz dan javob olinmadi"}

    soup = BeautifulSoup(response.text, "html.parser")

    # Mahsulot kartalari (eng yaqin class)
    products = soup.select("div.product-card")

    if not products:
        return {"error": "Mahsulot topilmadi"}

    first = products[0]

    try:
        title = first.select_one(".product-title").get_text(strip=True)
        price = first.select_one(".price").get_text(strip=True)
        link = "https://olcha.uz" + first.select_one("a")["href"]

        return {
            "title": title,
            "price": clean_price(price) + " so‘m",
            "link": link
        }

    except Exception as e:
        return {"error": f"Parslashda xatolik: {e}"}
