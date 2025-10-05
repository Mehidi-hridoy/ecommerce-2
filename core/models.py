
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    # Extend Django User for custom fields (e.g., for customers/suppliers)
    phone = models.CharField(max_length=15, blank=True)
    is_customer = models.BooleanField(default=False)
    is_supplier = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to='profiles/', blank=True)  # For logos/icons

    def __str__(self):
        return self.username

class SiteSettings(models.Model):  # General Settings
    site_name = models.CharField(max_length=100, default='E-Commerce')
    logo = models.ImageField(upload_to='logos/', blank=True)
    favicon = models.ImageField(upload_to='icons/', blank=True)
    contact_email = models.EmailField()
    sms_provider = models.CharField(max_length=50, default='Twilio')  # For SMS Promotion
    api_key = models.CharField(max_length=200, blank=True)  # API Settings
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.site_name

class AccessPermission(models.Model):  # Access Manage
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission_name = models.CharField(max_length=50)  # e.g., 'view_orders', 'edit_products'
    allowed = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.permission_name}"