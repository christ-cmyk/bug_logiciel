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
