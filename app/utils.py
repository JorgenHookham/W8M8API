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


def get_master_framework_sheet_id():
    master_sheet = get_program_master_sheet()
    workout_sheets = filter(lambda x: x['properties']['title'] == 'Frameworks', master_sheet['sheets'])
    return map(lambda x: x['properties']['sheetId'], workout_sheets)[0]


def get_workout_component_sheet_ids(target_spreadsheet_id):
    sheets = get_google_sheets_service()
    component_sheet_names = sheets.spreadsheets().values().get(spreadsheetId=target_spreadsheet_id, range='A8:A14').execute()
    component_sheet_names = map(lambda x: x[0], component_sheet_names['values'])
    master_sheet = get_program_master_sheet()
    sheet_ids = []

    for sheet in master_sheet['sheets']:
        if sheet['properties']['title'] in component_sheet_names:
            sheet_ids.append(sheet['properties']['sheetId'])

    return sheet_ids


def create_new_workout():
    sheets = get_google_sheets_service()
    drive = get_google_drive_service()
    date = datetime.now().date().isoformat()
    time = datetime.now().time().isoformat()
    timestamp = '%s %s' % (date, time)

    # Make the new sheet
    workout_log_sheet = sheets.spreadsheets().create(body={'properties': {'title': timestamp}}).execute()

    # Move the new sheet into the workout logs folder
    drive.files().update(fileId=workout_log_sheet['spreadsheetId'], addParents=settings.WORKOUT_LOGS_FOLDER_ID).execute()

    return workout_log_sheet


def delete_sheet(target_spreadsheet_id, target_sheet_id):
    sheets = get_google_sheets_service()
    response = sheets.spreadsheets().batchUpdate(spreadsheetId=target_spreadsheet_id, body={
        'requests': [{
            'deleteSheet': {'sheetId': target_sheet_id}
        }]
    }).execute()
    return response


def clone_workout_sheet(clone_sheet_id, target_spreadsheet_id):
    sheets = get_google_sheets_service()
    new_sheet = sheets.spreadsheets().sheets().copyTo(
        spreadsheetId=settings.MASTER_PROGRAM_SHEET_ID,
        sheetId=clone_sheet_id,
        body={'destinationSpreadsheetId': target_spreadsheet_id}
    ).execute()
    sheets.spreadsheets().batchUpdate(spreadsheetId=target_spreadsheet_id, body={
        'requests': [{'updateSheetProperties': {
            'properties': {
                'sheetId': new_sheet['sheetId'],
                'title': 'Log'
            },
            'fields': 'title'
        }}]
    }).execute()
    return new_sheet
