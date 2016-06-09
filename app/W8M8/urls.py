"""W8M8 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from W8M8.views import Workouts, WorkoutTemplates
from W8M8.views import TestView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^test/', TestView.as_view()),
]

apiurlpatterns = [
    url(r'^api/workouts/$', Workouts.as_view()),
    url(r'^api/workouts/(?P<workout_spreadsheet_id>[a-zA-Z0-9\-_ #*]+/)$', Workouts.as_view()),
    url(r'^api/workout-templates/$', WorkoutTemplates.as_view()),
    url(r'^api/workout-templates/(?P<workout_template_sheet_name>[a-zA-Z0-9\-_ #*]+/)$', WorkoutTemplates.as_view()),
]

apiurlpatterns = format_suffix_patterns(apiurlpatterns)
urlpatterns = urlpatterns + apiurlpatterns
