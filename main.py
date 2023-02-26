import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import json

prog_language = 'python'
cities = ['Москва', 'Санкт-Петербург']
keywords = ['Django', 'Flask']


def get_headers():
    headers = Headers(browser='firefox', os='win')
    return headers.generate()


if __name__ == '__main__':
    raw_resp = requests.get(f'https://spb.hh.ru/search/vacancy?text={prog_language}&area=1&area=2',
                            headers=get_headers())
    soup = BeautifulSoup(raw_resp.text, 'lxml')
