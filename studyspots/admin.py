from django.contrib import admin
from .models import Location, StudySpot, PendingStudySpot, PendingLocation

# Register your models here.
admin.site.register(Location)
admin.site.register(StudySpot)
admin.site.register(PendingStudySpot)
admin.site.register(PendingLocation)