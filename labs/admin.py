from django.contrib import admin
from labs.models import *

admin.site.register(Lab)
admin.site.register(Equipment)
admin.site.register(LabBooking)
admin.site.register(BookingEquipment)
admin.site.register(EquipmentImportLog)