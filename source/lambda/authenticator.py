# -*- coding: utf-8 -*-

import os
from google.oauth2.credentials import Credentials as client_id
from google.oauth2.service_account import Credentials as service_account
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow


class Authenticator:
    def __init__(self):
        self.scopes = [
            'https://www.googleapis.com/auth/spreadsheets.readonly',
            'https://www.googleapis.com/auth/spreadsheets'
        ]
        self.credentials = self.__get_credentials_service()

    def __get_credentials_service(self):
        creds = service_account.from_service_account_file(
            'service_account.json')

        return creds

    def __get_credentials_oauth(self):
        creds = None

        if os.path.exists('token.json'):
            creds = client_id.from_authorized_user_file(
                'token.json', self.scopes)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.scopes)
                creds = flow.run_local_server(port=0)

            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        return creds
