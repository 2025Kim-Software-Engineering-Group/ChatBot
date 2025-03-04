from django.urls import path
from ChatBot.views import reportMessage

urlpatterns = [

path('api/', reportMessage, name='report_message'),
]
