from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200, null=False)
    description = models.TextField(null=True, blank=True, default='')

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, null=False)
    short_description = models.CharField(max_length=200, null=True, default='')
    description = models.TextField(null=True, blank=True, default='')
    price = models.IntegerField(default=0)
    small_photo = models.ImageField(null=True)
    big_photo = models.ImageField(null=True)
    is_enabled = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_really_hot = models.BooleanField(default=False)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "{n} ({i})".format(n=self.name, i=self.id)

    def readable_price(self):
        true_price = self.price / 100
        return true_price