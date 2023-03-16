from django.contrib import admin

from . models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'job', 'email', 'date')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('date',)


admin.site.register(User, UserAdmin)

