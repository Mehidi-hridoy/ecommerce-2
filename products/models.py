from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='brands/', blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class ProductAttribute(models.Model):  # Attributes (e.g., size, color)
    name = models.CharField(max_length=50)  # e.g., 'Color'
    value = models.CharField(max_length=50)  # e.g., 'Red'
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='attributes')

    def __str__(self):
        return f"{self.name}: {self.value}"

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='products/', blank=True)
    is_active = models.BooleanField(default=True)
    stock_quantity = models.IntegerField(default=0)  # Links to Inventory
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class LandingPage(models.Model):  # Landing Pages
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()  # Or use a rich text field like CKEditor
    is_active = models.BooleanField(default=True)
    meta_description = models.TextField(blank=True)

    def __str__(self):
        return self.title