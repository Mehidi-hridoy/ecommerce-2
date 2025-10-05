# products/urls.py (full update)
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet, CategoryViewSet, BrandViewSet, LandingPageViewSet, 
    upload_product, ProductDetailView  # Add these
)

app_name = 'products'  # Fixed from 'produtcs'

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'brands', BrandViewSet)
router.register(r'landing-pages', LandingPageViewSet)

urlpatterns = [
    path('', include(router.urls)),  # API endpoints
    path('upload/', upload_product, name='upload_product'),  # From previous
    path('<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),  # New: Detail page
]