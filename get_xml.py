from lxml import etree, objectify
import datetime, json, sys, re
from help import *


def get_modifiers_groups():
    '''*-|-@-@-|-*'''
    m_groups = []
    m_modifiers = []

    for int, cat_item in enumerate(load_json('./json/link.json'), 1):
        code_page = cat_item['href'].replace('/catalog/','').replace('/','').replace('-','_')

        for offer in load_json(f'./json/data_{code_page}_.json'):
            if len(offer['properties']) > 0:                
                for key, prop in enumerate(offer['properties'], 0):
                    if key == 0:
                        continue

                    m_item = {}
                    m_item['gid'] = f"{int}{key}"
                    m_item['name'] = f"{cat_item['name']} {prop['title'].replace(':','').lower()}"
                    type_elem = prop['labels'][0]['type']
                    m_item['type'] = get_type_m(type_elem) # one_one || all_one
                    m_item['minimum'] = '1'
                    m_item['maximum'] = get_maximun_m(type_elem)
                
                    if m_item['gid'] not in get_list_gid(m_groups):                        
                        m_groups.append(m_item)

                        #--@@--#
                        for k_, l_ in enumerate(prop['labels'], 0):
                            m_modifier = {}
                            m_modifier['gid'] = m_item['gid']
                            m_modifier['name'] = l_['title']
                            m_modifier['price'] = l_['price']
                            m_modifier['mid'] = f"{m_item['gid']}{k_}"

                            m_modifiers.append(m_modifier)

    return {'groups':m_groups, 'modifiers':m_modifiers}

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
    
    modifiersGroups = etree.SubElement(pageElementShop, 'modifiersGroups')
    gg = get_modifiers_groups()
    for m_group in gg['groups']:
        modifiersGroup = etree.SubElement(modifiersGroups, 'modifiersGroup', id = m_group['gid'])
        etree.SubElement(modifiersGroup, 'name').text = m_group['name']
        etree.SubElement(modifiersGroup, 'type').text = m_group['type']
        etree.SubElement(modifiersGroup, 'minimum').text = m_group['minimum']
        etree.SubElement(modifiersGroup, 'maximum').text = m_group['maximum']
    
    modifierList = etree.SubElement(pageElementShop, 'modifiers')
    for m_modifier in gg['modifiers']:
        # p(m_modifier)
        modifierElem = etree.SubElement(modifierList, 'modifier', id=str(m_modifier['mid']))
        etree.SubElement(modifierElem, 'name').text = m_modifier['name']
        etree.SubElement(modifierElem, 'price').text = f"+{m_modifier['price']}"
        etree.SubElement(modifierElem, 'modifiersGroupId').text = m_modifier['gid']

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

            if len(offer['properties']) > 0:
                for k_, p_ in enumerate(offer['properties'], 0):
                    if k_ == 0:
                        continue
                    '''@@'''
                    mGroupsIds = etree.SubElement(offerElem, 'modifiersGroupsIds')
                    etree.SubElement(mGroupsIds, 'modifiersGroupId').text = f"{int}{k_}"

            propsParameters = etree.SubElement(offerElem, 'parameters')
            if len(offer['properties']) > 0:
                '''_@_@_'''
                for key, prop in enumerate(offer['properties'], 1):
                    p_title =  prop['title']
                    if p_title == 'Дополнительно:' or key > 1:
                        continue

                    for p_label in prop['labels']:
                        propParameter = etree.SubElement(propsParameters, 'parameter', id=str(get_id()))
                        etree.SubElement(propParameter, 'price').text = p_label['price']
                        etree.SubElement(propParameter, 'description').text = p_label['title']
                        
                        unit = offer['unit'] if len(offer['unit']) > 0 else 'шт'
                        unit_text = re.sub(r"\d+", "", p_label['title']).replace('.','').strip()
                        '''_@_@_@_'''
                        val_unit = get_description_index(unit_text)
                        unit = val_unit if len(val_unit) > 0 else get_description_index(unit)

                        etree.SubElement(propParameter, 'descriptionIndex').text = unit
                
            else:
                propParameter = etree.SubElement(propsParameters, 'parameter', id=str(get_id()))
                
                if offer['prise']:
                    etree.SubElement(propParameter, 'price').text = offer['prise']
                
                try:
                    if offer['weight'] and len(offer['weight']) > 0 and len(offer['weight'][0]) > 0:
                        etree.SubElement(propParameter, 'description').text = str(offer['weight'][0])
                    
                    unit = offer['unit'] if len(offer['unit']) > 0 else 'шт'
                    etree.SubElement(propParameter, 'descriptionIndex').text = get_description_index(unit)
                
                except Exception as e:
                    pcolor(f"{offer['name']} / {offer['unit']} / {sys.exc_info()[1]}", 1)
        
        pcolor(f'[+] {int} add: {code_page}')


    return doc

if __name__ == "__main__":
    ''' save to XML file '''
    doc = get_doc()
    obj_xml = etree.tostring(doc, xml_declaration=True, encoding='utf-8')

    with open('./xml/x1.xml', 'wb') as xml_writer:
        xml_writer.write(obj_xml)