import json
import random

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

def get_description_index(unit):
    ''' return index '''
    
    nids = {
        'ед.':0, 
        'гр.':1, 'гр':1, 
        'кг.':2, 
        'мл.':3, 
        'л.':4, 'л':4,
        'см.':5, 'см':5,
        'м.':6,
        'мин.':7,
        'ч.':8,
        'шт.':9, 'штук.':9,
        'порц.':10,
    }

    return nids[unit] if nids[unit] else ''

def get_id():
    return random.randrange(1992, 3999)