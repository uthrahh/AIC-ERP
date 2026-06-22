from django.urls import path
from labs.views import booking_create, booking_list, admin_list, admin_detail
from labs.views import (
    lab_create,
    equipment_create,
)

app_name = 'labs'

urlpatterns = [
    path('', booking_list, name='list'),
    path('create/', booking_create, name='create'),
    path('manage/', admin_list, name='admin_list'),
    path('manage/<int:pk>/', admin_detail, name='admin_detail'),
    path(
        "add-lab/",
        lab_create,
        name="add_lab"
    ),

    path(
        "add-equipment/",
        equipment_create,
        name="add_equipment"
    ),
]
