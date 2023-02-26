import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import json

# Города заданы в параметре 'area' в url
prog_language = 'python'
pages_count = 5
keywords = ['django', 'flask']


def get_headers():
    headers = Headers(browser='firefox', os='win')
    return headers.generate()


def vacancy_processing(link):
    pass


if __name__ == '__main__':
    for page in range(pages_count):
        raw_resp = requests.get(f'https://spb.hh.ru/search/vacancy?text={prog_language}&area=1&area=2&page='
                                f'{page}',
                                headers=get_headers())
        soup = BeautifulSoup(raw_resp.text, 'lxml')

        vacancies = soup.find_all('div', class_='serp-item')
        for vacancy in vacancies:
            vacancy_link = vacancy.find('a', class_='serp-item__title').attrs.get('href')
            vacancy_processing(vacancy_link)
