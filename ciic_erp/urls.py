from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('portal.urls')),
    path('accounts/', include('accounts.urls')),
    path('startups/', include('startups.urls')),
    path('applications/', include('applications.urls')),
    path('services/', include('services.urls')),
    path('labs/', include('labs.urls')),
    path('finance/', include('finance.urls')),
    path('feedback/', include('feedback.urls')),
    path('reports/', include('reports.urls')),
    path('halls/', include('halls.urls')),
    path('mentorship/', include('mentorship.urls')),
    path('mentors/', include('mentors.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
