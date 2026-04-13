import time
from json import loads
from typing import Any

from requests import Response
from services.api_mailhog import MailHogApi
from services.dm_api_account import DMApiAccount

from retrying import retry

def retry_if_result_none(result):
    """Return True if we should retry (in this case when result is None), False otherwise"""
    return result is None

def retrier(
        function
        ):
    def wrapper(
            *args,
            **kwargs
            ):

        token = None
        counter = 0
        while token is None:
            print(f"Try to get activation token № {counter}")
            token = function(*args, **kwargs)
            counter +=1
            if counter == 5:
                raise AssertionError("Too many tries to get activation token")
            if token:
                return token

            time.sleep(1)
    return wrapper


class AccountHelper:
    def __init__(
            self,
            dm_account_api: DMApiAccount,
            mailhog: MailHogApi
    ):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

    def auth_client(self, login, password):
        response = self.dm_account_api.login_api.post_v1_account_login(
            json_data={'login': login, 'password': password}
        )

        token = {
            "x-dm-auth-token": response.headers["x-dm-auth-token"]
        }

        self.dm_account_api.account_api.set_headers(token)
        self.dm_account_api.login_api.set_headers(token)

    def register_new_user(
            self,
            login: str,
            password: str,
            email: str
    ):
        json_data = {
            'login': login,
            'email': email,
            'password': password,
        }

        response = self.dm_account_api.account_api.post_v1_account(json_data=json_data)
        assert response.status_code == 201, f"User hasn't been created {response.json()}"
        # response = self.mailhog.mailhog_api.get_api_v2_messages()
        # assert response.status_code == 200, f"Emails hasn't been collected {response.json()}"
        token = self.get_activation_token_by_login(login=login)
        assert token is not None, f"User token for user with {login} hasn't been collected"
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, f"User activation failed {response.json()}"

        return response

    def user_login(
            self,
            login: str,
            password: str,
            remember_me: bool = True
            ):
        json_data = {
            'login': login,
            'password': password,
            'rememberMe': True,
        }
        response = self.dm_account_api.login_api.post_v1_account_login(json_data=json_data)
        assert response.status_code == 200, f"User authorization failed {response.json()}"
        return response



    @retry(stop_max_attempt_number=5, retry_on_result=retry_if_result_none, wait_fixed=1000)
    def get_activation_token_by_login(
            self,
            login: str
            ) -> Any:
        token = None

        response = self.mailhog.mailhog_api.get_api_v2_messages()
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
