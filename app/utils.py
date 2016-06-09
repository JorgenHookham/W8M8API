from apiclient.discovery import build
from datetime import datetime
from django.conf import settings
from oauth2client.service_account import ServiceAccountCredentials
import httplib2
import json


def get_oauth_credentials():
    google_json = json.loads(settings.GOOGLE_SECRET_JSON)
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
    return service.spreadsheets().get(spreadsheetId=settings.MASTER_PROGRAM_SHEET_ID).execute()


def get_workout_template_sheets():
    master_sheet = get_program_master_sheet()
    workout_sheets = filter(lambda x: '#W' in x['properties']['title'], master_sheet['sheets'])
    return map(lambda x: (x['properties']['sheetId'], x['properties']['title']), workout_sheets)


def create_new_workout():
    sheets = get_google_sheets_service()
    drive = get_google_drive_service()
    date = datetime.now().date().isoformat()
    time = datetime.now().time().isoformat()

    workout_log_sheet = sheets.spreadsheets().create(body={'properties': {'title': '%s %s' % (date, time)}}).execute()
    drive.files().update(fileId=workout_log_sheet['spreadsheetId'], addParents=settings.WORKOUT_LOGS_FOLDER_ID).execute()

    return workout_log_sheet['spreadsheetId']


def clone_sheet_to_spreadsheet(clone_spreadsheet_id, clone_sheet_name, target_spreadsheet_id, target_sheet_name):
    return ''
