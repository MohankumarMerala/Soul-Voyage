from django.urls import path
from . import views

app_name = 'consultation'

urlpatterns = [
    path('request/', views.consultation_request, name='request'),
]