# dashboard/views.py
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from orders.models import Order
from products.models import Product
from customers.models import Customer
from .models import Report  # For generating reports

def dashboard_html(request):
    # Fetch data
    from .views import dashboard_overview
    data = dashboard_overview(request).data
    return render(request, 'dashboard/overview.html', data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_overview(request):
    today = timezone.now().date()
    prev_day = today - timezone.timedelta(days=1)
    
    # Order Stats (like your snippet)
    total_orders = Order.objects.filter(created_at__date=today).count()
    prev_total = Order.objects.filter(created_at__date=prev_day).count()
    increase = ((total_orders - prev_total) / prev_total * 100) if prev_total else 0
    
    context = {
        'total_orders': total_orders,
        'increase': f"{increase:.0f}% {'increase' if increase > 0 else 'decrease'}",
        'pending_orders': Order.objects.filter(status='pending').count(),
        'processed_orders': Order.objects.filter(status='processing').count(),
        'on_delivery_orders': Order.objects.filter(status='shipped').count(),
        'delivered_orders': Order.objects.filter(status='delivered').count(),
        'cancelled_orders': Order.objects.filter(status='cancelled').count(),
        'partial_delivery': Order.objects.filter(status='partial').count() if hasattr(Order, 'partial') else 0,
        'returned_orders': 0,  # Add model field if needed
        # Analytics: Total revenue, top products
        'total_revenue': sum(o.total_amount for o in Order.objects.filter(created_at__date=today)),
        'top_product': Product.objects.annotate(order_count=models.Count('orderitem')).order_by('-order_count').first(),
        # Leaderboard preview
        'top_customers': Customer.objects.order_by('-total_spent')[:5],
    }
    return Response(context)

# For Chart Data (Performance)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def performance_chart(request):
    # Sample data; query real from AnalyticsEvent
    labels = ['Today', 'Yesterday', 'Last Week']
    data = [total_orders, prev_total, Order.objects.filter(created_at__week__lt=today).count()]  # Pseudo
    return Response({'labels': labels, 'data': data})