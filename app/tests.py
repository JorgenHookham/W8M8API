from app.utils import clone_workout_sheet
from app.utils import create_new_workout
from app.utils import delete_sheet
from app.utils import get_workout_template_sheets
from app.utils import get_google_sheets_service
from datetime import datetime


def test_create_new_workout_flow():
    sheets = get_google_sheets_service()
    new_workout = create_new_workout()
    templates = get_workout_template_sheets()
    new_sheet = clone_workout_sheet(templates[0][0], new_workout['spreadsheetId'])
    delete_sheet(new_workout['spreadsheetId'], 0)

    # Give the new sheet a date parameter
    sheets.spreadsheets().values().update(spreadsheetId=new_workout['spreadsheetId'], range='A2', valueInputOption='USER_ENTERED', body={
        'range': 'A2',
        'majorDimension': 'ROWS',
        'values': [[datetime.now().date().isoformat()]]
    }).execute()
    return new_sheet
