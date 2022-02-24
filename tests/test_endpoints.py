import requests

HOST = 'http://127.0.0.1:8080'


class TestEndpoint:
    def test_main_url_404(self):
        assert requests.get(HOST).status_code == 404

    def test_health(self):
        response = requests.get(f'{HOST}/health')
        assert response.status_code == 200
        assert response.json()['status'] == 'OK'

