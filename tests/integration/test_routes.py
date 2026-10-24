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
