from django.urls import path
from portal.views import (
    home,
    about,
    startup_directory,
    contact,
    startup_home,
    admin_home,
    admin_history,
)

app_name = 'portal'

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('startups/', startup_directory, name='startup_directory'),
    path('contact/', contact, name='contact'),
    path('startup/', startup_home, name='startup_home'),
    path('AIC-CIIC-admin/', admin_home, name='admin_home'),
    path('AIC-CIIC-admin/history/', admin_history, name='admin_history'),
]
