#!/usr/bin/python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from json import loads
from urllib.request import urlopen
from urllib.parse import urlencode, unquote
import pandas as pd
import re
from flask_caching import Cache
import ssl

cache = Cache()

def getJSON(page):
    params = urlencode({
      'format': 'json',  
      'action': 'parse',  
      'prop': 'text',  
      'redirects': 'true',  
      'page': page})
    API = "https://fr.wikipedia.org/w/api.php" 
    # désactivation de la vérification SSL pour contourner un problème sur le
    # serveur d'évaluation -- ne pas modifier
    gcontext = ssl.SSLContext()
    response = urlopen(API + "?" + params, context=gcontext)
    return response.read().decode('utf-8')


def getRawPage(page):
    parsed = loads(getJSON(page))
    try:
        title = parsed['parse']['title']  
        content = parsed['parse']['text']['*']  
        return title, content
    except KeyError:
        # La page demandée n'existe pas
        print('La page demandée n\'existe pas')
        return None, None

#@cache.memoize()
def getPage(page):
    title, html = getRawPage(page)
    try : 
        soup = BeautifulSoup(html, 'html.parser')
        p_soup = soup.div.find_all('p', recursive=False)
        link = []
        for p in p_soup:
            for a in p.find_all(href=re.compile('/wiki/')):
                link.append(a.get('href'))
        link = [unquote(re.sub('/wiki/','', x)) for x in link]  # Traiter les caractères non-ASCII
        link = [re.sub('#(.)+','', x) for x in link] # Retirer les fragments de liens
        link = [re.sub('_',' ', x) for x in link] # Remplacer les "_" par " "
        link = [x for x in link if re.search('(.)+:(.)', x) is None] # Ne pas prendre en compte les liens vers des pages ext
        link = pd.Series(link).drop_duplicates().tolist() # Supprimer les doublons en gardant l'ordre
        link = link[:10]
        return title, link
    except TypeError:
        return None, []


    
if __name__ == '__main__':
    # Ce code est exécuté lorsque l'on exécute le fichier
    print("Ça fonctionne !")
    #getJSON('Liverpool')
    
    # Voici des idées pour tester vos fonctions :
    #print(getJSON("Utilisateur:A3nm/INF344"))
    #test("Utilisateur:A3nm/INF344")
    #print(getRawPage("Utilisateur:A3nm/INF344"))
    print(getPage("Utilisateur:A3nm/INF344"))
    #print(getPage("Philosophie"))
    # print(getRawPage("Histoire"))

