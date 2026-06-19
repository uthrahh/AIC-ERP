from django.urls import path
from feedback.views import (
    complaint_create, complaint_list, feedback_submit,
    admin_complaint_list, admin_complaint_detail,
)

app_name = 'feedback'

urlpatterns = [
    path('complaints/', complaint_list, name='complaint_list'),
    path('complaints/create/', complaint_create, name='complaint_create'),
    path('submit/', feedback_submit, name='submit'),
    path('manage/complaints/', admin_complaint_list, name='admin_complaint_list'),
    path('manage/complaints/<int:pk>/', admin_complaint_detail, name='admin_complaint_detail'),
]
