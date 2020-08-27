from django.contrib import admin
from .models import Order, OrderedProduct
# Register your models here.

admin.site.register(Order)
admin.site.register(OrderedProduct)
