#!/usr/bin/env python
# coding: utf-8

# <h3><div align='center'>Web Scraping Wikipedia using BeautifulSoup and Python</div></h3>
# 
# <div align='center'>Camille COCHENER</div>

# <div align='justify'>https://secouchermoinsbete.fr/69863-tous-les-chemins-menent-a-la-philosophie-sur-wikipedia : </div>  
#   
# *<div align='center'>« Une théorie veut que n'importe quel article sur Wikipedia pointe au final sur la philosophie. Pour la vérifier, il suffit de cliquer sur le premier lien d'un article Wikipedia qui mène à un autre article et ainsi de suite : à force, on tombe immanquablement sur l'article dédié à la philosophie. »  </div>* 
#   
# <div align='justify'>Ecrivons un programme qui vérifie cette théorie. Ce programme doit renvoyer la "distance" (int) qui sépare un article donné de l'article Philosophie.</div>

# **Importation des librairies**

# In[87]:


import time
import urllib
import bs4
import requests
import quopri
import sys


# **Première fonction qui trouve le premier lien d'un article dans une page wikipedia**

# In[3]:


def find_first_link(url):
    # Récupère le contenu de la page
    response = requests.get(url).text 
    # Parse le contenu dans un objet BeautifulSoup
    soup = bs4.BeautifulSoup(response, "html.parser") 

    # Trouve les 
    links = soup.find(id="mw-content-text").find(class_="mw-parser-output") 

    article_link = None

    for link in links.find_all("p", recursive=False):
        
        if link.find("a", recursive=False):
            article_link = link.find("a", recursive=False).get('href')
            break

    if not article_link:
        return

    # Création de l'url
    first_link = urllib.parse.urljoin('https://fr.wikipedia.org/', article_link)

    return first_link


# **Deuxième fonction pour parcourir les articles trouvés**

# In[1]:


def continuer(curr_links, target_url, max_iter=25):
    
    # Dès qu'on trouve l'article Philosophie, on arrête
    if curr_links[-1] == target_url:
        print("Nous avons atteint l'article Philosophie")
        return False

    # Pour éviter que l'algorithme tourne trop longtemps:
    elif len(curr_links) > max_iter:
        print("La recherche est anormalement longue, on arrête le job!")
        return False
    
    # On vérifie que le lien trouvé n'a pas déjà été analysé sinon l'algorithme va tourner en rond
    elif curr_links[-1] in curr_links[:-1]:
        print("Nous avons déjà rencontré cet article, on arrête là!")
        return False
    else:
        return True


# **Troisième fonction pour trouver l'article philosophie**

# In[2]:


def getting_to_philosophy(my_url): 
    
    curr_lst = [my_url]
    target_url = "https://fr.wikipedia.org/wiki/Philosophie"
    
    # Tant que la fonction continuer nous indique que True, on continue
    while continuer(curr_lst, target_url):
        # Article courant
        print(curr_lst[-1])
        
        # Recherche du premier lien sur cet article
        first_link = find_first_link(curr_lst[-1])
        
        if not first_link:
            print("Nous avons trouvé un lien sans article, on arrête le job!")
            break
            
        curr_lst.append(first_link)
        time.sleep(2) 
    
    print('La distance parcourue entre ces 2 articles est : ' + str(len(curr_lst)-1))


# **Main**

# In[ ]:


def main():
  if len(sys.argv) != 2:
    print('usage: ./ex_philosophie_wiki.py start_url')
    sys.exit(1)

  filename = sys.argv[1]
  getting_to_philosophy(filename)

if __name__ == '__main__':
  main()


# In[ ]:


#my_url = "https://fr.wikipedia.org/wiki/Glace"

