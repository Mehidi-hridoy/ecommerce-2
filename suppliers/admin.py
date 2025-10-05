from .models import Supplier, Purchase
from django.contrib import admin


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')

class PurchaseInline(admin.TabularInline):
    model = Purchase
    extra = 1

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    inlines = [PurchaseInline]