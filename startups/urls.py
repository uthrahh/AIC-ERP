from django.urls import path
from startups.views import (
    profile_setup,
    profile_view,
    profile_edit,
    document_upload,
    admin_startup_list,
    admin_startup_create,
    admin_startup_detail,
    admin_startup_edit,
    StartupPublicDetailView,
    founder_create,
)

app_name = 'startups'

urlpatterns = [
    path('profile/setup/', profile_setup, name='profile_setup'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', profile_edit, name='profile_edit'),
    path('profile/documents/upload/', document_upload, name='document_upload'),
    path('startups/admin/list/', admin_startup_list, name='admin_list'),
    path('startups/admin/create/', admin_startup_create, name='admin_create'),
    path('startups/admin/<int:pk>/', admin_startup_detail, name='admin_detail'),
    path('startups/admin/<int:pk>/edit/', admin_startup_edit, name='admin_edit'),
    path('public/<int:pk>/', StartupPublicDetailView.as_view(), name='public_detail'),
    path(
        'profile/founders/add/',
        founder_create,
        name='founder_create'
    ),
]
