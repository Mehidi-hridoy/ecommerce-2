from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser  # Admin for create/update
from .models import Product, Category, Brand, LandingPage
from .serializers import ProductSerializer, CategorySerializer, BrandSerializer, LandingPageSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().select_related('category', 'brand')
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    @action(detail=False, methods=['get'])  # Custom: /api/products/low-stock/
    def low_stock(self, request):
        low_stock = self.queryset.filter(inventory__current_stock__lte=10)
        serializer = self.get_serializer(low_stock, many=True)
        return Response(serializer.data)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class LandingPageViewSet(viewsets.ModelViewSet):
    queryset = LandingPage.objects.filter(is_active=True)
    serializer_class = LandingPageSerializer
    permission_classes = [IsAuthenticated]