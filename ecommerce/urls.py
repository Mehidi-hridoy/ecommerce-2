from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Web page routes
    path('', include('core.urls')),                  
    path('products/', include('products.urls')),    
    path('orders/', include('orders.urls')),        
    path('customers/', include('customers.urls')),  
    path('suppliers/', include('suppliers.urls')),  
    path('inventory/', include('inventory.urls')),  
    path('promotions/', include('promotions.urls')), 
    path('dashboard/', include('dashboard.urls')),  

    # JWT authentication endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # App APIs
    path('api/products/', include('products.urls')),               
    path('api/orders/', include('orders.urls')),                   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # Optional, for static too

