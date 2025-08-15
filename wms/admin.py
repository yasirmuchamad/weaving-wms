from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'unit', 'picture']