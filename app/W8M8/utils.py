from apiclient.discovery import build
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
import httplib2
import json
import os


def get_oauth_credentials():
    google_json = json.loads(os.environ.get('GOOGLE_SECRET_JSON'))
    scopes = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(google_json, scopes=scopes)
    return credentials


def get_google_sheets_service():
    credentials = get_oauth_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?version=v4')
    service = build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)
    return service


def get_google_drive_service():
    credentials = get_oauth_credentials()
    http = credentials.authorize(httplib2.Http())
    service = build('drive', 'v3', http=http)
    return service


def get_program_master_sheet():
    service = get_google_sheets_service()
    program_master_spreadsheet_id = '1rA5ugdgnVvT0_D9JL_yBAzf1_-_wm3YojhjgDqYGumU'
    return service.spreadsheets().get(spreadsheetId=program_master_spreadsheet_id).execute()


def create_new_workout():
    sheets = get_google_sheets_service()
    drive = get_google_drive_service()
    workout_logs_folder_id = '0B5Z-q6OlTHYsQUw3Mk81bGFsMVU'
    date = datetime.now().date().isoformat()
    time = datetime.now().time().isoformat()

    workout_log_sheet = sheets.spreadsheets().create(body={'properties': {'title': '%s %s' % (date, time)}}).execute()
    drive.files().update(fileId=workout_log_sheet['spreadsheetId'], addParents=workout_logs_folder_id).execute()

    return workout_log_sheet['spreadsheetId']
