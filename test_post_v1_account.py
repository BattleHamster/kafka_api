import pprint

import pytest
import requests
from json import loads


def test_post_v1_account():

    login = 'bhs-test4'
    password ='123456789'
    email = f'{login}@test'

    # # 1. Регистрация пользователя
    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = requests.post('http://185.185.143.231:5051/v1/account', json=json_data)
    print(response.status_code)
    assert response.status_code == 201, f"User hasn't been created {response.json()}"
    # print(response.text)

    # # 2.1 Получить письмо из почтового сервера

    params = {
        'limit': '50',
    }

    response = requests.get('http://185.185.143.231:5025/api/v2/messages', params=params, verify=False)
    print(response.status_code)
    assert response.status_code == 200, f"Email hasn't been collected {response.json()}"
    #print(response.text)

    # 2.2 Получить активационный токен
    #pprint.pprint(response.json())
    token = None
    for item in response.json()['items']:
        body  = item['Content']['Body']
        if body.startswith('{'):
            try:
                user_data = loads(body)

                user_login = user_data['Login']

                if user_login == login:
                    token = user_data['ConfirmationLinkUrl'].split('/')[-1]
                    print(token)

            except (ValueError, KeyError):
                pass

    assert token is not None, f"User token for user with {login} hasn't been collected"



    # 2. Активировать пользователя
    headers = {
        'accept': 'text/plain',
    }

    response = requests.put(f'http://185.185.143.231:5051/v1/account/{token}',
                            headers=headers)
    print(response.status_code)
    assert response.status_code == 200, f"User activation failed {response.json()}"
    # print(response.text)

    # 3. Авторизоваться

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = requests.post('http://185.185.143.231:5051/v1/account/login', json=json_data)
    print(response.status_code)
    assert response.status_code == 200, f"User authorization failed {response.json()}"
    # print(response.text)