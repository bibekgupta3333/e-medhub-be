from django.urls import path
from .views import UserView, CompanyProfileView, UserProfileView, SignupView, ResetPasswordView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
app_name = 'accounts'

urlpatterns = [
    path('user/<str:email>/', UserView.as_view()),
    path('signup/', SignupView.as_view()),
    path('company/<int:pk>/', CompanyProfileView.as_view()),
    path('users/<int:pk>/', UserProfileView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('<str:token>/', ResetPasswordView.as_view(), name='password_reset'),
    path('reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('activate/<uidb64>/', ResetPasswordView.as_view(),
         name='password_reset_activate'),
]
