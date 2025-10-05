from django.db import models
import json
# dashboard/models.py (extend existing)

class PerformanceMetric(models.Model):  # For Performance section
    metric_name = models.CharField(max_length=50)  # e.g., 'Sales'
    value = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

class AnalyticsEvent(models.Model):  # For Analytics (track views, sales, etc.)
    event_type = models.CharField(max_length=50)  # e.g., 'page_view', 'order_placed'
    data = models.JSONField(default=dict)  # Flexible data storage
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('core.User', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.event_type} at {self.timestamp}"

class Report(models.Model):  # Custom Reports (e.g., sales report)
    name = models.CharField(max_length=100)
    report_type = models.CharField(max_length=50)  # e.g., 'sales', 'inventory'
    filters = models.JSONField(default=dict)  # e.g., {'date_from': '2025-01-01'}
    generated_at = models.DateTimeField(auto_now_add=True)
    # CSV download: Handled in views

    def __str__(self):
        return self.name

class DashboardPage(models.Model):  # Pages for dashboard customization
    name = models.CharField(max_length=100)
    content = models.TextField()  # Or JSON for widgets
    layout = models.JSONField(default=dict)  # e.g., {'widgets': ['orders_chart', 'sales_summary']}
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name