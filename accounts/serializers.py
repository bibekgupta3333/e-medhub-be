from rest_framework import serializers
from .models import MyUser, UserProfile, CompanyProfile


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email',
                  'is_staff', 'is_buyer', 'is_seller', 'is_active', 'password']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'user',
                  'phone', 'bio', 'photo', 'address']
        depth = 1


class CompanyProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyProfile
        fields = ['id', 'user', 'company_name',
                  'phone', 'bio', 'photo', 'address']
        depth = 1
