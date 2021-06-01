import base64

import svgwrite
import svgwrite.container
import svgwrite.shapes
import svgwrite.image
import bs4
import os

from urllib.request import urlopen
from selenium import webdriver

index = 0
code = input('덱 코드를 입력하세요.> ')
os.mkdir(code)

url = 'https://pokemoncard.co.kr/recipe/search?code=' + code
driver = webdriver.PhantomJS('phantomjs.exe')
driver.implicitly_wait(5)
driver.get(url)

soup = bs4.BeautifulSoup(driver.page_source, 'lxml')
card_items = soup.select(f'#show-card-detail-{code} .card-item')

card_list = []
for item in card_items:
    cnt = item.select_one('.count')
    cnt = int(cnt.text)

    for i in range(cnt):
        img = item.select_one('img')
        card_list.append(img['src'])

pages = (len(card_list) // 9) + 1 if len(card_list) % 9 != 0 else 0
start_x, start_y = 10.5, 16.5
for p in range(0, pages):
    x, y = 0, 0

    path = os.path.join(code, f'card{p + 1}.svg')
    dwg = svgwrite.Drawing(path, size=('210mm', '297mm'))

    background = svgwrite.container.Group()
    background.add(svgwrite.shapes.Rect(size=('210mm', '297mm'), fill='#ffe659'))
    dwg.add(background)

    cards_group = svgwrite.container.Group()

    for i in range(0, 9):
        index = p * 9 + i
        if index >= len(card_list):
            break

        image = urlopen(card_list[index]).read()
        cards_group.add(svgwrite.image.Image(
            href='data:image/png;base64,' + base64.b64encode(image).decode(),
            width='63mm', height='88mm',
            x=str(start_x + (63 * x))+'mm', y=str(start_y + (88 * y))+'mm')),

        x += 1

        if x >= 3:
            x = 0
            y += 1

        if y >= 3:
            continue

    dwg.add(cards_group)
    dwg.save()
