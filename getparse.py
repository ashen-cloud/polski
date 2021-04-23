#!/usr/bin/python3

import re
import requests
import string
import sys

from bs4 import BeautifulSoup

url_base = "https://lingust.ru/polski/lekcje-polskiego/"

def remove_trash_before(st):
    if not len(st): return ""
    ret = ""
    garbage_index = 0
    for char in st:
        if char in string.whitespace:
            garbage_index += 1
        else:
            ret = st[garbage_index:] or ""
            break

    if "— " in ret[:2]:
        ret = ret[2:]
    return ret    

def parse_page(l_num):
    r = requests.get(url_base + f"lekcja{l_num}")
    
    soup = BeautifulSoup(r.text, 'html.parser')
    
    regex = re.compile('.*col-xs-6.*')
    
    words = soup.find_all("div", {'class': regex})
    
    pol,rus = [],[]
    
    for mixed_word in words:
        clean_re = re.compile('[,\.!?<>]') 
        for word in mixed_word.get_text().split("\n"):
            cleaned_word = remove_trash_before(word).replace("\r", "")
            if cleaned_word and len(cleaned_word):
                if cleaned_word[0].lower() in string.ascii_lowercase:
                    pol.append(cleaned_word) 
                else:
                    rus.append(cleaned_word)
    return zip(pol, rus)

def get_all_parsed(c_arg):
    lesson_number = 0
    if len(c_arg) >= 2:
        lesson_number = int(c_arg[1])
    
    prt = lambda ln: [print(p,r) for p,r in parse_page(ln)]
    if lesson_number:
        prt(lesson_number)
    else:
        for i in range(1, 28):
            prt(i)

get_all_parsed(sys.argv)
