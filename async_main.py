import datetime
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import aiohttp
import asyncio
import pandas as pd


async def collect_data(city_code='2398'):
    cur_time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M_%S')
    ua = UserAgent()

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent': ua.random
    }

    cookies = {
        'mg_geo_id': f'{city_code}'
    }

    async with aiohttp.ClientSession() as session:

        response = await session.get(url='https://magnit.ru/promo/', headers=headers, cookies=cookies)
        soup = BeautifulSoup(await response.text(), 'lxml')

        city = soup.find('a', class_='header__contacts-link_city').text.strip()
        cards = soup.find_all('a', class_='card-sale_catalogue')

        data = {'Продукт': [],
                'Старая цена': [],
                'Новая цена': [],
                'Процент скидки': [],
                'Время акции': []
                }
        for card in cards:
            try:
                card_title = card.find('div', class_='card-sale__title').text.strip()

                card_discount = card.find('div', class_='card-sale__discount').text.strip()

                card_price_old_integer = card.find('div', class_='label__price_old').find('span',
                                                                                          class_='label__price-integer').text.strip()
                card_price_old_decimal = card.find('div', class_='label__price_old').find('span',
                                                                                          class_='label__price-decimal').text.strip()
                card_old_price = f'{card_price_old_integer}.{card_price_old_decimal}'

                card_price_integer = card.find('div', class_='label__price_new').find('span',
                                                                                      class_='label__price-integer').text.strip()
                card_price_decimal = card.find('div', class_='label__price_new').find('span',
                                                                                      class_='label__price-decimal').text.strip()
                card_price = f'{card_price_integer}.{card_price_decimal}'

                card_sale_date = card.find('div', class_='card-sale__date').text.strip().replace('\n', ' ')


                data['Продукт'].append(card_title)

                data['Старая цена'].append(card_discount)

                data['Новая цена'].append(card_old_price)

                data['Процент скидки'].append(card_price)

                data['Время акции'].append(card_sale_date)

            except AttributeError:

                continue


    df = pd.DataFrame(data)
    df.to_excel(f'{city}_{cur_time}.xlsx')
    return f'{city}_{cur_time}.xlsx'


async def main():
    await collect_data(city_code='2398')


if __name__ == '__main__':
    asyncio.run(main())