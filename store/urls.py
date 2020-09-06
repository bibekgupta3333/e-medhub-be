from django.urls import path

from . import views
app_name = 'store'
urlpatterns = [
    path("category/", views.MainCategorySerializerView.as_view()),
    path("category/<slug:slug>/", views.MainCategoryUpdateSerializerView.as_view()),
    path("sub/", views.SubCategorySerializerView.as_view()),
    path("sub/<slug:slug>/",
         views.SubCategoryUpdateSerializerView.as_view()),
    path("brand/", views.BrandSerializerView.as_view()),
    path("brand/<str:slug>/",
         views.BrandUpdateSerializerView.as_view()),
    path("product/", views.ProductSerializerView.as_view()),
    path("product/create/", views.ProductCreateSerializerView.as_view()),
    path("product/user/", views.UserProductListView.as_view()),
    path("product/<str:slug>/",
         views.ProductUpdateSerializerView.as_view()),
]
