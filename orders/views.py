from rest_framework.views import APIView
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.utils.text import slugify
from .models import Order, OrderedProduct
from .serializers import OrderSerializer, OrderedProductSerializer


class OrderedProductSerializerView(generics.ListCreateAPIView):
    """
    This method helps create ordered product item. And helps to get items.
    """
    permission_classes = (permissions.AllowAny,)
    queryset = OrderedProduct.objects.all()
    serializer_class = OrderedProductSerializer

    def perform_create(self, serializer):
        if not self.request.user:
            user = self.request.user
            serializer.save(user=user)


class OrderedProductUpdateSerializerView(generics.RetrieveUpdateDestroyAPIView):
    """
    This method helps retrieve ,update and delete the ordered product item.
    """
    permission_classes = (permissions.AllowAny,)
    queryset = OrderedProduct.objects.all()
    serializer_class = OrderedProductSerializer
    lookup_field = 'id'

    def perform_update(self, serializer):
        user = self.get_object().user
        serializer.save(user=user)


class OrderSerializerView(generics.ListCreateAPIView):
    """
    This method helps create check order list of ordered items and calculate total price.
    """
    permission_classes = (permissions.AllowAny,)
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        if not self.request.user:
            user = self.request.user
            serializer.save(user=user)


class OrderUpdateSerializerView(generics.RetrieveUpdateDestroyAPIView):
    """
    This method helps retrieve, update and delete order checkout related stuff.
    """
    permission_classes = (permissions.AllowAny,)
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'id'

    def perform_update(self, serializer):
        user = self.get_object().user
        serializer.save(user=user)
