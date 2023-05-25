from django.contrib import admin
from .models import *
# from .models import UserData

# Register your models here.
admin.site.register(Employee) 
admin.site.register(Client)
admin.site.register(Company)
admin.site.register(Project)
admin.site.register(Mapping)
admin.site.register(Attendance)
admin.site.register(ApprovedAtt)

# admin.site.register(JrAttendance)

# @admin.register(UserData)
# class UserDataAdmin(admin.ModelAdmin):
#     list_display = ('user', 'role')