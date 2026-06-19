from django.urls import path
from halls import views

app_name = 'halls'

urlpatterns = [
    path('', views.booking_list, name='list'),
    path('book/', views.booking_create, name='create'),
    path('admin/', views.admin_list, name='admin_list'),
    path('admin/<int:pk>/', views.admin_detail, name='admin_detail'),
]
