# products/views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.forms import inlineformset_factory

from .models import Product, Category, Brand, LandingPage, ProductAttribute
from .serializers import ProductSerializer, CategorySerializer, BrandSerializer, LandingPageSerializer
from .forms import ProductUploadForm, ProductAttributeForm
from dashboard.models import AnalyticsEvent
from inventory.models import Inventory


@login_required
def upload_product(request):
    AttributeFormSet = inlineformset_factory(Product, ProductAttribute, form=ProductAttributeForm, extra=2)
    if request.method == 'POST':
        form = ProductUploadForm(request.POST, request.FILES)
        formset = AttributeFormSet(request.POST, instance=Product())
        if form.is_valid() and formset.is_valid():
            product = form.save()
            formset.instance = product
            formset.save()
            return redirect('home')
    else:
        form = ProductUploadForm()
        formset = AttributeFormSet(instance=Product())
    
    context = {'form': form, 'formset': formset}
    return render(request, 'products/upload.html', context)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().select_related('category', 'brand')
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        # Only include products with total inventory <= 10
        low_stock_products = []
        for product in self.queryset:
            total_stock = sum(inv.current_stock for inv in product.inventory.all())
            if total_stock <= 10:
                low_stock_products.append(product)
        serializer = self.get_serializer(low_stock_products, many=True)
        return Response(serializer.data)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/detail.html'
    context_object_name = 'product'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Related products
        context['related_products'] = Product.objects.filter(
            category=self.object.category,
            is_active=True
        ).exclude(pk=self.object.pk)[:4]

        # Stock info (aggregate all inventory)
        stock_items = self.object.inventory.all()
        total_stock = sum(item.current_stock for item in stock_items)
        context['stock'] = total_stock
        context['low_stock_threshold'] = min([i.low_stock_threshold for i in stock_items], default=10)

        # Analytics logging
        AnalyticsEvent.objects.create(
            event_type='product_view',
            data={'product_slug': self.object.slug},
            user=self.request.user if self.request.user.is_authenticated else None
        )
        return context


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
