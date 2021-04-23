#!/usr/bin/python3

import re
import requests
import string

from bs4 import BeautifulSoup

url_base = "https://lingust.ru/polski/lekcje-polskiego/"

lessons = [
    "lekcja16"
]

r = requests.get(url_base + lessons[0])

soup = BeautifulSoup(r.text, 'html.parser')

regex = re.compile('.*col-xs-6.*')

words = soup.find_all("div", {'class': regex})

pol,rus = [],[]

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

for mixed_word in words:
    clean_re = re.compile('[,\.!?<>]') 
    for word in mixed_word.get_text().split("\n"):
        # cleaned_word = word.replace("\n", "").replace("\r", "").replace("\t", "").replace("-\xa0", "")
        cleaned_word = remove_trash_before(word).replace("\r", "")
        if cleaned_word and len(cleaned_word):
            # TODO: check for - properly
            if cleaned_word[0].lower() in string.ascii_lowercase:
                pol.append(cleaned_word) 
            else:
                rus.append(cleaned_word)

dict = {}
for p,r in zip(pol, rus):
    dict[p] = r

print(dict)

# print(soup.find_all("div", {'class': regex}))
# [print(c.get_text()) for c in words]
# print(r.text)
# print(soup.get_text())


