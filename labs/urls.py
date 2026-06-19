from django.urls import path
from labs.views import booking_create, booking_list, admin_list, admin_detail

app_name = 'labs'

urlpatterns = [
    path('', booking_list, name='list'),
    path('create/', booking_create, name='create'),
    path('manage/', admin_list, name='admin_list'),
    path('manage/<int:pk>/', admin_detail, name='admin_detail'),
]
