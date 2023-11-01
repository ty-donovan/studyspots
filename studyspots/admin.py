from django.contrib import admin
from .models import Location, StudySpace, PendingStudySpot, PendingLocation


class StudySpaceAdmin(admin.ModelAdmin):
    exclude = (
        'location_ordinal', 'comments', 'overall_ratings', 'comfort_ratings', 'noise_level_ratings',
        'crowdedness_ratings')


admin.site.register(Location)
admin.site.register(PendingStudySpot)
admin.site.register(PendingLocation)
admin.site.register(StudySpace, StudySpaceAdmin)
