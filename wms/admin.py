from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'unit', 'picture']

@admin.register(Subdepartement)
class Subdepartement(admin.ModelAdmin):
    list_display = ['name', 'leader']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['item', 'qty', 'transaction_type', 'date', 'requested_by', 'received_by', 'subdepartement']