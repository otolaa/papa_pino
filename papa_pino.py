""" https://xn--80aayufbbb.xn--p1ai/ """
import sys, time, json
from datetime import datetime
import requests, fake_useragent
from bs4 import BeautifulSoup
from tinydb import TinyDB, Query
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def p(text, *args):
    print(text, *args, sep=' / ', end='\n')

def wtf(html, pg):
    with open(f'./html/html{pg}.txt', "w", encoding='utf8') as f:
        f.write(html)

def lf(filename):
    with open(filename, 'r') as f:
        return f.read()

def write_json(data, path):
    with open(path, 'w', encoding='utf8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)  

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_selenium(url, pg = None):
    """ start selenium """       
    service = Service(executable_path='/usr/local/bin/geckodriver')
    options = Options()
    options.add_experimental_option("detach", True)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.headless = True    
    driver = webdriver.Chrome(options=options)

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        'source': '''
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Object
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Proxy
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol
        '''
    })

    driver.maximize_window()
    driver.get(url)
    time.sleep(7)
    
    try:
        ''' Этот код будет ждать 10 секунд до того, как отдаст исключение TimeoutException или если найдет элемент за эти 10 секунд, то вернет его. 
        WebDriverWait по умолчанию вызывает ExpectedCondition каждые 500 миллисекунд до тех пор, пока не получит успешный return. 
        Успешный return для ExpectedCondition имеет тип Boolean и возвращает значение true, либо возвращает not null для всех других ExpectedCondition типов. '''
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "gift-modal"))
        )

        html = driver.page_source        
        if pg is not None:
            wtf(html, pg)

        print(f'\033[32m[+] success return html \033[0m', end='\n')
        return html
    
    except Exception as e:
        print(f'\033[31m[-] errorf: {sys.exc_info()[1]}\033[0m', end='\n')

def get_links(html):
    ''' '''
    soup = BeautifulSoup(html, 'lxml')
    result_body = soup.find('body', {})

    r = []
    ul = result_body.find('ul', {"class":"font-fix menu-general"})
    for lia in ul.find_all('a'):
        
        row = {}
        row['name'] = lia.text.strip()
        row['href'] = lia.get('href')

        r.append(row)
    
    return r

def get_item(html):
    soup = BeautifulSoup(html, 'lxml')
    r_b = soup.find('body', {})

    for item in r_b.find_all('div', {"class":'row product-list'}):
        # p(item.text.strip())
        pass

if __name__ == "__main__":
    ''' '''
    url = 'https://xn--80aayufbbb.xn--p1ai/'
    html = get_selenium(url, '_0_')
    r = get_links(html)

    write_json(r, './json/link.json')
    p(r)

    # url_1 = 'https://xn--80aayufbbb.xn--p1ai/catalog/pizza/'
    # html_1 = get_selenium(url_1, '_pizza_')
    # get_item(html_1)