import requests
from bs4 import BeautifulSoup

def search_asaxiy(query):
    try:
        url = f"https://asaxiy.uz/product?key={query}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return "❌ Saytdan javob olinmadi"

        soup = BeautifulSoup(response.text, "html.parser")
        product = soup.find("div", class_="product__item d-flex flex-column justify-content-between")

        if not product:
            return "❌ Mahsulot topilmadi"

        name = product.find("a", class_="product__item__info-title").text.strip()
        price = product.find("span", class_="product__item-price").text.strip()

        return f"✅ Asaxiy:\n📦 {name}\n💰 {price}"

    except Exception as e:
        return f"❌ Xatolik: {e}"

# Test
if __name__ == "__main__":
    query = input("Qidiruv so‘rovi: ")
    result = search_asaxiy(query)
    print(result)
