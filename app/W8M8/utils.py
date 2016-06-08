from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import httplib2
import json
import os


def get_oauth_credentials():
    google_json = json.loads(os.environ.get('GOOGLE_SECRET_JSON'))
    scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(google_json, scopes=scopes)
    return credentials


def get_program_master_sheet():
    credentials = get_oauth_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?version=v4')
    service = build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)
    program_master_spreadsheet_id = '1rA5ugdgnVvT0_D9JL_yBAzf1_-_wm3YojhjgDqYGumU'
    return service.spreadsheets().get(spreadsheetId=program_master_spreadsheet_id).execute()
