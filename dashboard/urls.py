from django.urls import path
from .views import dashboard_overview, performance_chart

app_name = 'dashboard'

urlpatterns=[
    path('overview/', dashboard_overview),
    path('performance/', performance_chart),
    
]