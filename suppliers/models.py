from django.db import models

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    logo = models.ImageField(upload_to='suppliers/', blank=True)

    def __str__(self):
        return self.name

class Purchase(models.Model):  # Purchase orders from suppliers
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='purchases')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')  # pending, received, etc.

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Purchase {self.id} from {self.supplier.name}"