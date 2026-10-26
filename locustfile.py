from locust import HttpUser, between, task


class ClubSecretaryUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def index(self):
        self.client.get('/')

    @task(2)
    def public_points_board(self):
        self.client.get('/points')

    @task(2)
    def login_known_email(self):
        self.client.post('/showSummary', data={'email': 'john@simplylift.co'})

    @task(1)
    def login_unknown_email(self):
        self.client.post('/showSummary', data={'email': 'unknown@test.com'})

    @task(1)
    def logout(self):
        self.client.get('/logout')
