import requests
from bs4 import BeautifulSoup
import random

# Sahibinden kiralık ana sayfası
URL = "https://www.sahibinden.com/kiralik"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129 Safari/537.36",
    "Accept-Language": "tr-TR,tr;q=0.9",
}

def get_random_listing():
    # 1) Sayfayı çek
    response = requests.get(URL, headers=headers)
    response.raise_for_status()

    # 2) HTML'i parse et
    soup = BeautifulSoup(response.text, "html.parser")

    # 3) Tüm ilan linklerini bul (tabloda listelenir)
    # Normal ilanlar "class='classifiedTitle'" içindeki <a> etiketinde
    links = [a["href"] for a in soup.select(".classifiedTitle a") if a.get("href")]

    if not links:
        raise Exception("İlan bulunamadı. Sahibinden bot koruması devrede olabilir.")

    # 4) Rastgele bir ilan seç
    random_link = random.choice(links)

    # 5) Tam URL'ye dönüştür
    full_url = "https://www.sahibinden.com" + random_link

    return full_url


if __name__ == "__main__":
    ilan = get_random_listing()
    print("Rastgele İlan URL:", ilan)
