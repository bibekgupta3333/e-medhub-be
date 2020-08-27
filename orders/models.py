from django.dispatch import receiver
from django.db import models
from store.models import Product
from emedhub import settings
from datetime import datetime
from django.db.models.signals import post_save, m2m_changed
# Create your models here.


class OrderedProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{str(self.user)} {str(self.product.name)}'

    class Meta:
        ordering = ('-created',)
        verbose_name = 'OrderProduct'
        verbose_name_plural = 'OrderProducts'


def limit_order_choices():
    Q = models.Q
    return Q(ordered=False)


class Order(models.Model):
    Payment = (
        ('COD', 'CashOnDelivery'),
        ('OP', 'OnlinePayment')
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, null=True, blank=True)
    products = models.ManyToManyField(
        OrderedProduct, limit_choices_to=limit_order_choices)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    shipping_address = models.CharField(
        max_length=200, blank=False, null=False, help_text='Please enter the accurate address before ordering')
    amount = models.IntegerField(default=0)
    being_delivered = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    payment = models.CharField(max_length=20, default='COD', choices=Payment)

    # def save(self, *args, **kwargs):
    #     if str(self.products.all()):
    #         print(self.products.all())
    #     super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return f"{str(self.user)}-{self.created}"

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


@receiver(m2m_changed, sender=Order.products.through)
def m2m_changed_order_model_receiver(sender, instance, action, **kwargs):
    try:
        instance.being_delivered = True
        instance.save()
        total = 0
        # if action == 'post_add' or action == 'post_remove':
        for product in instance.products.all():
            print(product)
            print(product.product.price)
            total += product.product.price*product.quantity
            products = product
            products.ordered = True
            products.save()
        print(total)
        instance.amount = total
        instance.save()

    except:
        print('error has occur in order signal')
