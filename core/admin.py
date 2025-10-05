# core/admin.py
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.http import HttpRequest
from django.utils.html import format_html
from .models import User, SiteSettings, AccessPermission
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from django.utils import timezone

class UserAdmin(ImportExportModelAdmin):  # CSV import/export
    list_display = ('username', 'email', 'phone', 'is_customer', 'is_supplier', 'date_joined')
    list_filter = ('is_customer', 'is_supplier', 'is_staff')
    search_fields = ('username', 'email', 'phone')
    actions = ['export_to_csv']  # Custom action below

    def export_to_csv(self, request, queryset):
        # Simple CSV via import_export (configure in settings)
        return self.export_action(request, queryset, 'csv')
    export_to_csv.short_description = "Export selected users to CSV"

class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'contact_email', 'sms_provider', 'created_at')
    fields = ('site_name', 'logo', 'favicon', 'contact_email', 'sms_provider', 'api_key')

class AccessPermissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'permission_name', 'allowed', 'created_at')
    list_filter = ('allowed', 'permission_name')
    search_fields = ('user__username', 'permission_name')

# Register
admin.site.register(User, UserAdmin)
admin.site.register(SiteSettings, SiteSettingsAdmin)
admin.site.register(AccessPermission, AccessPermissionAdmin)

# Custom Dashboard Index (Order Overview like your snippet)
class CustomAdminSite(AdminSite):
    site_header = "E-Commerce Dashboard"  # Modern title
    site_title = "E-Commerce Admin"
    index_title = "Welcome to Dashboard"

    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        # Add custom stats to index (fetched via views)
        return app_list

    def index(self, request: HttpRequest, extra_context=None):
        # Fetch Order Overview stats (link to orders app)
        from orders.models import Order
        today = timezone.now().date()
        total_orders_today = Order.objects.filter(created_at__date=today).count()
        pending_orders = Order.objects.filter(status='pending').count()
        # Calculate % change (compare to previous day; use dateutil for real calc)
        prev_total = Order.objects.filter(created_at__date=today - timezone.timedelta(days=1)).count()
        increase = ((total_orders_today - prev_total) / prev_total * 100) if prev_total else 0

        context = {
            **(extra_context or {}),
            'total_orders': total_orders_today,
            'increase': f"{increase:.0f}% {'increase' if increase > 0 else 'decrease'}",
            'pending_orders': pending_orders,
            # Add more: processed, on_delivery, etc.
            'processed_orders': Order.objects.filter(status='processing').count(),
            'on_delivery_orders': Order.objects.filter(status='shipped').count(),
            'delivered_orders': Order.objects.filter(status='delivered').count(),
            'cancelled_orders': Order.objects.filter(status='cancelled').count(),
            'returned_orders': Order.objects.filter(status='returned').count() if hasattr(Order, 'returned') else 0,
        }
        return super().index(request, extra_context=context)

admin.site.__class__ = CustomAdminSite  # Apply custom site