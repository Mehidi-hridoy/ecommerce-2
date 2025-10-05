# core/views.py (update home function)
from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils import timezone
from django.db.models import Prefetch
from products.models import Product, Category
from inventory.models import Inventory
from dashboard.models import AnalyticsEvent  # Integrate your dashboard models

def home(request):
    # Log Analytics Event (page view)
    AnalyticsEvent.objects.create(
        event_type='home_page_view',
        data={'user_agent': request.META.get('HTTP_USER_AGENT', 'Unknown')},
        user=request.user if request.user.is_authenticated else None
    )

    # Fetch All Categories for Sidebar/Filter
    categories = Category.objects.all().prefetch_related('products')

    # Base Product Query: Active with stock prefetch, EXCLUDE empty slugs
    products_query = Product.objects.filter(
        is_active=True,
        slug__isnull=False  # Exclude None slugs
    ).exclude(
        slug=''  # Exclude empty string slugs
    ).prefetch_related(
        Prefetch('inventory', queryset=Inventory.objects.all(), to_attr='stock_info'),
        'attributes'  # For attributes
    ).select_related('category', 'brand').order_by('-created_at')  # Latest first

    # Search/Filter Handling
    search_query = request.GET.get('search', '')
    category_slug = request.GET.get('category', '')
    if search_query:
        products_query = products_query.filter(name__icontains=search_query)
    if category_slug:
        products_query = products_query.filter(category__slug=category_slug)

    # Pagination
    paginator = Paginator(products_query, 12)  # 12 products per page
    page_number = request.GET.get('page')
    products_page = paginator.get_page(page_number)

    # Enrich Products with Stock & Attributes
    product_list = []
    for product in products_page:
        stock_info = product.stock_info[0] if product.stock_info else None
        stock = stock_info.current_stock if stock_info else product.stock_quantity  # Fallback to model field
        attributes_str = ', '.join([f"{attr.name}: {attr.value}" for attr in product.attributes.all()]) if product.attributes.exists() else 'No attributes'
        product_list.append({
            'obj': product,  # Full object for URLs
            'name': product.name,
            'price': product.price,
            'image': product.image.url if product.image else '/static/no-image.png',
            'slug': product.slug,  # Guaranteed non-empty
            'stock': stock,
            'low_stock': stock <= (stock_info.low_stock_threshold if stock_info else 10),
            'category': product.category.name if product.category else 'Uncategorized',
            'attributes': attributes_str,
        })

    # Featured Products (Top 4 by latest)
    featured_products = product_list[:4]

    context = {
        'categories': categories,
        'products': product_list,  # For current page
        'featured_products': featured_products,
        'search_query': search_query,
        'selected_category': Category.objects.get(slug=category_slug) if category_slug else None,
        'products_page': products_page,  # For pagination links
        'total_products': products_query.count(),
        'software_version': '2.01',  # From your earlier snippet
    }
    return render(request, 'core/home.html', context)   