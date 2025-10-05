from .models import Customer
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin

@admin.register(Customer)
class CustomerAdmin(ImportExportModelAdmin):
    list_display = ('user', 'phone', 'total_spent', 'is_loyal')
    list_filter = ('is_loyal',)