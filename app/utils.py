# filepath: app/utils.py
import requests
from bs4 import BeautifulSoup
import random

def get_amazon_product(asin, domain='co.uk'):
    headers = {
        'User-Agent': random.choice([
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
        ]),
        'Accept-Language': 'en-US,en;q=0.9'
    }

    url = f"https://www.amazon.{domain}/dp/{asin}"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching product data: {e}")
        return None

    soup = BeautifulSoup(response.content, 'lxml')
    title = soup.select_one("#productTitle")
    price = soup.select_one(".a-price .a-offscreen")
    image = soup.select_one("#landingImage")

    try:
        return {
            "title": title.get_text(strip=True) if title else "N/A",
            "price": float(price.get_text(strip=True).replace('£', '').replace(',', '')) if price else None,
            "asin": asin,
            "url": url,
            "image": image['src'] if image else None
        }
    except Exception as e:
        print(f"Error parsing product data: {e}")
        return None