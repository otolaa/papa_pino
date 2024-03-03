from lxml import etree, objectify
import datetime, json, sys


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)
    
def get_doc():
    ''' create the root element '''
    today = datetime.date.today()
    today_format = today.strftime("%Y-%m-%dT%H:%M:%S%Z")
    pageYmlCatalog = etree.Element('yml_catalog', date=str(today_format))

    # make a new document tree
    doc = etree.ElementTree(pageYmlCatalog)

    # add the subelements
    pageElementShop = etree.SubElement(pageYmlCatalog, 'shop')

    # for multiple multiple attributes, use as shown above
    etree.SubElement(pageElementShop, 'name').text = 'https://xn--80aayufbbb.xn--p1ai'
    etree.SubElement(pageElementShop, 'company').text = 'https://xn--80aayufbbb.xn--p1ai'
    etree.SubElement(pageElementShop, 'url').text = 'https://xn--80aayufbbb.xn--p1ai'
    
    currenciesElem = etree.SubElement(pageElementShop, 'currencies')
    etree.SubElement(currenciesElem, 'currency', id='RUR', rate='1')
    
    categoryElement = etree.SubElement(pageElementShop, 'categories')
    for int, category_item in enumerate(load_json('./json/link.json'), 1):
        etree.SubElement(categoryElement, 'category', id=str(int)).text = category_item['name']

    offersElement = etree.SubElement(pageElementShop, 'offers')
    for int, cat_item in enumerate(load_json('./json/link.json'), 1):
        code_page = cat_item['href'].replace('/catalog/','').replace('/','').replace('-','_')
        
        for offer in load_json(f'./json/data_{code_page}_.json'):
            offerElem = etree.SubElement(offersElement, 'offer', id=str(offer['pid']))
            etree.SubElement(offerElem, 'name').text = offer['name']
            
            if offer['description']:
                etree.SubElement(offerElem, 'description').text = f"<![CDATA[{offer['description'].replace('�','')}]]>"
            
            etree.SubElement(offerElem, 'picture').text = f"https://xn--80aayufbbb.xn--p1ai{offer['url']}"
            etree.SubElement(offerElem, 'categoryId').text = str(int)
            
            if offer['prise']:
                etree.SubElement(offerElem, 'price').text = offer['prise']
            
            if offer['weight'] and len(offer['weight']) > 0 and len(offer['weight'][0]) > 0:
                w = float(offer['weight'][0].replace(',','.'))
                we = w/1000
                etree.SubElement(offerElem, 'weight').text = str(we)
            
            # <param name="Размер экрана" unit="дюйм">27</param>
            if len(offer['properties'])>0:
                for pro in offer['properties']:
                    if pro['title'] == 'Дополнительно:':
                        continue

                    label_ = (pro['label'][0]).strip().split(' ')
                    if len(label_)>=2:
                        label_title = (pro['title']).replace('Объем','Размер').replace('объём','Размер')
                        if label_[1] == 'штук' or label_[1] == 'шт':
                            label_title = 'Размер'
                            label_[1] = 'штук'

                        etree.SubElement(offerElem, 'param', name=label_title, unit=label_[1]).text = label_[0].replace(',','.')

        print(f'\033[32m[+] {int} add: {code_page}\033[0m', end='\n')


    return doc

if __name__ == "__main__":
    ''' save to XML file '''
    doc = get_doc()
    obj_xml = etree.tostring(doc, xml_declaration=True, encoding='utf-8')

    with open('./xml/x1.xml', 'wb') as xml_writer:
        xml_writer.write(obj_xml)