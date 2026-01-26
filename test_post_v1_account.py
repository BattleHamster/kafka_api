import pprint

import pytest
import requests


def test_post_v1_account():

    login = 'bhs-test'
    password ='123456789'
    email = f'{login}@test'

    # 1. Регистрация пользователя
    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = requests.post('http://185.185.143.231:5051/v1/account', json=json_data)
    # 2.1 Получить письмо из почтового сервера
    print(response.status_code)
    print(response.text)

    params = {
        'limit': '50',
    }

    response = requests.get('http://185.185.143.231:5025/api/v2/messages', params=params, verify=False)
    print(response.status_code)
    print(response.text)

    # 2.2 Получить активационный токен

    # 2. Активировать пользователя
    headers = {
        'accept': 'text/plain',
    }

    response = requests.put('http://185.185.143.231:5051/v1/account/76b12015-71a8-4f17-9e8c-b3a7cd7bc569',
                            headers=headers)
    print(response.status_code)
    print(response.text)

    # 3. Авторизоваться

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = requests.post('http://185.185.143.231:5051/v1/account/login', json=json_data)
    print(response.status_code)
    print(response.text)
    pass
