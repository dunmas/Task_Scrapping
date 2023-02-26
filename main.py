import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import json
import re

# Города заданы в параметре 'area' в url
prog_language = 'python'
pages_count = 1
keywords = ['django', 'flask']


def get_headers():
    headers = Headers(browser='firefox', os='win')
    return headers.generate()


def vacancy_processing(link, result_list):
    resp = requests.get(link, headers=get_headers())
    soup = BeautifulSoup(resp.text, 'lxml')

    description = soup.find('div', class_='vacancy-description')
    find_flag = False

    for keyword in keywords:
        regex = re.compile(keyword, re.I)
        match_res = description.find_all(string=regex)

        if match_res:
            find_flag = True
            break

    if not find_flag:
        return

    salary = soup.find('div', attrs={'data-qa': 'vacancy-salary'})
    company = soup.find('a', attrs={'data-qa': 'vacancy-company-name'})
    city = soup.find('span', attrs={'data-qa': 'vacancy-view-raw-address'})
    if city is None:
        city = soup.find('p', attrs={'data-qa': 'vacancy-view-location'})

    result = {
        'link': link,
        'salary': salary.text.replace('\xa0', ""),
        'company': company.text.replace('\xa0', " "),
        'city': city.contents[0]
    }

    result_list.append(result)


if __name__ == '__main__':
    vacancies_list = []
    for page in range(pages_count):
        raw_resp = requests.get(f'https://spb.hh.ru/search/vacancy?text={prog_language}&area=1&area=2&page='
                                f'{page}',
                                headers=get_headers())
        main_soup = BeautifulSoup(raw_resp.text, 'lxml')

        vacancies = main_soup.find_all('div', class_='serp-item')
        for vacancy in vacancies:
            vacancy_link = vacancy.find('a', class_='serp-item__title').attrs.get('href')
            vacancy_processing(vacancy_link, vacancies_list)
