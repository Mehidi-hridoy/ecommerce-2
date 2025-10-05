from .models import Inventory
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin

@admin.register(Inventory)
class InventoryAdmin(ImportExportModelAdmin):
    list_display = ('product', 'current_stock', 'low_stock_threshold')
    actions = ['update_stock']
    # Low stock alert
    change_list_template = 'admin/inventory_change_list.html'  # Custom template with warnings