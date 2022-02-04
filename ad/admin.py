from django.contrib import admin
from .models import Ad, AdDetailType, AdImage, AdLike,AdType, ApartmentDetail, AreaDetail,City,BuildingType, Communications,RepairType,RentType,HomeDetail


class AdImageTabularInline(admin.TabularInline):

    model = AdImage


class AdAdmin(admin.ModelAdmin):
    inlines = [AdImageTabularInline]
    model = Ad

admin.site.register(Ad,AdAdmin)
admin.site.register(AdType)
admin.site.register(City)
admin.site.register(BuildingType)
admin.site.register(Communications)

admin.site.register(RepairType)
admin.site.register(RentType)
admin.site.register(HomeDetail)
admin.site.register(AreaDetail)
admin.site.register(AdLike)
admin.site.register(ApartmentDetail)
admin.site.register(AdDetailType)



class AdImageAdmin(admin.ModelAdmin):

    fields = ( 'image_tag', 'image')
    readonly_fields = ['image_tag']
    

admin.site.register(AdImage,AdImageAdmin)