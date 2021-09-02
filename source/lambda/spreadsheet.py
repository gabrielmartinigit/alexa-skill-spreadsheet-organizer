# -*- coding: utf-8 -*-

from authenticator import Authenticator
from googleapiclient.discovery import build


class Spreadsheet:
    def __init__(self, spreadsheet_id, spreadsheet_range):
        self.spreadsheet_range = spreadsheet_range
        self.spreadsheet_id = spreadsheet_id
        self.__remote_sheet_client = self.__create_remote_spreadsheet_client()

    #TODO: Refactor this method to Authenticator Factory
    def __create_remote_spreadsheet_client(self):
        service = build(
            'sheets',
            'v4',
            credentials=Authenticator().credentials
        )

        sheet = service.spreadsheets()

        return sheet

    def get_rows(self):
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
        # Get updated rows
        rows = self.get_rows()
        return rows[-1]

    def create_row(self, *args):
        # Get all parameters as cell value
        values = []
        for value in args:
            values.append(value)

        row = {
            'values': [values]
        }

        self.__remote_sheet_client.values().append(
            spreadsheetId=self.spreadsheet_id,
            range=self.spreadsheet_range,
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body=row).execute()

        return
