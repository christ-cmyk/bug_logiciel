import json
import os
from datetime import datetime
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

MONTHS_FR = {
    1: 'Janvier', 2: 'Février', 3: 'Mars', 4: 'Avril',
    5: 'Mai', 6: 'Juin', 7: 'Juillet', 8: 'Août',
    9: 'Septembre', 10: 'Octobre', 11: 'Novembre', 12: 'Décembre'
}


@app.template_filter('format_date')
def format_date_filter(date_str):
    try:
        dt = datetime.strptime(str(date_str), '%Y-%m-%d %H:%M:%S')
        return f"{dt.day} {MONTHS_FR[dt.month]} {dt.year} à {dt.hour:02d}h{dt.minute:02d}"
    except (ValueError, KeyError):
        return date_str


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    club = find_club_by_email(clubs, request.form.get('email', ''))
    if club is None:
        flash("Adresse email inconnue. Veuillez réessayer.", 'danger')
        return redirect(url_for('index'))
    session['club'] = club['name']
    session['club_email'] = club['email']
    club_bookings = {
        k[1]: v for k, v in bookings.items() if k[0] == club['name']
    }
    return render_template('welcome.html', club=club,
                           competitions=competitions,
                           club_bookings=club_bookings)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = find_club_by_name(clubs, club)
    foundCompetition = find_competition(competitions, competition)
    if foundClub is None or foundCompetition is None:
        flash("Club ou compétition introuvable.", 'danger')
        return redirect(url_for('index'))
    session_club = session.get('club')
    if session_club is None:
        flash("Veuillez vous connecter.", 'danger')
        return redirect(url_for('index'))
    if session_club != foundClub['name']:
        flash("Accès non autorisé à cette réservation.", 'danger')
        return redirect(url_for('index'))
    return render_template('booking.html', club=foundClub,
                           competition=foundCompetition)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = find_competition(
        competitions, request.form.get('competition', ''))
    club = find_club_by_name(clubs, request.form.get('club', ''))
    if club is None or competition is None:
        flash("Club ou compétition introuvable.", 'danger')
        return redirect(url_for('index'))
    session_club = session.get('club')
    if session_club is None or session_club != club['name']:
        flash("Accès non autorisé.", 'danger')
        return redirect(url_for('index'))
    placesRequired = request.form.get('places', type=int)
    key = (club['name'], competition['name'])
    already_booked = bookings.get(key, 0)
    ok, message = validate_purchase(
        club, competition, placesRequired, already_booked)
    if not ok:
        flash(message, 'danger')
        club_bookings = {
            k[1]: v for k, v in bookings.items() if k[0] == club['name']
        }
        return render_template('welcome.html', club=club,
                               competitions=competitions,
                               club_bookings=club_bookings)
    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
    club['points'] = int(club['points']) - placesRequired
    bookings[key] = already_booked + placesRequired
    flash(f'Reservation reussie : {placesRequired} place(s) reservee(s).', 'success')
    club_bookings = {
        k[1]: v for k, v in bookings.items() if k[0] == club['name']
    }
    return render_template('welcome.html', club=club,
                           competitions=competitions,
                           club_bookings=club_bookings)


@app.route('/points')
def points():
    return render_template('points.html', clubs=clubs)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
