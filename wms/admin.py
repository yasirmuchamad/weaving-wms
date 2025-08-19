from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'unit', 'location', 'picture']

@admin.register(Subdepartement)
class Subdepartement(admin.ModelAdmin):
    list_display = ['name', 'leader']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction_type', 'date', 'requested_by', 'received_by', 'subdepartement']

@admin.register(TransactionItem)
class TransactionItemAdmin(admin.ModelAdmin):
    list_display = ['item', 'qty']