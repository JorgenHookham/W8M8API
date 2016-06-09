from django.http import HttpResponse
from django.views.generic.base import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.utils import get_program_master_sheet


class TestView(View):
    template_name = 'W8M8/test.html'

    def get(self, request):
        master_sheet = get_program_master_sheet()
        import ipdb; ipdb.set_trace()
        return HttpResponse('result')


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
        # create new workout log sheet
        # copy template sheet to new sheet, name it "Log"
        # return new sheet id
        return Response({}, status=status.HTTP_201_CREATED)

    def patch(self, request, format=None, *args, **kwargs):
        return Response({}, status=status.HTTP_202_ACCEPTED)

    def get(self, request, format=None, *args, **kwargs):
        return Response({}, status=status.HTTP_200_OK)


class WorkoutTemplates(APIView):
    """
    Allows access to workout templates present in the master program sheet.
    """
    def get(self, request, format=None, *args, **kwargs):
        return Response({}, status=status.HTTP_200_OK)
