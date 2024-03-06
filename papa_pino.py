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
from help import *


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

def get_selenium_driver():
    """ start selenium driver """
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
    return driver

def get_html(driver, url, pg = None):
    """"""   
    driver.get(url)
    time.sleep(0.5)
    
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

def get_attr_tag(tag):
    '''  '''
    attrs = {}
    for key, value in tag.attrs.items():
        ss = -1
        for s in ['data-price', 'data-weight', 'data-old-price']:
            ss = key.find(s)
            if ss >= 0:
                attrs[s.replace('data-','')] = value

        if ss == -1 and key in ['value', 'type', 'name']:
            attrs[key] = value

    return attrs

def get_properties(property_item):
    pro = []
    for prop_div in property_item.find_all('div', {"class":"row"}):
        prop_t = prop_div.find('div', {"class":"option_title"})

        if prop_t is not None:
            # Дополнительно:
            prop_title = prop_t.text.strip()
            if prop_title == 'Дополнительно:':
                continue
            
            labels_ = []
            for ls in prop_div.find_all('label', {}):
                #---@@@$$$@@@---#
                l_item = {}
                l_title = ls.text.strip()
                
                input_item = ls.find('input')
                if input_item is not None:
                    l_item = get_attr_tag(input_item)
                    if len(l_title) > 0:
                        l_item['title'] = l_title

                if len(l_item) > 0:
                    labels_.append(l_item)
            
            lb = {}
            lb['title'] = prop_title
            lb['labels'] = labels_
            pro.append(lb)
    
    sr = []
    for pro_div in property_item.find_all('div', {"class":"row"}):
        prop_t = pro_div.find('div', {"class":"option_title"})

        if prop_t is None:
            for spn in pro_div.find_all('label', {}):
                l1_item = {}
                span_t = spn.text.strip()

                input_item_1 = spn.find('input')
                if input_item_1 is not None:
                    l1_item = get_attr_tag(input_item_1)

                    if len(span_t) > 0:
                        l1_item['title'] = span_t

                if len(l1_item) > 0:
                    sr.append(l1_item)

    if len(sr) > 0:
        pro.append({'title':'Дополнительно:','labels':sr})

    return pro

def get_items(html):
    ''' '''
    soup = BeautifulSoup(html, 'lxml')
    r_b = soup.find('body', {})
    items = r_b.find('div', {"class":'row product-list'})

    res = []
    for item in items.find_all('div', {"class":'col-lg-3 col-xl-3 col-sm-6 product-ajax-cont'}):
        ''''''
        product = item.find('div', {'class':'product-item'})
        if product is None:
            continue

        property_item = product.find('div', {'class':'product-options'})
        p = product.find('div', {'class':'product-info'})
        f = product.find('div', {'class':'product-footer'})
        img = product.find('a', {'itemprop':'image'})
        
        if p is None:
           continue

        p_t = p.find('a', {'class':'product-title'})
        p_d = p.find('div', {'class':'product-description'})
        p_prise = f.find('span', {'itemprop':'price'})
        p_m = f.find('span', {'class':'weight'})

        r = {}
        r['pid'] = product.get('data-id')
        r['unit'] = product.get('data-unit')
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
        
        if property_item is not None:
            ''' properties '''          
            r['properties'] = get_properties(property_item)

        res.append(r)

    return res

if __name__ == "__main__":
    ''' '''
    url = 'https://xn--80aayufbbb.xn--p1ai'
    
    driver = get_selenium_driver();
    get_html(driver, f'{url}', None)

    for href_ in load_json('./json/link.json'):
        url_path = href_['href']
        code_page = url_path.replace('/catalog/','').replace('/','').replace('-','_')
        #--------------------------$$$---------------------------------#
        print(f'\033[32m[+] start {url_path} code {code_page} \033[0m', end='\n')

        #--------------------------$$$---------------------------------#
        pg = f'_{code_page}_'        
        html_ = get_html(driver, f'{url}{url_path}', pg)
            
        # html_ = lf(f'./html/html{pg}.txt') # htm for file

        data = get_items(html=html_)
        write_json(data, f'./json/data{pg}.json')

        print(f'\033[32m[+] parse: {len(data)} element \033[0m', end='\n')