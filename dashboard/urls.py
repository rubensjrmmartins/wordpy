from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('stats/', views.dashboard_stats, name='stats'),
]
