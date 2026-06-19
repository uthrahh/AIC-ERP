from django.urls import path
from services.views import (
    request_create, request_list, request_feedback,
    admin_list, admin_detail,
)

app_name = 'services'

urlpatterns = [
    path('', request_list, name='list'),
    path('create/', request_create, name='create'),
    path('<int:pk>/feedback/', request_feedback, name='feedback'),
    path('manage/', admin_list, name='admin_list'),
    path('manage/<int:pk>/', admin_detail, name='admin_detail'),
]
