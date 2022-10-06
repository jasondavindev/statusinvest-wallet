from functools import cached_property
import re
from typing import Dict

import requests

from statusinvest.base import STATUS_INVEST_BASE_URL

LOGIN_ENDPOINT = '/account/login'


class Auth:
    def __init__(self, email: str, password: str) -> None:
        self.email = email
        self.password = password
        self.token = None

    def login(self, ) -> str:
        response = requests.post(f'{STATUS_INVEST_BASE_URL}{LOGIN_ENDPOINT}', headers={
            'Content-type': 'application/x-www-form-urlencoded'
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
            'cookie': f'.StatusInvest={self.token};'
        }
