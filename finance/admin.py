from django.contrib import admin
from finance.models import *

admin.site.register(Invoice)
admin.site.register(Payment)
admin.site.register(BankAccount)
admin.site.register(StartupBillingPlan)