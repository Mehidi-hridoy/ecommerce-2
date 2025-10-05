from .models import Order, OrderItem, POSSession
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin

@admin.register(Order)
class OrderAdmin(ImportExportModelAdmin):
    list_display = ('order_number', 'user', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    actions = ['mark_as_delivered', 'export_orders']
    raw_id_fields = ('user',)  # For large user lists

def mark_as_delivered(self, request, queryset):
    queryset.update(status='delivered')
mark_as_delivered.short_description = "Mark selected as delivered"

@admin.register(POSSession)
class POSSessionAdmin(admin.ModelAdmin):
    list_display = ('cashier', 'start_time', 'total_sales', 'is_active')