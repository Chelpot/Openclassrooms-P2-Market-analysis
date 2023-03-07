
# Openclassrooms-P2-Market-analysis

Ceci est le 2nd projet de la formation Openclassrooms. Le code a pour but de visiter les pages du site ***http://books.toscrape.com/*** et de scrapper les informations des différents livres. Enfin, ces données sont stockés dans des fichiers CSV afin d'êtres consultés ulterieurement.

## Prérequis

il est necessaire d'avoir **Python** d'installé sur la machine.

## Installation

Pour que le projet fonctionne il est necessaire de créer un environnement virtuel à la racine du projet :

```
cd Projet2-Openclassrooms
python -m venv env
```

puis activer l'environnement pour ce projet :

**Linux / Mac**
```
source env/bin/activate
```

**Windows**

```
env\Scripts\activate.bat
```

enfin, il faut installer les dépendances du projet :

```
pip install -r requirements.txt
```

## Utilisation

Pour lancer le script il suffit de taper :

```
python main.py
```

## Résultats

A la racine du projet seront générés 2 dossier, l'un contenant les images des livres, et l'autre, nommé output, stockera pour chaque catégorie de livres un fichier CSV contenant les différentes données des livres (Titre / Prix / Description ...)
