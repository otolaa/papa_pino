""" https://xn--80aayufbbb.xn--p1ai/ """
import sys, time, json
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

def get_pagen(browser, *args):
    try:
        pagen = browser.find_element(By.CSS_SELECTOR, 'div.ajax-pager-wrap')
        if pagen is not None:
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            return True
        else:
            return False

    except Exception as e:
        print(sys.exc_info()[1])
        return False

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
    time.sleep(3)
    
    try:
        ''' Этот код будет ждать 10 секунд до того, как отдаст исключение TimeoutException или если найдет элемент за эти 10 секунд, то вернет его. 
        WebDriverWait по умолчанию вызывает ExpectedCondition каждые 500 миллисекунд до тех пор, пока не получит успешный return. 
        Успешный return для ExpectedCondition имеет тип Boolean и возвращает значение true, либо возвращает not null для всех других ExpectedCondition типов. '''
        element = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.ID, "gift-modal"))
        )

        # div.ajax-pager-wrap
        if get_pagen(driver) is True:
            print(f'\033[32m[+] is set pagen\033[0m', end='\n')

        while True:
            if get_pagen(driver) is True:
                print(f'\033[32m[+] is set pagen\033[0m', end='\n')
                time.sleep(1)
            else:
                break

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

def get_items(html):
    ''' '''
    soup = BeautifulSoup(html, 'lxml')
    r_b = soup.find('body', {})
    items = r_b.find('div', {"class":'row product-list'})

    res = []
    for item in items.find_all('div', {"class":'col-lg-3 col-xl-3 col-sm-6 product-ajax-cont'}):
        p = item.find('div', {'class':'product-info'})
        f = item.find('div', {'class':'product-footer'})
        img = item.find('a', {'itemprop':'image'})
        
        if p is None:
           continue

        p_t = p.find('a', {'class':'product-title'})
        p_d = p.find('div', {'class':'product-description'})
        p_prise = f.find('span', {'itemprop':'price'})
        p_m = f.find('span', {'class':'weight'})

        r = {}
        r['name'] = p_t.text.strip()
        r['url'] = p_t.get('href')
        if p_d is not None:
            r['description'] = p_d.text.strip()

        if p_prise is not None:
            r['prise'] = p_prise.text.strip()

        if p_m is not None:
            rw = []
            for w in p_m.find_all('span'):
                rw.append(w.text.strip())

            r['weight'] = rw

        if img is not None:
            r['img'] = img.get('href')

        res.append(r)

    return res

if __name__ == "__main__":
    ''' '''
    url = 'https://xn--80aayufbbb.xn--p1ai'
    # html = get_selenium(url, '_0_')
    # r = get_links(html)

    # write_json(r, './json/link.json')
    # p(r)

    #--------------------------------------------------------------#
    pg = '_pizza_'
    url_1 = '/catalog/pizza/'
    html_1 = get_selenium(f'{url}{url_1}', '_pizza_')
        
    # html_1 = lf(f'./html/html{pg}.txt')

    data = get_items(html=html_1)
    write_json(data, f'./json/data{pg}.json')

    print(f'\033[32m[+] parse: {len(data)} element \033[0m', end='\n')