from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200, null=False)
    description = models.TextField(null=True, blank=True, default='')

class Product(models.Model):
    name = models.CharField(max_length=200, null=False)
    short_description = models.CharField(max_length=200, null=True, default='')
    description = models.TextField(null=True, blank=True, default='')
    price = models.IntegerField(null=True, default=0)
    small_photo = models.ImageField(null=True)
    big_photo = models.ImageField(null=True)
    is_enabled = models.BooleanField(null=True, default=False)
    is_featured = models.BooleanField(null=True, default=False)
    is_really_hot = models.BooleanField(null=True, default=False)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
