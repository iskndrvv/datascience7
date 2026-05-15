'''парсинг машин с сайта turbo.kg
задача:
вытащить первые 20 страниц и все данные о машинах 
данные об автомобилях сохранять в CSV файлах

какие данные нам нужны:
-название и модели
-цена
-год выпуска
-url объявления
-url картинки

добавочно вытащить 13 характеристик (руль, кузов, цвет, пробег, привод итд)
-все ссылки на фотографии 
-дата и время создания публикации

инструменты:
requests - http запросы
BeautifulSoup4 - парсинг html
pandas - экспорт данных в CSV файл
lxml - быстрый бэкенд для BS4
'''



"""================= начало ================="""

import requests
from bs4 import BeautifulSoup
# BeautifulSoup - превращает строку html в определенный скрипт 
# по которому мы можем пройтись и удобно искать как html теги так и CSS - селекторы
import pandas as pd
# хорошо обрабатывает разные виды ключей и если у одного нет
# определенного поля то сам создает пустую ячейку и заполняет ее None
import time
# time - нужен для пауз между запросами 
import re
# re - регулярные выражения (для очистки цены '134304 сом' -> 134304)
from urllib.parse import urljoin
# urljoin - корректно склеивает относительный url с базовым



"""================= настройки и константы ================="""

BASE_URL = 'https://turbo.kg' # базовая ссылка на сайт который мы парсим 
OUTPUT_CSV = 'turbo_cars.csv' # название файла куда мы запишем наши данные 
DELAY_SEC = 1.0 # пауза между запросами, во избежания Ddos атак и получить бан или ошибку 429
PAGES_TO_PARSE = 20 # сколько стр нам надо обработать 

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ru-RU,ru;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

# HTTP заголовки. User-Agent - обязателен без него выкинет ошибку 403
# прикидываемся обычным пользователем декстопным приложением Chrome
# Accept-Language - язык пользователя
# Accept - что сайт ожидает от нас и что мы ждем от сайта (ответ в каком формате)



"""================= загрузка html ================="""
SESSION = requests.Session()
SESSION.headers.update(HEADERS)
# requests.session() — объект сессии для http запросов
# он переиспользует tcp соединение и сохраняет cookies между запросами
# зачем это нужно:
# 1 ускоряет работу парсера потому что не создает новое соединение для каждого запроса
# 2 сохраняет cookies которые сайт может выдать при первом посещении
# 3 позволяет хранить общие headers для всех запросов

# важно:
# если сайт не принимает запросы или считает их подозрительными
# он может вернуть ошибку 403 forbidden
# это может быть связано с отсутствием cookies неправильными headers
# защитой от ботов или слишком частыми запросами

def fetch_html(url: str, retries: int = 3) -> str | None:
    # получает html страницы в виде строки
    # использует общую session с cookies между запросами
    # если запрос не удался пробует повторить несколько раз

    for attempt in range(1, retries + 1):
        try:
            response = SESSION.get(url, timeout=15)
            # timeout=15 не ждем ответ дольше 15 секунд

            response.raise_for_status()
            # если сервер вернул ошибку например 403 404 500 вызовется исключение

            return response.text

        except requests.RequestException as e:
            print(f"попытка {attempt}/{retries} для {url}: {e}")

            # если это последняя попытка то прекращаем запросы
            if attempt == retries:
                return None

            time.sleep(2 ** attempt)
            # экспоненциальная пауза 2с 4с 8с
            # даем серверу время и не отправляем запросы слишком часто

    return None

# print(fetch_html(url=BASE_URL))


"""================= вспомогательные функции для очистки ================="""
def extract_price(text: str) -> int | None:
    '''
    превращает строку с ценой в число
    для очистки цены '134304 сом' -> 134304

    алогоритм работы:
    1) если в тексте есть слово 'сом' берет только цифры, которые идут 
    непосредственнок до него (перед ним)
        с возможными пробелами между ними
        это защищает нас от того что в тексте не будет года или объема
    2) если 'cом' нет то берем все цифры подряд
    '''
    
    if not text:
        return None
    
    text = text.replace('\xa0', ' ')
    # нормализовать неразрывные пробелы (\xa0) в обычные 

    match = re.search(r'([\d\s]+)\s*сом', text)
    if match:
        digits = re.sub(r'\D', '', match.group(1))
        return int(digits) if digits else None
    
    digits = re.sub(r'\D', '', text)
    return int(digits) if digits else None


def extract_year(text: str) -> int | None:
    """
    вытаскивает год из текста
    пример: 'toyota camry 2008 год' -> 2008

    алгоритм работы:
    1 если текста нет возвращает none
    2 ищет год в формате 1900-2099
    3 если год найден возвращает его как число int
    4 если год не найден возвращает none
    """

    if not text:
        return None

    match = re.search(r"\b(19\d{2}|20\d{2})\b", text)
    # ищем год от 1900 до 2099
    # \b нужен чтобы не брать год из середины большого числа

    if match:
        return int(match.group(1))

    return None


def extract_mileage(text: str) -> int | None:
    if not text:
        return None
    
    digits = re.sub(r'[^\d]', '', text)
    return int(digits) if digits else None


"""================= парсинг turbo-stream ответа ================="""
'''
<turbo-stream action="update" target="madal">
<template>
контент
</template>
'''
def extract_turbo_template(html: str) -> str:
    # исправлено: </template> вместо <template>
    match = re.search(r'<template>(.*?)</template>', html, flags=re.DOTALL)
    return match.group(1) if match else html


"""================= парсинг одной страницы ================="""
def parse_catalog_page(html: str) -> list[dict]:
    # получаем html страницу отправив запрос на ссылку https://turbo.kg/?page=1#scroll
    soup = BeautifulSoup(html, 'lxml')
    cars_by_url = {} # словарь или наше бд для хранения уникальных машин

    # найти все ссылки на отдельные машины
    # селектор a[href*="/cars/"] ловит любой <a> в href содержится подстрока /cars/
    for link in soup.select('a[href*="/cars/"]'):
        href = link.get('href', '')

        if not re.match(r"^/cars/[A-Za-z0-9]+$", href):
            continue
        full_url = urljoin(BASE_URL, href)

        # если мы находим дубликат действуем по следующему сценарию:
        if full_url in cars_by_url:
            title_attr = link.get('title', '').strip()
            if title_attr and not cars_by_url[full_url].get('name'):
                cars_by_url[full_url]['name'] = title_attr
            continue

        """================= название ================="""
        name = link.get('title', '').strip() or link.get_text(' ', strip=True)

        """================= изображения ================="""
        img_url = ''
        img_tag = link.find('img')
        if img_tag:
            img_url = img_tag.get('src', '') or img_tag.get('data-src', '')

        # сохраняем в словарь
        cars_by_url[full_url] = {
            'url': full_url,
            'name': name,
            'image_url': img_url,
            'price': None,
            'year_from_catalog': None
        }

    # вытащим цену и год выпуска 
    for link in soup.select('a[href*="/cars/"]'):
        href = link.get('href', '')
        if not re.match(r"^/cars/[A-Za-z0-9]+$", href):
            continue

        full_url = urljoin(BASE_URL, href)
        if full_url not in cars_by_url:
            continue

        text = link.get_text(' ', strip=True) # берем весь текст внутри ссылки

        if 'сом' in text and cars_by_url[full_url]['price'] is None:
            cars_by_url[full_url]['price'] = extract_price(text)

        if cars_by_url[full_url]['year_from_catalog'] is None:
            cars_by_url[full_url]['year_from_catalog'] = extract_year(text)

        if not cars_by_url[full_url]['name']:
            clean_text_from_year = re.sub(r'\d{4}\s*г\.?', '', text)
            # исправлено: убран пробел внутри квантификатора [\d\s] + -> [\d\s]+
            clean_text_from_price = re.sub(r'~?\s*[\d\s]+\s*сом', '', clean_text_from_year)
            cars_by_url[full_url]['name'] = clean_text_from_price.strip()

    return list(cars_by_url.values())




"""================= детальный парсинг машин ================="""

def parse_car_page(html: str) -> dict:
    '''
    получаем html конкретной машины и будем доставать из него название, цену, характеристики 
    и ссылки на картинки, время публикации 
    '''

    inner_html = extract_turbo_template(html)
    soup = BeautifulSoup(inner_html, 'lxml')
    result = {}
    

    """================= получение точного названия ================="""
    title_tag = soup.select_one('h1.h5')
    if title_tag:
        result['full_name'] = title_tag.get_text(strip=True)


    """================= получение точной цены ================="""
    price_tag = soup.select_one('div.h4 b')
    if price_tag:
        result['price_soms'] = extract_price(price_tag.get_text(strip=True))


    """================= получение характеристик ================="""
    specs = {}
    dl = soup.select_one('dl.row')
    if dl:
        dt_list = dl.find_all('dt')
        # получили список названий всех характеристик под тегом dt
        dd_list = dl.find_all('dd')
        # получили список значений всех характеристик под тегом dd
        for name_specs, value_specs in zip(dt_list, dd_list):
        

            clear_name = name_specs.get_text(strip=True) # получили не html а текст
            clear_value = value_specs.get_text(strip=True) # получили не html а текст
            if clear_name:
                specs[clear_name] = clear_value

        # разложили харак-ки на отдельные колонки(чтобы легче записать в csv файл)
        for k, v in specs.items():
            result[f'specs_{k}'] = v

        if 'Пробег' in specs:
            result['mileage_km'] = extract_mileage(specs['Пробег'])

    photo_urls = []
    for a in soup.select('a.d-block[href]'):
        href = a['href']
        if href.lower().endswith(('.jpeg', '.jpg', '.png', '.webp', '.avif')):
            photo_urls.append(href)

    result['photos'] = ' | '.join(photo_urls)
    result['photos_count'] = len(photo_urls)

    time_tag = soup.select_one('time[datetime]')
    if time_tag:
        result['published_at'] = time_tag['datetime']

    return result
    




    
"""================= оркестратор (главная функция) ================="""

def scrape_all_cars(num_pages: int) -> list[dict]:
    '''
    главная функция которая проходится по страницам и вытаскивать каждый авто
    и его характеристики    
    ''' 
    all_cars = []

    # 1 обход страниц
    for page_num in range(1, num_pages+1):
        url = f'{BASE_URL}/?page={page_num}'

        html = fetch_html(url)
        if not html:
            print(f'страница {page_num} пропущена')
            continue
        page_items = parse_catalog_page(html)

        if not page_items:
            print(f'нет объявлений или не получили доступ')
            break


        all_cars.extend(page_items)

        time.sleep(DELAY_SEC)

    # 2 детально машины
    total = len(all_cars)
    for i, car in enumerate(all_cars, start=1):
        print(f'[{i}/{total}] {car["url"]}')
        html = fetch_html(car['url'])
        if html is None:
            continue
        details = parse_car_page(html)
        if not details:
            continue
        car.update(details)

        time.sleep(DELAY_SEC)

    return all_cars


def save_to_csv(cars, file_name):
    df = pd.DataFrame(cars)
    main_columns = [
        'url', 'name', 'full_name', 'price', 'year_from_catalog', 'mileage_km', 
        'image_url', 'photos_count', 'published_at'
    ]    

    specs_columns = sorted([c for c in df.columns if c.startswith('specs_')])

    other_columns = [
        c for c in df.columns if c not in main_columns and not c.startswith('specs_')
    ]

    final = [c for c in main_columns if c in df.columns] + specs_columns + other_columns
    df = df[final]


    df.to_csv(file_name, index=False, encoding='utf-8-sig')
    print(f'сохранено {len(df)} машин → {file_name}')




if __name__ == "__main__":
    cars = scrape_all_cars(PAGES_TO_PARSE)
    save_to_csv(cars, OUTPUT_CSV)
    print('the end xd')