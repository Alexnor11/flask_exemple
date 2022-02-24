import requests

HOST = 'http://127.0.0.1:8080'

resp = requests.get(f'{HOST}/health')
print(resp.status_code)

resp = requests.get(f'{HOST}/users/1')
print(resp.status_code)
print(resp.text)


resp = requests.post(f'{HOST}/users/', json={
    'username': 'user_1',
    'email': 'user@user.ru',
    # 'password': '12345',

})
print(resp.status_code)
print(resp.text)
