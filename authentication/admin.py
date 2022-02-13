from django.contrib import admin
from .models import NotifcationType, Notification, Rating, User,UserType
# Register your models here.


class UserAdmin(admin.ModelAdmin):

    list_editable = ('user_type',)
    list_display = ('id','email','user_type')
    list_display_links = ('email',)
admin.site.register(User,UserAdmin)
admin.site.register(UserType)

admin.site.register(Notification)
admin.site.register(NotifcationType)
admin.site.register(Rating)