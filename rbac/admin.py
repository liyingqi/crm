from django.contrib import admin

# Register your models here.
from rbac import models


class PermissionModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'url','name']
    list_editable = ['url','name']


# admin.site.register(models.User)
admin.site.register(models.Role)
admin.site.register(models.Permission)
admin.site.register(models.Menu)
# admin.site.register(models.Test)

