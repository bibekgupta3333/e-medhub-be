from django.urls import path
from . import views
app_name = "orders"
urlpatterns = [
    path('', views.OrderedProductSerializerView.as_view()),
    path('<int:id>/', views.OrderedProductUpdateSerializerView.as_view()),
    path('cart/', views.OrderSerializerView.as_view()),
    path('cart/<int:id>/', views.OrderUpdateSerializerView.as_view()),
]
