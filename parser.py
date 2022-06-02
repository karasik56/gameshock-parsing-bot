import requests
from bs4 import BeautifulSoup

URL_xbox360 = "https://gameshock174.ru/catalog/xbox_360/videoigry_xbox_360/videoigry_b_u_215/"
URL_ps3 = "https://gameshock174.ru/catalog/playstation_3/videoigry_ps3/videoigry_b_u_253/"

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.45 Safari/537.36',
    'accept': '*/*'
}


def get_html(url, params=None):
    r = requests.get(url, params=params, headers=HEADERS, )
    return r


def get_page_count(html):
    soup = BeautifulSoup(html, 'lxml')
    pagination = []
    pagination = soup.find_all('div', class_='nums')
    str_page = str(
        pagination[-1].get_text(strip=True))  # строка со выбором страницы, в данном случае 1,2,3... и последняя
    first_3_page, last_page = str_page.split('...')  # ... здесь в качестве разделителя
    return int(last_page)


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_="inner_wrap TYPE_1")
    games = []
    for item in items:
        games.append({
            'title': item.find('div', class_='item-title').next_element.next_element.get_text(strip=True),
            'price': ''.join(item.find('span', class_='price_value').
                             get_text(strip=True).split()),  # убираем пробелы с помощью join и split
            'availability': item.find('span', class_='value font_sxs').get_text(strip=True),
        })
    return games


def parse(platform, price=None):
    if platform == "xbox360":
        URL = URL_xbox360.strip()
    elif platform == "ps3":
        URL = URL_ps3.strip()
    html = get_html(URL)
    if html.status_code == 200:
        games = []
        page_count = get_page_count(html.text)
        for page in range(1, page_count + 1):  # перебор всех страниц с 1 до page_count
            print(f'Парсинг страницы {page} из {page_count}...')
            html = get_html(URL, params={"PAGEN_1": page})
            games.extend(get_content(html.text))
        return games
    else:
        print('Error')



