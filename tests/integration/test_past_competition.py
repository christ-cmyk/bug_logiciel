from datetime import datetime, timedelta

import server

PAST_DATE = '%Y-%m-%d %H:%M:%S'


def _add_past_competition():
    past_competition = {
        'name': 'Past Competition',
        'date': (datetime.now() - timedelta(days=1)).strftime(PAST_DATE),
        'numberOfPlaces': '10',
    }
    server.competitions.append(past_competition)
    return past_competition


def _club(name='Simply Lift'):
    return next(club for club in server.clubs if club['name'] == name)


def test_purchase_past_competition_is_rejected(client):
    _add_past_competition()
    with client.session_transaction() as sess:
        sess['club'] = 'Simply Lift'

    response = client.post('/purchasePlaces', data={
        'club': 'Simply Lift',
        'competition': 'Past Competition',
        'places': '2',
    })

    assert response.status_code == 200
    assert 'Cette compétition est déjà terminée.'.encode('utf-8') in response.data
    competition = server.find_competition(
        server.competitions, 'Past Competition')
    assert competition['numberOfPlaces'] == '10'
    assert _club()['points'] == '13'


def test_book_past_competition_is_blocked(client):
    _add_past_competition()
    with client.session_transaction() as sess:
        sess['club'] = 'Simply Lift'

    response = client.get('/book/Past Competition/Simply Lift')

    assert response.status_code == 302
    assert response.headers['Location'].endswith('/')
    follow_up = client.get('/')
    assert 'Cette compétition est déjà terminée.'.encode('utf-8') in follow_up.data
