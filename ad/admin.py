from django.contrib import admin
from .models import Ad, AdDetailType, AdImage,AdType,City,BuildingType,RepairType,RentType,HomeDetail


admin.site.register(Ad)
admin.site.register(AdType)
admin.site.register(City)
admin.site.register(BuildingType)

admin.site.register(RepairType)
admin.site.register(RentType)
admin.site.register(HomeDetail)
admin.site.register(AdDetailType)
admin.site.register(AdImage)