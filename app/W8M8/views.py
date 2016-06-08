from django.http import HttpResponse
from django.views.generic.base import View
from W8M8.utils import get_program_master_sheet


class TestView(View):
    template_name = 'W8M8/test.html'

    def get(self, request):
        master_sheet = get_program_master_sheet()
        import ipdb; ipdb.set_trace()
        return HttpResponse('result')
