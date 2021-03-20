from django.contrib import admin
from . import models

class GroupMemberInline(admin.TabularInline):
  model = models.GroupMember

admin.site.register(models.Group)
admin.site.register(models.GroupMember)
