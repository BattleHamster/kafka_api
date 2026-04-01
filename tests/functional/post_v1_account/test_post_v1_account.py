from textwrap import indent
from typing import Any
from json import loads
from requests import Response

from helpers.account_helper import AccountHelper
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi
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

    mailhog_configuration = MailhogConfiguration(host='http://185.185.143.231:5025')
    dm_api_configuration = DmApiConfiguration(host='http://185.185.143.231:5051', disable_log=False)

    account = DMApiAccount(configuration=dm_api_configuration)
    mailhog = MailHogApi(configuration=mailhog_configuration)

    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)

    login = 'bhs-test13'
    password ='123456789'
    email = f'{login}@test'

    account_helper.register_new_user(login=login, password=password, email=email)

    account_helper.user_login(login=login, password=password)

    # 1. Регистрация пользователя
    # json_data = {
    #     'login': login,
    #     'email': email,
    #     'password': password,
    # }
    #
    #
    #
    # response = account.account_api.post_v1_account(json_data=json_data)
    # assert response.status_code == 201, f"User hasn't been created {response.json()}"
    #
    # # 2.1 Получить письмо из почтового сервера
    # response = mailhog.mailhog_api.get_api_v2_messages()
    # assert response.status_code == 200, f"Emails hasn't been collected {response.json()}"
    #
    # # 2.2 Получить активационный токен
    # token = get_activation_token_by_login(login, response)
    # assert token is not None, f"User token for user with {login} hasn't been collected"
    #
    #
    # # 2. Активировать пользователя
    # response = account.account_api.put_v1_account_token(token=token)
    # assert response.status_code == 200, f"User activation failed {response.json()}"


    # 3. Авторизоваться
    # response = account.login_api.post_v1_account_login(json_data=json_data)
    # assert response.status_code == 200, f"User authorization failed {response.json()}"







