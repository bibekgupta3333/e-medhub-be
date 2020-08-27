from django.db import models
import uuid
from datetime import datetime
from emedhub import settings
from django.db.models.signals import post_save
from django.utils.text import slugify


def image_path(_, filename):
    extension = filename.split('.')[-1]
    unique_id = uuid.uuid4().hex
    new_file_name = unique_id+'.'+extension
    new_file_name = f"{datetime.now().date()}/{slugify(_.category)}/{new_file_name}"
    print(new_file_name)
    return "users/"+new_file_name


class MainCategory(models.Model):
    name = models.CharField(max_length=120, null=False, blank=False)
    slug = models.SlugField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=120, null=False, blank=False)
    slug = models.SlugField(max_length=200, blank=True, null=True)
    category = models.ForeignKey(
        MainCategory, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=120, null=False, blank=False)
    slug = models.SlugField(max_length=200, blank=True, null=True)
    category = models.ForeignKey(
        MainCategory, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=False, null=False)
    slug = models.SlugField(max_length=200, blank=True, null=True)
    generic_name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True)

    image = models.ImageField(upload_to=image_path, blank=True)
    category = models.ForeignKey(MainCategory, related_name='main_products',
                                 on_delete=models.CASCADE,  blank=False, null=False)
    sub_category = models.ForeignKey(SubCategory, related_name='sub_products',
                                     on_delete=models.CASCADE, blank=False, null=False)
    brand = models.ForeignKey(Brand, related_name='brand_products',
                              on_delete=models.CASCADE,  blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    mfg_company = models.CharField(max_length=200, blank=True, null=True)
    mfg_month = models.CharField(max_length=2, null=True, blank=True)
    mfg_year = models.CharField(max_length=4, null=True, blank=True)
    exp_month = models.CharField(max_length=2, null=True, blank=True)
    exp_year = models.CharField(max_length=4, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.name


def post_save_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:
            instance.slug = slugify(instance.name)+f"-{instance.id}"
            instance.save()
        except:
            pass


post_save.connect(post_save_model_receiver,
                  sender=MainCategory)
post_save.connect(post_save_model_receiver,
                  sender=SubCategory)
post_save.connect(post_save_model_receiver,
                  sender=Brand)
post_save.connect(post_save_model_receiver,
                  sender=Product)


# class FeedBack(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL,
#                              on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     message = models.TextField()
#     created_date = models.DateTimeField(auto_now_add=True)
#     updated_date = models.DateTimeField(auto_now=True)
