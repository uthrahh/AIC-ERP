from django.contrib import admin
from feedback.models import Complaint, GeneralFeedback

admin.site.register(Complaint)
admin.site.register(GeneralFeedback)
