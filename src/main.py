import numpy as np
import time
from bs4 import BeautifulSoup as soup, BeautifulSoup
import pandas as pd
import requests
import logging


logging.basicConfig(filename='log.log', level=logging.INFO)                                 # For logging errors.

headers = ({'User-Agent':                                                                   # With headers and getting
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'                                 # random ua,
                'AppleWebKit/'                                                              # insuring access to URL 
                '537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'})           # with no blocks.


page = 1

while page != 3:
    base_url = f"https://longo.lt/katalogas?search=&pageSize=24&currentPage={page}"



# print(response)

    def get_random_ua():
        random_ua = ''
        ua_file = 'ua_file.txt'
        try:
            with open(ua_file) as f:
                lines = f.readlines()
            if len(lines) > 0:
                prng = np.random.RandomState()
                index = prng.permutation(len(lines) - 1)
                idx = np.asarray(index, dtype=np.integer)[0]
                random_proxy = lines[int(idx)]
        except Exception as ex:
            print('Exception in random_ua')
            print(str(ex))
        finally:
            return random_ua


    user_agent = get_random_ua()
    headers = {
        'user-agent': user_agent,
    }

    response = requests.get(base_url, headers=headers)



    html_soup = soup(response.text, 'html.parser')

    content_list = html_soup.find_all('div', attrs={'class': 'col-6 col-md-4'})
# print(content_list)

    delays = [7, 4, 6, 2, 10, 19]
    delay = np.random.choice(delays)
    time.sleep(1.5)

    basic_info = []
    for item in content_list:
        basic_info.append(item.find_all('div', attrs={'class': 'v-card-item__content'}))           # getting page content
# print(basic_info)


    time.sleep(1.5)


    def get_names(basic_info):                                                                     # getting car names
        names = []
        for item in basic_info:
            for i in item:
                names.append(i.find_all('div', attrs={'class': 'v-card-item__title'})[0].text.strip())
        return names


    names = get_names(basic_info)

    time.sleep(1.5)


    def get_prices(basic_info):                                                                     # getting car prices.
        prices = []
        for item in basic_info:
            for i in item:
                prices.append(
                    i.find_all('span', attrs={"class": "v-card-item__price-value"})[1].string.replace(u'\xa0', u' ').strip())
        return prices


    prices = get_prices(basic_info)
    time.sleep(1.5)


    def get_motor(basic_info):                                                           # getting car motor information.
        mileages = []
        for item in basic_info:
            for i in item:
                mileages.append(i.find('div', attrs={"class": "chip"}).string)
        return mileages


    mileages = get_motor(basic_info)


    time.sleep(1.5)

    data = pd.DataFrame({"Name": names,                                                        # Framing data
                        "Mileages": mileages,
                        "Price": prices})
    data.head()
    data.drop_duplicates()

    print(data)
    data.to_excel('Car_list.xls')                                                         # Putting data to exel file

    page = page + 1




logging.info('{} : {}'.format('Names', get_names))                                          # logging information
logging.info('{} : {}'.format('Mileages', get_motor))
logging.info('{} : {}'.format('prices', get_prices))
