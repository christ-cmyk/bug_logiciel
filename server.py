import json
from flask import Flask,render_template,request,redirect,flash,url_for


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


def validate_purchase(club, competition, places):
    if places is None or places <= 0:
        return False, 'Le nombre de places doit être un entier strictement positif.'
    if places > int(competition['numberOfPlaces']):
        return False, 'Il ne reste pas assez de places dans cette compétition.'
    if places > int(club['points']):
        return False, 'Vous ne disposez pas d\'assez de points pour cette réservation.'
    return True, 'ok'


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    club = find_club_by_email(clubs, request.form.get('email', ''))
    if club is None:
        flash("Adresse email inconnue. Veuillez réessayer.")
        return redirect(url_for('index'))
    return render_template('welcome.html',club=club,competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = find_club_by_name(clubs, club)
    foundCompetition = find_competition(competitions, competition)
    if foundClub is None or foundCompetition is None:
        flash("Club ou compétition introuvable.")
        return redirect(url_for('index'))
    return render_template('booking.html',club=foundClub,competition=foundCompetition)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = find_competition(
        competitions, request.form.get('competition', ''))
    club = find_club_by_name(clubs, request.form.get('club', ''))
    if club is None or competition is None:
        flash("Club ou compétition introuvable.")
        return redirect(url_for('index'))
    placesRequired = request.form.get('places', type=int)
    ok, message = validate_purchase(club, competition, placesRequired)
    if not ok:
        flash(message)
        return render_template('welcome.html', club=club,
                               competitions=competitions)
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))