import json
import os
from flask import (Flask, render_template, request, redirect,
                   flash, url_for, session)


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


def find_club_by_email(clubs_list, email):
    for club in clubs_list:
        if club['email'] == email:
            return club
    return None


def find_club_by_name(clubs_list, name):
    for club in clubs_list:
        if club['name'] == name:
            return club
    return None


def find_competition(competitions_list, name):
    for competition in competitions_list:
        if competition['name'] == name:
            return competition
    return None


def validate_purchase(club, competition, places, already_booked=0):
    if places is None or places <= 0:
        return False, 'Le nombre de places doit être un entier strictement positif.'
    if places > MAX_PLACES_PER_BOOKING:
        return False, 'Vous ne pouvez pas réserver plus de 12 places par réservation.'
    if already_booked + places > MAX_PLACES_PER_BOOKING:
        return False, ('Vous ne pouvez pas dépasser 12 places au total '
                       'pour une même compétition.')
    if places > int(competition['numberOfPlaces']):
        return False, 'Il ne reste pas assez de places dans cette compétition.'
    if places > int(club['points']):
        return False, 'Vous ne disposez pas d\'assez de points pour cette réservation.'
    return True, 'ok'


MAX_PLACES_PER_BOOKING = 12

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-fallback')

competitions = loadCompetitions()
clubs = loadClubs()
bookings = {}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    club = find_club_by_email(clubs, request.form.get('email', ''))
    if club is None:
        flash("Adresse email inconnue. Veuillez réessayer.")
        return redirect(url_for('index'))
    session['club'] = club['name']
    session['club_email'] = club['email']
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = find_club_by_name(clubs, club)
    foundCompetition = find_competition(competitions, competition)
    if foundClub is None or foundCompetition is None:
        flash("Club ou compétition introuvable.")
        return redirect(url_for('index'))
    session_club = session.get('club')
    if session_club is None:
        flash("Veuillez vous connecter.")
        return redirect(url_for('index'))
    if session_club != foundClub['name']:
        flash("Accès non autorisé à cette réservation.")
        return redirect(url_for('index'))
    return render_template('booking.html', club=foundClub, competition=foundCompetition)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = find_competition(
        competitions, request.form.get('competition', ''))
    club = find_club_by_name(clubs, request.form.get('club', ''))
    if club is None or competition is None:
        flash("Club ou compétition introuvable.")
        return redirect(url_for('index'))
    session_club = session.get('club')
    if session_club is None or session_club != club['name']:
        flash("Accès non autorisé.")
        return redirect(url_for('index'))
    placesRequired = request.form.get('places', type=int)
    key = (club['name'], competition['name'])
    already_booked = bookings.get(key, 0)
    ok, message = validate_purchase(
        club, competition, placesRequired, already_booked)
    if not ok:
        flash(message)
        return render_template('welcome.html', club=club,
                               competitions=competitions)
    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
    club['points'] = int(club['points']) - placesRequired
    bookings[key] = already_booked + placesRequired
    flash(f'Reservation reussie : {placesRequired} place(s) reservee(s).')
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/points')


@app.route('/clubs-points')
def points():
    return render_template('points.html', clubs=clubs)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

