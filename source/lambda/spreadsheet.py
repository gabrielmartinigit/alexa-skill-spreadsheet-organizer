# -*- coding: utf-8 -*-

from authenticator import Authenticator
from googleapiclient.discovery import build


class Spreadsheet:
    def __init__(self, spreadsheet_id, spreadsheet_range, api_key=None):
        self.spreadsheet_range = spreadsheet_range
        self.spreadsheet_id = spreadsheet_id
        self.api_key = api_key  # API Key for public spreadsheets
        self.__remote_sheet_client = self.__create_remote_spreadsheet_client()
        self.rows = self.__get_rows()

    def __create_remote_spreadsheet_client(self):
        # If spreadsheet is public create client with API Key
        if getattr(self, 'api_key'):
            service = build(
                'sheets', 'v4',
                developerKey=self.api_key
            )
        else:
            service = build(
                'sheets', 'v4',
                credentials=Authenticator().credentials
            )

        sheet = service.spreadsheets()

        return sheet

    def __get_rows(self):
        rows = None

        result = self.__remote_sheet_client.values().get(
            spreadsheetId=self.spreadsheet_id,
            range=self.spreadsheet_range
        ).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
        else:
            rows = values

        return rows

    def get_last_row(self):
        return self.rows[-1]

    # TODO: Append new row
    def create_row(self):
        pass
