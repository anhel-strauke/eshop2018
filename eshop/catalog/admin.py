from django.contrib import admin
from .models import Category, Product

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "short_description"]


@admin.register(Product)
class ProductAdmin(admin.ProductAdmin):
    list_filter = ["category", "is_enabled", "is_featured", "is_really_hot",]
    list_display = ["id", "name", "short_description", "price", "category", "is_enabled", "is_featured", "is_really_hot"]
    list_display_links = ["id", "name"]