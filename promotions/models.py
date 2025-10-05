from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
from decimal import Decimal

class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)  # e.g., 10.00 for 10%
    is_percentage = models.BooleanField(default=True)
    valid_from = models.DateField()
    valid_to = models.DateField()
    max_uses = models.IntegerField(default=1)
    used_by = models.ManyToManyField(User, blank=True, related_name='used_coupons')

    def __str__(self):
        return self.code

class Promotion(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    discount_type = models.CharField(max_length=20, choices=[('fixed', 'Fixed'), ('percent', 'Percentage')])
    discount_value = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    # SMS Promotion: Add a field for SMS message template
    sms_template = models.TextField(blank=True, help_text="SMS message for promotion")

    def __str__(self):
        return self.name