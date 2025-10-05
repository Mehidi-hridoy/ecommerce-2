from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Customer
from .serializers import CustomerSerializer

@action(detail=False)
def leaderboard(self, request):
    top = self.queryset.order_by('-total_spent')[:10]
    return Response(TopCustomerSerializer(top, many=True).data)