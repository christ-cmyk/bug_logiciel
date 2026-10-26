# GUDLFT - Plateforme de réservation

## Description
POC Flask + JSON pour la réservation de places de compétition par club avec gestion des points.

## Installation
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Lancement
```bash
$env:FLASK_APP="server.py"
$env:SECRET_KEY="dev-local"
python -m flask --app server run --debug
```

## Tests
```bash
pytest --cov=server
```

## Performance
```bash
locust -f locustfile.py --headless -u 6 -r 1 --run-time 1m --host http://127.0.0.1:5000
```
