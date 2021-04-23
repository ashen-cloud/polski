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

def remove_spaces_before(st):
    if not len(st): return ""
    garbage_index = 0
    for char in st:
        if char in string.whitespace:
            garbage_index += 1
        else:
            return st[garbage_index:] or ""

for mixed_word in words:
    clean_re = re.compile('[,\.!?<>]') 
    for word in mixed_word.get_text().split("\n"):
        # cleaned_word = word.replace("\n", "").replace("\r", "").replace("\t", "").replace("-\xa0", "")
        cleaned_word = word.replace("\n", "").replace("— ", "")
        cleaned_word = remove_spaces_before(cleaned_word)
        if cleaned_word and len(cleaned_word):
            print("RESULT", cleaned_word[0], cleaned_word[0].lower() in string.ascii_lowercase or cleaned_word[0] == "-")
            if cleaned_word[0].lower() in string.ascii_lowercase or cleaned_word[0] == "-":
                pol.append(cleaned_word) 
            else:
                rus.append(cleaned_word)
 
print(len(pol), len(rus))

# print(soup.find_all("div", {'class': regex}))
# [print(c.get_text()) for c in words]
# print(r.text)
# print(soup.get_text())


