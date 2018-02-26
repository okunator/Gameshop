from django.contrib import admin
from . import models
# Register your models here.

# class GameInline(admin.TabularInline):
#     model = models.Game

admin.site.register(models.Game)
admin.site.register(models.Genre)
