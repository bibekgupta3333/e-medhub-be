from .models import MainCategory, SubCategory, Brand, Product
from .serializers import BrandSerializer, MainCategorySerializer, SubCategorySerializer, ProductSerializer
from rest_framework.views import APIView
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.utils.text import slugify


class MainCategorySerializerView(generics.ListCreateAPIView):
    """
        This method helps to creating main categories and getting main category
    """
    permission_classes = (permissions.AllowAny,)
    queryset = MainCategory.objects.all()
    serializer_class = MainCategorySerializer


class MainCategoryUpdateSerializerView(generics.RetrieveUpdateAPIView):
    """
        This method helps to retrieve, update and delete the main categories.
    """
    permission_classes = (permissions.AllowAny,)
    queryset = MainCategory.objects.all()
    serializer_class = MainCategorySerializer
    lookup_field = 'slug'

    def perform_update(self, serializer):
        name = self.get_object().name
        id = self.get_object().id
        slug = slugify(name)+f"-{id}"
        print(slug)
        serializer.save(slug=slug)


class SubCategorySerializerView(generics.ListCreateAPIView):
    """
        This method helps to creating sub categories and getting sub category
    """
    permission_classes = (permissions.AllowAny,)
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


class SubCategoryUpdateSerializerView(generics.RetrieveUpdateAPIView):
    """
        This method helps to retrieve, update and delete the  sub categories.
    """
    permission_classes = (permissions.AllowAny,)
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    lookup_field = 'slug'

    def perform_update(self, serializer):
        name = self.get_object().name
        id = self.get_object().id
        slug = slugify(name)+f"-{id}"
        print(slug)
        serializer.save(slug=slug)


class BrandSerializerView(generics.ListCreateAPIView):
    """
        This method helps to creating brand and getting brand.
    """
    permission_classes = (permissions.AllowAny,)
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class BrandUpdateSerializerView(generics.RetrieveUpdateAPIView):
    """
        This method helps to retrieve, update and delete the brand.
    """
    permission_classes = (permissions.AllowAny,)
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    lookup_field = 'slug'

    def perform_update(self, serializer):
        name = self.get_object().name
        id = self.get_object().id
        slug = slugify(name)+f"-{id}"
        print(slug)
        serializer.save(slug=slug)


class ProductSerializerView(generics.ListCreateAPIView):
    """
        This method helps to creating product and getting product.
    """
    permission_classes = (permissions.AllowAny,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        if not self.request.user:
            serializer.save(user=self.request.user.id)
            return
        serializer.save()


class ProductUpdateSerializerView(generics.RetrieveUpdateDestroyAPIView):
    """
        This method helps to retrieve, update and delete the product.
    """
    permission_classes = (permissions.AllowAny,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'

    def perform_update(self, serializer):
        name = self.get_object().name
        id = self.get_object().id
        slug = slugify(name)+f"-{id}"
        print(slug)
        user = self.get_object().user
        serializer.save(slug=slug, user=user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views = instance.views+1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
