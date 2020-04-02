from django.contrib import admin

# Register your models here.
from polls.models import PlantData, Plants, Water
#admin.site.register(UserProfileInfo)

class PlantDataAdmin(admin.ModelAdmin):
    model = PlantData
class PlantsAdmin(admin.ModelAdmin):
    model = Plants
class WaterAdmin(admin.ModelAdmin):
    model = Water

admin.site.register(PlantData, PlantDataAdmin)
admin.site.register(Plants, PlantsAdmin)
admin.site.register(Water, WaterAdmin)