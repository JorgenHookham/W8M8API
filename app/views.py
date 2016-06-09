from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.utils import get_workout_template_sheets
from app.utils import clone_workout_sheet
from app.utils import create_new_workout
from app.utils import delete_sheet
from app.utils import get_google_sheets_service
from datetime import datetime


class Workouts(APIView):
    """
    **POST** \n
    Allows for creation of new workout logs. \n
    `workout_template_sheet_name` The name of the program master sheet to be used as the template for this workout. \n

    **PATCH**\n
    Allows for updating rows in a workout log.\n
    `spreadsheet_id` The id of the spreadsheet.\n
    `data` An array of objects representing rows to be updated.\n
    `data[n]['rowNumber']` The row to be updated.\n
    `data[n]['actualWeight']` The actual weight used during the set.\n
    `data[n]['actualReps']` The actual number of reps completed during the set.\n
    `data[n]['actualStartTime']` Timestamp the set started at.\n
    `data[n]['actualStopTime']` Timestamp the set was completed at.\n

    **GET**\n
    Allows for retrieving all data from a workout log.\n
    `spreadsheet_id` The id of the spreadsheet.\n
    """
    def post(self, request, format=None, *args, **kwargs):
        # data = request.data
        sheets = get_google_sheets_service()
        new_workout = create_new_workout()
        template_sheet_id = request.data.get('template_sheet_id', None)

        if not template_sheet_id:
            return Response('No template sheet provided', status=status.HTTP_400_BAD_REQUEST)

        clone_workout_sheet(template_sheet_id, new_workout['spreadsheetId'])
        delete_sheet(new_workout['spreadsheetId'], 0)

        # Give the new sheet a date parameter
        sheets.spreadsheets().values().update(
            spreadsheetId=new_workout['spreadsheetId'],
            range='A2',
            valueInputOption='USER_ENTERED',
            body={
                'range': 'A2',
                'majorDimension': 'ROWS',
                'values': [[datetime.now().date().isoformat()]]
            }
        ).execute()

        return Response(new_workout['spreadsheetId'], status=status.HTTP_201_CREATED)

    def patch(self, request, format=None, *args, **kwargs):
        return Response({}, status=status.HTTP_202_ACCEPTED)

    def get(self, request, format=None, *args, **kwargs):
        if kwargs.get('workout_spreadsheet_id', None):
            raise NotImplementedError()
        return Response({}, status=status.HTTP_200_OK)


class WorkoutTemplates(APIView):
    """
    Allows access to workout templates present in the master program sheet.
    """
    def get(self, request, format=None, *args, **kwargs):
        if kwargs.get('workout_template_sheet_name', None):
            raise NotImplementedError()
        else:
            response = get_workout_template_sheets()
        return Response(response, status=status.HTTP_200_OK)
