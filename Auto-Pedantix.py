import requests
import wikipedia
from tqdm import tqdm
wikipedia.set_lang("fr")


banner = r"""
    _______       _____            ________     _________             __________        
    ___    |___  ___  /______      ___  __ \__________  /_____ _________  /___(_)___  __
    __  /| |  / / /  __/  __ \     __  /_/ /  _ \  __  /_  __ `/_  __ \  __/_  /__  |/_/
    _  ___ / /_/ // /_ / /_/ /     _  ____//  __/ /_/ / / /_/ /_  / / / /_ _  / __>  <  
    /_/  |_\__,_/ \__/ \____/      /_/     \___/\__,_/  \__,_/ /_/ /_/\__/ /_/  /_/|_|  

                Petrus Clovis                                                                    
                Version 1.0
"""

# Fonction pour envoyer une requête à l'API de pédantix
def send_word(word):
    payload = {"word": word, "answer": [word, word, word]}
    response = requests.post(url, headers=headers,json=payload).json()
    if response:
        return response
    else:
        return None

# Dictionnaire des mots trouver sur la page sans doublons
def get_list_words(word, list_words):
    response = send_word(word)
    if response and response['score']:
        for words in response["score"].items():
            word = words[1]
            if isinstance(word, str):
                if word.lower() not in list_words.values():
                    list_words[int(words[0])] = word.lower()
    
    return list_words

# Fonction pour tester le dictionnaire
def test_dictionnary(dictionnary, list_words):
    for word in tqdm(dictionnary):
        get_list_words(word, list_words)
    return list_words


def dico2texte(dico):
    L = ""
    for key in sorted(dico.keys()):
        L = L + " " + dico[key]
    return L

def rechercheWiki(list_words):
    v = wikipedia.search(list_words, results=30, suggestion=True)    
    return v[0]

def affinage_recherche(pages):
    titres = list(set(' '.join(pages).split(' ')))
    mots = [x for x in titres if len(x) > 3]
    bons_mots = test_dictionnary(mots, {})
    bons_mots = dico2texte(bons_mots)
    
    return bons_mots

# Fonction pour afficher les résultats:
def afficher_resultats(res):
    i = 1
    print("\nListe des mots pédantix potentiel aujourd'hui:\n")
    for result in res[0:len(res)//2]:
        print("\033[92m" + f"[+{i}+]" + "\033[0m" + f" {result}\n")
        i += 1

# Programme principal
def main():

    print(banner)

    print("En recherche:")
    dictionnary = open("dictionnary.txt", "r").readlines()
    words = test_dictionnary(dictionnary, {})
    words = dico2texte(words)

    Pages = rechercheWiki(words)
    afficher_resultats(Pages)

    #
    j = 2
    while True:
        q = input("\nVoulez-vous affiner la recherche ? (Y/n)\n")
        if q == "Y" or q == "y":
            print("\nAffinage de la recherche:\n")
            print('\n Itération n°{}:\n'.format(j))
            words = affinage_recherche(Pages)
            Pages = rechercheWiki(words)
            afficher_resultats(Pages)
            j += 1
        else:
            print("\nFin du programme\n")
            break
    


if __name__ == "__main__":

    url = "https://cemantix.certitudes.org/pedantix/score"

    headers = {
        "authority" : "cemantix.certitudes.org",
        "method" : "POST",
        "path" : "/pedantix/score",
        "scheme" : "https",
        "accept" : "*/*",
        "accept-encoding" : "gzip, deflate, br",
        "accept-language" : "fr-FR,fr;q=0.7",
        "content-length" : "43",
        "content-type" : "application/json",
        "origin" : "https://cemantix.certitudes.org",
        "referer" : "https://cemantix.certitudes.org/pedantix",
        "sec-fetch-dest" : "empty",
        "sec-fetch-mode" : "cors",
        "sec-fetch-site" : "same-origin",
        "sec-gpc" : "1",
        "user-agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }

    main()