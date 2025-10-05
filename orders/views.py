from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action  # ✅ import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import Order, POSSession
from .serializers import OrderSerializer, POSSessionSerializer


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only return orders for the current user
        return Order.objects.filter(user=self.request.user).select_related('user')

    @action(detail=False, methods=['get'])  # /api/orders/incomplete/
    def incomplete(self, request):
        incomplete = self.get_queryset().filter(is_incomplete=True)
        serializer = self.get_serializer(incomplete, many=True)
        return Response(serializer.data)


class POSSessionViewSet(viewsets.ModelViewSet):
    queryset = POSSession.objects.filter(is_active=True)
    serializer_class = POSSessionSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]  # Only cashiers/admins


# Custom login-protected view example
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_orders(request):
    orders = Order.objects.filter(user=request.user)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)
