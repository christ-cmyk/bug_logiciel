# GUDLFT - Plateforme de réservation de compétitions (POC)

Ce projet est un Proof of Concept (POC) d'une application web permettant aux secrétaires de clubs de réserver des places pour des compétitions sportives en utilisant les points accumulés par leur club.

## Prérequis
- Python 3.x
- Flask

## Installation
1. Créer un environnement virtuel : `python -m venv venv`
2. Activer l'environnement : `venv\Scripts\activate` (Windows) ou `source venv/bin/activate` (Mac/Linux)
3. Installer les dépendances : `pip install -r requirements.txt` et `pip install -r requirements-dev.txt`

## Lancement de l'application
`flask --app server run`
L'application sera accessible à l'adresse : http://127.0.0.1:5000

## Lancement des tests
Pour vérifier la couverture de code :
`pytest --cov=server --cov-report=term-missing --cov-report=html`
Le rapport HTML sera généré dans le dossier `htmlcov/`.

## Tests de performance (Locust)
Pour lancer les tests avec 6 utilisateurs simultanés :
`locust -f locustfile.py --headless -u 6 -r 1 --run-time 1m --host http://127.0.0.1:5000`

## Structure du projet
- `server.py` : Application Flask et logique métier
- `templates/` : Fichiers HTML (Jinja2)
- `tests/` : Tests unitaires, d'intégration et fonctionnels
- `rapports/` : Rapports QA (tests, performances, flake8)
