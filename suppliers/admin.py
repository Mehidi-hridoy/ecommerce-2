from django.contrib import admin
from .models import Supplier, Purchase

# Inline for purchases related to a supplier
class PurchaseInline(admin.TabularInline):
    model = Purchase  # Must have FK to Supplier
    extra = 1  # Number of empty rows
    readonly_fields = ('total_price',)

# Supplier admin
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'email', 'phone')
    inlines = [PurchaseInline]

# Purchase admin
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'supplier', 'product', 'quantity', 'unit_price', 'total_price', 'status', 'purchase_date')
    list_filter = ('status', 'purchase_date', 'supplier')
    search_fields = ('supplier__name', 'product__title')

admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Purchase, PurchaseAdmin)
