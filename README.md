# GUDLFT - Plateforme de réservation de compétitions (POC)

## 📖 Description

GUDLFT est un Proof of Concept (POC) d'une application web Flask permettant aux secrétaires de clubs sportifs de réserver des places pour des compétitions en utilisant les points accumulés par leur club.

## 🚀 Installation et Lancement

1. Cloner le projet et créer un environnement virtuel :

```bash
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate sur Windows
```

2. Installer les dépendances :

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

3. Lancer l'application :

```bash
flask --app server run
```

L'application est accessible sur http://127.0.0.1:5000.

## 🧪 Qualité et Tests

Le projet a été développé en suivant une approche TDD (Test-Driven Development).

- **Couverture de code** : 91% (Objectif : 60%)
- **Tests** : 23 tests (unitaires, intégration, fonctionnels)
- **Qualité** : 0 erreur Flake8

### Rapports détaillés

Tous les rapports sont disponibles dans le dossier `rapports/` :

- [🧪 Rapport de tests (Pytest)](rapports/rapport-tests.html)
- [📊 Rapport de couverture de code](rapports/couverture-html/index.html)
- [🧹 Rapport de qualité (Flake8)](rapports/flake8-html/index.html)
- [🚀 Rapport de performance (Locust)](rapports/rapport-locust.html)

## 🛡️ Sécurité

- Protection contre l'IDOR (Insecure Direct Object Reference) via l'utilisation de sessions Flask.
- Validation stricte des entrées utilisateur (places > 0, places <= 12, places <= points).
- Clé secrète gérée via variable d'environnement.

## ✨ Fonctionnalités (Phase 2 & Améliorations)

- Tableau public des points (accessible sans connexion).
- Historique des réservations par club.
- Mode sombre (Dark Mode).
- Filtre des compétitions (disponibles / complètes).
- Interface moderne et responsive (Bootstrap 5).
