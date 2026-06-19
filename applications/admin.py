from django.contrib import admin
from applications.models import *

admin.site.register(Application)
admin.site.register(ApplicationReview)
admin.site.register(ApplicationMentorshipReview)