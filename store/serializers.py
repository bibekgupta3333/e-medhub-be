from rest_framework import serializers
from .models import MainCategory, SubCategory, Brand, Product
from django.contrib.auth import get_user_model
User = get_user_model()
# create list


class MainCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MainCategory
        fields = '__all__'
        depth = 1
        depth = 1

# CL


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'
        depth = 1

# CL


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'
        depth = 1


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id',)


# CRUDL


class ProductSerializer(serializers.ModelSerializer):
    # user = UserSerializer()

    class Meta:
        model = Product
        fields = '__all__'


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
