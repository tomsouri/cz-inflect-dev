#!/usr/bin/env python3.9

import requests
import json
import itertools

# Pravdepodobne vubec nesklonuje nezname tvary.
# Napsat Neverilove, jakou strategii pouziva.

# Dle clanku na https://www.researchgate.net/publication/301887499_Declension_of_Czech_Noun_Phrases
# str. 4, pouzivaji majka generator, ktery je zalozen na slovniku.

def one_form(lemma, case, num):
    url = f"https://nlp.fi.muni.cz/languageservices/service.py?call=declension&lang=cs&output=json&text={lemma}&c1=c1&c2=c{case}&n=n{num}"
    response = requests.get(url)
    response.encoding='utf8'
    res = json.loads(response.text)["response"]
    return res

def decline(lemma):
    forms = [[one_form(lemma, case, num) for case in range(1,8)] for num in ["S", "P"]]
    #print(forms)
    forms = itertools.chain(forms)
    
    return list(forms)

def inflect(lemma):
    url = f"https://nlp.fi.muni.cz/languageservices/service.py?call=gen&lang=cs&output=json&text={lemma}"
    response = requests.get(url)
    response.encoding='utf8'
    #print(response.text)
    res = json.loads(response.text)["forms"]

    return res

while True:
    lemma = input("Enter lemma to be declined:")
    res= decline(lemma)
    print(res)
    res= inflect(lemma)
    print(res)