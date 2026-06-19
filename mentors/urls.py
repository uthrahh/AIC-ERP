from django.urls import path
from mentors import views

app_name = 'mentors'

urlpatterns = [
    path('', views.mentor_home, name='home'),
    path('profile/', views.mentor_profile, name='profile'),
]
