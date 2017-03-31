import requests
import json
import re
from selenium import webdriver
from base64 import b64decode
import os.path


def send_requests(start):
    """
    Функция посылает запрос на получение доменов
    :param start: порядковый номер страницы
    :rtype: response
    :return: Ответ запроса
    """
    url = 'https://domainpunch.com/tlds/daily.php'
    headers = {
        "X-Requested-With": "XMLHttpRequest"
    }
    params = {
        'domains': '',
        'start': start,
        'length': 50000,
        'zid': 1

    }

    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        return response


def get_all_domains():
    """
    Функция возвращает список доменов полученных с сайта domainpunch.com
    :rtype: list
    :return: Список доменов
    """
    domains_list = list()
    start = 0

    response = send_requests(start)
    tmp = json.loads(response.text)
    count = tmp['recordsTotal']
    domains_list += [domain_name['1'] for domain_name in tmp['data']]
    while len(domains_list) < count:
        start = len(domains_list)
        response = send_requests(start)
        tmp = json.loads(response.text)
        domains_list += [domain_name['1'] for domain_name in tmp['data']]
    return domains_list


def check_reg(text, reg_exp, flag=False):
    """
    Функция проверяет совпадение ввденного ключевого слова или регулярного выражения с именем домена
    :param text: Имя домена
    :param reg_exp: Слово или регулярное выражение
    :param flag: False
    :return:
    """
    if flag:
        pre_match = re.search(r"" + reg_exp, str(text))
        if pre_match is not None:
            return True
        return False


def screen(titles):
    """
    Функция вовзращает итератор по списку доменов полученных с сайта domainpunch.com
    :rtype: list
    :return: Список доменов
    """
    driver = webdriver.PhantomJS(os.path.abspath('.') + '/phantomjs/bin/phantomjs')
    for tit in titles:
        driver.get("https://" + tit)
        ba = b64decode(driver.get_screenshot_as_base64())
        description = driver.title
        title = tit
        yield [title, description, ba]
