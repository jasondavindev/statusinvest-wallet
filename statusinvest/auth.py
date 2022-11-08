import os
import re
from functools import cached_property
from typing import Dict

import requests

from statusinvest.base import STATUS_INVEST_BASE_URL
from statusinvest.utils.singleton import SingletonMeta

LOGIN_ENDPOINT = '/account/login'
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'


class Auth(metaclass=SingletonMeta):
    def __init__(self, email: str, password: str, token: str = None) -> None:
        self.email = email
        self.password = password
        self.token = token

    def login(self) -> str:
        if self.token:
            return self.token

        response = requests.post(f'{STATUS_INVEST_BASE_URL}{LOGIN_ENDPOINT}', headers={
            'Content-type': 'application/x-www-form-urlencoded',
            'user-agent': USER_AGENT,
        }, data={
            'Email': self.email,
            'Password': self.password,
        })

        headers = response.headers
        cookies_header = headers['set-cookie'].split(';')

        login_token_cookie = [
            header for header in cookies_header if '.StatusInvest' in header
        ]
        login_token_cookie = login_token_cookie[0]

        token = re.search('StatusInvest=(.*)', login_token_cookie).group(1)

        self.token = token

        return token

    @cached_property
    def auth_headers(self) -> Dict[str, str]:
        return {
            'cookie': f'.StatusInvest={self.token};',
            'user-agent': USER_AGENT,
        }

    @staticmethod
    def from_env():
        auth = Auth(os.getenv('EMAIL'), os.getenv('PASSWORD'), os.getenv('TOKEN'))
        auth.login()
        return auth
