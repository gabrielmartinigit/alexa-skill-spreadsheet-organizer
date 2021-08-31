from authenticator import Authenticator
from googleapiclient.discovery import build


class Spreadsheet:
    def __init__(self, spreadsheet_id, spreadsheet_range):
        self.spreadsheet_range = spreadsheet_range
        self.spreadsheet_id = spreadsheet_id
        self.__remote_sheet = self.__get_remote_spreadsheet()
        self.rows = self.__rows()

    def __get_remote_spreadsheet(self):
        service = build(
            'sheets', 'v4',
            credentials=Authenticator().credentials
        )

        sheet = service.spreadsheets()

        return sheet

    def __rows(self):
        rows = None

        result = self.__remote_sheet.values().get(
            spreadsheetId=self.spreadsheet_id,
            range=self.spreadsheet_range
        ).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
        else:
            rows = values

        return rows

    # TODO: Return last row
    def get_last_row(self):
        pass

    # TODO: Append new row
    def create_row(self):
        pass
