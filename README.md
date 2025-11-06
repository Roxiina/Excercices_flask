# Flask Blog Application

Une application Flask complète avec des exercices de gestion de base de données, templates, et blueprints.

## Description

Ce projet contient 15 exercices progressifs couvrant:
- Routes et templates Flask
- Gestion des formulaires
- Bases de données SQLite et SQLAlchemy
- Blueprints
- Gestion des utilisateurs
- API JSON

## Structure du Projet

```
Flask/
├── app.py                 # Application principale Flask
├── blog/
│   ├── __init__.py        # Initialisation du blueprint blog
│   └── routes.py          # Routes du blueprint blog
├── static/
│   └── style.css          # Feuille de styles
├── templates/
│   ├── base.html          # Template de base (héritage)
│   ├── index.html         # Page d'accueil
│   ├── contact.html       # Page de contact
│   ├── users.html         # Gestion des utilisateurs
│   ├── articles.html      # Liste des articles
│   ├── age.html           # Calcul d'âge
│   └── 404.html           # Page d'erreur
├── instance/              # Dossier des données (non versionné)
├── requirements.txt       # Dépendances Python
└── README.md              # Ce fichier
```

## Installation

1. Créer un environnement virtuel:
```bash
python -m venv venv
venv\Scripts\activate
```

2. Installer les dépendances:
```bash
pip install -r requirements.txt
```

## Utilisation

Lancer l'application:
```bash
python app.py
```

L'application sera disponible à `http://localhost:5000`

## Dépendances

- **Flask** - Framework web minimaliste
- **Flask-SQLAlchemy** - ORM SQLAlchemy pour Flask
- **SQLite3** - Base de données légère (incluse dans Python)

Voir `requirements.txt` pour la version complète.

## Exercices Couverts

- **Exo 1-2**: Routes de base et templates
- **Exo 3-8**: Gestion des formulaires et requêtes POST
- **Exo 9**: Base de données SQLite
- **Exo 10-13**: Modèles SQLAlchemy
- **Exo 14-15**: Blueprints et organisation avancée

## Auteur

Flavie

## Licence

MIT
