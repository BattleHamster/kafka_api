from textwrap import indent
from typing import Any
from json import loads
from requests import Response

from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True,
            sort_keys=True
        )
    ]
)


def test_post_v1_account():

    account_api = AccountApi(host='http://185.185.143.231:5051')
    login_api = LoginApi(host='http://185.185.143.231:5051')
    mailhog_api = MailhogApi(host='http://185.185.143.231:5025')

    login = 'bhs-test10'
    password ='123456789'
    email = f'{login}@test'

    # 1. Регистрация пользователя
    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }



    response = account_api.post_v1_account(json_data=json_data)
    assert response.status_code == 201, f"User hasn't been created {response.json()}"

    # 2.1 Получить письмо из почтового сервера
    response = mailhog_api.get_api_v2_messages()
    assert response.status_code == 200, f"Emails hasn't been collected {response.json()}"

    # 2.2 Получить активационный токен
    token = get_activation_token_by_login(login, response)
    assert token is not None, f"User token for user with {login} hasn't been collected"


    # 2. Активировать пользователя
    response = account_api.put_v1_account_token(token=token)
    assert response.status_code == 200, f"User activation failed {response.json()}"


    # 3. Авторизоваться
    response = login_api.post_v1_account_login(json_data=json_data)
    assert response.status_code == 200, f"User authorization failed {response.json()}"



def get_activation_token_by_login(login: str, response: Response) -> Any:
    token = None
    for item in response.json()['items']:
        body = item['Content']['Body']
        if body.startswith('{'):
            try:
                user_data = loads(body)

                user_login = user_data['Login']

                if user_login == login:
                    token = user_data['ConfirmationLinkUrl'].split('/')[-1]
                    print(token)

            except (ValueError, KeyError):
                pass
    return token





