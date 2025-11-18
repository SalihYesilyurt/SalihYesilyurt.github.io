import requests
from bs4 import BeautifulSoup
import random

BASE = "https://www.sahibinden.com"
LISTING_URL = BASE + "/kiralik"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129 Safari/537.36"
}

def pick_random_listing():
    """Kiralık sayfasından rastgele bir ilan döndürür (URL olarak)."""
    html = requests.get(LISTING_URL, headers=headers).text
    soup = BeautifulSoup(html, "html.parser")

    links = [a["href"] for a in soup.select(".classifiedTitle a") if a.get("href")]

    if not links:
        raise Exception("İlan linki bulunamadı. Muhtemelen bot koruması devrede.")

    return BASE + random.choice(links)


def scrape_listing(url):
    """İlanın tüm detaylarını (fiyat hariç) çeker."""
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, "html.parser")

    # FOTOĞRAFLAR
    photos = [img.get("data-src") for img in soup.select("#classifiedDetail img") if img.get("data-src")]

    # FİYAT
    price_tag = soup.select_one(".classifiedInfo h3")
    price = price_tag.text.strip().replace("\n", "") if price_tag else None

    # ÖZELLİKLER
    features = {}
    for row in soup.select("#classifiedDetail td"):
        key = row.get("data-label")
        if key:
            features[key.strip()] = row.text.strip()

    return {
        "url": url,
        "photos": photos,
        "features": features,
        "price": price  # backend gizleyecek
    }
