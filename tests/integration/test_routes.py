import server


def _purchase(client, places, club='Simply Lift',
              competition='Spring Festival'):
    return client.post('/purchasePlaces', data={
        'club': club,
        'competition': competition,
        'places': places,
    })


def _competition(name='Spring Festival'):
    return next(c for c in server.competitions if c['name'] == name)


def _club(name='Simply Lift'):
    return next(c for c in server.clubs if c['name'] == name)


def test_show_summary_unknown_email_redirects_to_index(client):
    response = client.post('/showSummary', data={'email': 'ghost@nowhere.com'})
    assert response.status_code == 302
    assert response.headers['Location'].endswith('/')


def test_show_summary_known_email_displays_welcome(client):
    response = client.post(
        '/showSummary', data={'email': 'john@simplylift.co'}
    )
    assert response.status_code == 200
    assert b'john@simplylift.co' in response.data


def test_book_unknown_club_does_not_crash(client):
    response = client.get('/book/Spring Festival/Unknown Club')
    assert response.status_code in (302, 200)


def test_book_unknown_competition_does_not_crash(client):
    response = client.get('/book/Unknown Competition/Simply Lift')
    assert response.status_code in (302, 200)


def test_book_valid_competition_and_club_displays_booking(client):
    response = client.get('/book/Spring Festival/Simply Lift')
    assert response.status_code == 200
    assert b'Spring Festival' in response.data


def test_purchase_non_numeric_places_is_rejected(client):
    response = _purchase(client, 'abc')
    assert response.status_code == 200
    assert _competition()['numberOfPlaces'] == '25'


def test_purchase_zero_places_is_rejected(client):
    response = _purchase(client, '0')
    assert response.status_code == 200
    assert _competition()['numberOfPlaces'] == '25'


def test_purchase_negative_places_is_rejected(client):
    response = _purchase(client, '-3')
    assert response.status_code == 200
    assert _competition()['numberOfPlaces'] == '25'


def test_purchase_more_places_than_available_is_rejected(client):
    response = _purchase(client, '30')
    assert response.status_code == 200
    assert _competition()['numberOfPlaces'] == '25'


def test_purchase_more_places_than_club_points_is_rejected(client):
    response = _purchase(client, '10', club='Iron Temple',
                         competition='Fall Classic')
    assert response.status_code == 200
    assert _competition('Fall Classic')['numberOfPlaces'] == '13'
    assert _club('Iron Temple')['points'] == '4'


def test_purchase_more_than_twelve_places_in_one_booking_is_rejected(client):
    response = _purchase(client, '13')
    assert response.status_code == 200
    assert _competition()['numberOfPlaces'] == '25'


def test_cumulative_bookings_cannot_exceed_twelve(client):
    _purchase(client, '8')
    _purchase(client, '5')
    assert int(_competition()['numberOfPlaces']) == 17


def test_cumulative_bookings_up_to_twelve_are_allowed(client):
    _purchase(client, '8')
    _purchase(client, '4')
    assert int(_competition()['numberOfPlaces']) == 13
