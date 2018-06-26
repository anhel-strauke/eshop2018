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
    price = models.PositiveIntegerField(default=0)
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

class Order(models.Model):
    code = models.CharField(max_length=30)
    person_name = models.CharField(max_length=200)
    person_email = models.EmailField()
    person_address = models.TextField()
    person_phone = models.CharField(max_length=30)
    notes = models.TextField(blank=True, null=True)
    status = models.ForeignKey('OrderStatus', on_delete=models.SET_NULL, null=True)
    comment = models.TextField(blank=True, null=True)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{i} ({d}, {pn})".format(i=self.id, d=self.order_date, pn=self.person_name)


class OrderStatus(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return "{i} ({d})".format(i=self.id, d=self.name)


class OrderedProduct(models.Model):
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "Order: {n} ({i})".format(n=self.order, i=self.id)

    def readable_price(self):
        true_price = self.price / 100
        return true_price
