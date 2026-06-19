from django.contrib import admin
from services.models import *

admin.site.register(ServiceRequest)
admin.site.register(ServiceCategory)
admin.site.register(ServiceTariff)