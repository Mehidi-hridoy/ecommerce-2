from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, POSSessionViewSet, my_orders

app_name = 'orders'

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')           # ✅ basename added
router.register(r'pos-sessions', POSSessionViewSet, basename='pos')  # ✅ basename added

urlpatterns = [
    path('', include(router.urls)),
    path('my-orders/', my_orders, name='my-orders'),  # /api/orders/my-orders/
]
