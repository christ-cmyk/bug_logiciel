def _purchase(client, places, club='Simply Lift', competition='Spring Festival'):
    with client.session_transaction() as sess:
        sess['club'] = club
    return client.post('/purchasePlaces', data={
        'club': club,
        'competition': competition,
        'places': places,
    })


def test_welcome_contains_booking_history_section(client):
    """La page welcome doit contenir la section 'Mes réservations'."""
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
    assert response.status_code == 200
    assert 'Mes réservations'.encode('utf-8') in response.data


def test_welcome_shows_no_bookings_message_when_empty(client):
    """Sans réservation, le message 'Aucune réservation' doit s'afficher."""
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
    assert response.status_code == 200
    assert 'Aucune réservation'.encode('utf-8') in response.data


def test_booking_appears_in_history_after_purchase(client):
    """Après un achat, la compétition réservée doit apparaître dans l'historique."""
    _purchase(client, '3')
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
    assert response.status_code == 200
    # La compétition réservée doit être visible
    assert b'Spring Festival' in response.data


def test_club_bookings_dict_passed_to_template(client):
    """Vérifie que club_bookings est bien transmis au template welcome."""
    _purchase(client, '5')
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
    assert response.status_code == 200
    assert b'Spring Festival' in response.data
    # La quantité doit aussi être visible
    assert b'5' in response.data
