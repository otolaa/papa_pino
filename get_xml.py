from lxml import etree, objectify
import datetime, json, sys
from help import *


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
                etree.SubElement(offerElem, 'description').text = offer['description'].replace('�','')
            
            etree.SubElement(offerElem, 'picture').text = f"https://xn--80aayufbbb.xn--p1ai{offer['url']}"
            etree.SubElement(offerElem, 'categoryId').text = str(int)

            propsParameters = etree.SubElement(offerElem, 'parameters')
            if len(offer['properties']) > 0:
                '''_@_@_'''
                for prop in offer['properties']:
                    propParameter = etree.SubElement(propsParameters, 'parameter', id=str(get_id()))
                    etree.SubElement(propParameter, 'price').text = prop['prise']
                    etree.SubElement(propParameter, 'description').text = prop['title']

                    unit = offer['unit'] if len(offer['unit']) > 0 else 'шт.'
                    etree.SubElement(propParameter, 'descriptionIndex').text = str(get_description_index(unit))
                
            else:
                propParameter = etree.SubElement(propsParameters, 'parameter', id=str(get_id()))
                
                if offer['prise']:
                    etree.SubElement(propParameter, 'price').text = offer['prise']
                
                try:
                    if offer['weight'] and len(offer['weight']) > 0 and len(offer['weight'][0]) > 0:
                        etree.SubElement(propParameter, 'description').text = str(offer['weight'][0])
                    
                    unit = offer['unit'] if len(offer['unit']) > 0 else 'шт.'
                    etree.SubElement(propParameter, 'descriptionIndex').text = str(get_description_index(unit))
                
                except Exception as e:
                    p(offer['name'], offer['unit'], sys.exc_info()[1])
        
        print(f'\033[32m[+] {int} add: {code_page}\033[0m', end='\n')


    return doc

if __name__ == "__main__":
    ''' save to XML file '''
    doc = get_doc()
    obj_xml = etree.tostring(doc, xml_declaration=True, encoding='utf-8')

    with open('./xml/x1.xml', 'wb') as xml_writer:
        xml_writer.write(obj_xml)