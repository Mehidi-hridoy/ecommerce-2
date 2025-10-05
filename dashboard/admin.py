from .models import AnalyticsEvent

from django.contrib import admin

@admin.register(AnalyticsEvent)
class AnalyticsAdmin(admin.ModelAdmin):
    list_display = ('event_type', 'timestamp', 'user')
    # Add chart preview in change_view