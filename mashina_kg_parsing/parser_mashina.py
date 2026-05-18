import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from urllib.parse import urljoin


BASE_URL = 'https://mashina.kg'
SEARCH_URL = 'https://mashina.kg/search/passenger'
OUTPUT_FILE = 'mashina_kg_cars.csv'
DELAY_SECONDS = 1.5
MAX_PAGES = 20

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ru-RU,ru;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}




"""================= загрузка html ================="""

SESSION = requests.Session()
SESSION.headers.update(HEADERS)

def get_html(url: str, retries: int = 3) -> str | None:
    for attempt in range(1, retries + 1):
        try:
            response = SESSION.get(url, timeout=15)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"попытка {attempt}/{retries} для {url}: {e}")
            if attempt == retries:
                return None
            time.sleep(2 ** attempt)
    return None


"""================= парсинг одной машины ================="""
def parse_card(card) -> dict | None:
    href = card.get('href', '')
    if not href.startswith('/details/'):
        return None

    url = urljoin(BASE_URL, href)

    title_tag = card.select_one('h3')
    title = re.sub(r'(?i)продажа\s*', '', title_tag.get_text(strip=True)).strip() if title_tag else ''

    img_tag = card.select_one('img')
    image_url = img_tag.get('src', '') if img_tag else ''

    city_tag = card.select_one('span.text-white.text-sm.leading-5.truncate')
    city = city_tag.get_text(strip=True) if city_tag else ''

    # год и пробег: "2019/113413 km"
    year, mileage_km = None, None
    year_mileage_tag = card.select_one('span.whitespace-nowrap.shrink-0')
    if year_mileage_tag:
        text = year_mileage_tag.get_text(strip=True)
        match = re.match(r'(\d{4})\s*/\s*([\d\s]+)', text)
        if match:
            year = int(match.group(1))
            mileage_km = int(re.sub(r'\D', '', match.group(2)))

    # цена в сомах
    price_kgs = None
    price_kgs_tag = card.select_one('span.font-bold.text-xs.text-text-secondary')
    if price_kgs_tag:
        digits = re.sub(r'\D', '', price_kgs_tag.get_text())
        price_kgs = int(digits) if digits else None

    # цена в долларах
    price_usd = None
    for span in card.select('span.text-xs.text-text-secondary'):
        text = span.get_text(strip=True)
        if '$' in text:
            digits = re.sub(r'\D', '', text)
            price_usd = int(digits) if digits else None
            break

    # двигатель и коробка передач
    engine, akpp = '', ''
    for span in card.select('span'):
        text = span.get_text(strip=True)
        if 'л.' in text and '/' in text:
            parts = text.split('/')
            engine = parts[0].strip()
            akpp = parts[1].strip() if len(parts) > 1 else ''
            break

    return {
        'url': url,
        'title': title,
        'price_usd': price_usd,
        'price_kgs': price_kgs,
        'year': year,
        'mileage_km': mileage_km,
        'engine': engine,
        'akpp': akpp,
        'city': city,
        'image_url': image_url,
    }


"""================= парсинг одной страницы ================="""
def parse_page(html: str) -> list[dict]:
    soup = BeautifulSoup(html, 'lxml')
    cards = soup.select('a[href^="/details/"]')
    results = []
    seen = set()
    for card in cards:
        item = parse_card(card)
        if item and item['url'] not in seen:
            seen.add(item['url'])
            results.append(item)
    return results


"""================= обход всех страниц ================="""
def fetch_all_pages(num_pages: int) -> list[dict]:
    all_cars = {}

    # страница 1
    html = get_html(SEARCH_URL)
    if not html:
        print('не удалось загрузить первую страницу')
        return []

    items = parse_page(html)
    for item in items:
        all_cars[item['url']] = item
    print(f'страница 1/{num_pages}: {len(items)} объявлений')

    # страницы 2 и другие 
    for page_num in range(2, num_pages + 1):
        time.sleep(DELAY_SECONDS)
        url = f'{SEARCH_URL}?page={page_num}'
        html = get_html(url)
        if not html:
            print(f'страница {page_num} пропущена')
            continue
        items = parse_page(html)
        new = 0
        for item in items:
            if item['url'] not in all_cars:
                all_cars[item['url']] = item
                new += 1
        print(f'страница {page_num}/{num_pages}: {len(items)} объявлений, новых: {new}')

    return list(all_cars.values())


"""================= сохранение в csv ================="""
def save_to_csv(cars: list[dict], file_name: str):
    df = pd.DataFrame(cars)
    df.to_csv(file_name, index=False, encoding='utf-8-sig')
    print(f'сохранено {len(df)} машин → {file_name}')


"""================= точка входа ================="""
if __name__ == '__main__':
    cars = fetch_all_pages(MAX_PAGES)
    save_to_csv(cars, OUTPUT_FILE)
    print('the end')
