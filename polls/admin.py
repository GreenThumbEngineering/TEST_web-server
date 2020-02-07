from django.contrib import admin

# Register your models here.
from polls.models import PlantData
#admin.site.register(UserProfileInfo)

class PlantDataAdmin(admin.ModelAdmin):
    model = PlantData

admin.site.register(PlantData, PlantDataAdmin)