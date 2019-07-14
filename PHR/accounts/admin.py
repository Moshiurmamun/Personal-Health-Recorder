from django.contrib import admin
from accounts.models import UserProfile

# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'age')


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.site_header = "Personal Health Recorder"
