# products/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Brand, Product, ProductAttribute, LandingPage

class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 2  # Allow 2 default attributes (e.g., color, size)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent', 'get_product_count')
    list_filter = ('parent',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

    def get_product_count(self, obj):
        return obj.products.count()
    get_product_count.short_description = 'Products'

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_product_count')
    search_fields = ('name', 'description')

    def get_product_count(self, obj):
        return obj.product_set.count()  # Assuming related via brand
    get_product_count.short_description = 'Products'

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'brand', 'stock_quantity', 'is_active', 'created_at')
    list_filter = ('category', 'brand', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductAttributeInline]
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'slug', 'description', 'category', 'brand')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'stock_quantity', 'is_active')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Advanced', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        # Sync stock to Inventory if exists (from earlier model)
        from inventory.models import Inventory
        if not change:  # New product
            Inventory.objects.create(product=obj, current_stock=obj.stock_quantity)
        else:
            inv = obj.inventory
            if inv:
                inv.current_stock = obj.stock_quantity
                inv.save()
        super().save_model(request, obj, form, change)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):  # Wait, duplicate? Use above
    pass  # Use the class defined

@admin.register(LandingPage)
class LandingPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_active')
    prepopulated_fields = {'slug': ('title',)}