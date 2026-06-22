from django.urls import path
from portal.views import (
    home,
    about,
    startup_directory,
    contact,
    team,
    startup_home,
    admin_home,
    admin_history,
)

app_name = 'portal'

urlpatterns = [
    path('', about, name='home'),
    path('about/', about, name='about'),
    path('startups/', startup_directory, name='startup_directory'),
    path('team/', team, name='team'),
    path('contact/', contact, name='contact'),
    path('startup/', startup_home, name='startup_home'),
    path('AIC-CIIC-admin/', admin_home, name='admin_home'),
    path('AIC-CIIC-admin/history/', admin_history, name='admin_history'),
]
