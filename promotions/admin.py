from .models import Coupon, Promotion
from django.contrib import admin

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'valid_from', 'valid_to', 'max_uses')
    actions = ['activate_coupons']

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('name', 'discount_value', 'start_date', 'is_active')