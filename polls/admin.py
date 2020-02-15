from django.contrib import admin

# Register your models here.
from polls.models import PlantData, Plants, NDVIMeasurement, Water
#admin.site.register(UserProfileInfo)

class PlantDataAdmin(admin.ModelAdmin):
    model = PlantData
class PlantsAdmin(admin.ModelAdmin):
    model = Plants
class NDVIMeasurementAdmin(admin.ModelAdmin):
    model = NDVIMeasurement
class WaterAdmin(admin.ModelAdmin):
    model = Water

admin.site.register(PlantData, PlantDataAdmin)
admin.site.register(Plants, PlantsAdmin)
admin.site.register(NDVIMeasurement, NDVIMeasurementAdmin)
admin.site.register(Water, WaterAdmin)