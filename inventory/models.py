from django.db import models
from products.models import Product

class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='inventory')
    current_stock = models.IntegerField(default=0)
    low_stock_threshold = models.IntegerField(default=10)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - Stock: {self.current_stock}"

# For Reports: Use views to generate CSV of stock levels