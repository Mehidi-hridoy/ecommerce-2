from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    phone = models.CharField(max_length=15)
    address = models.TextField()
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # For Leaderboard
    join_date = models.DateField(auto_now_add=True)
    is_loyal = models.BooleanField(default=False)  # Based on total_spent threshold

    def __str__(self):
        return self.user.username

# Leaderboard can be a view querying top customers by total_spent