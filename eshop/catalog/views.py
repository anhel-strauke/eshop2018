from django.shortcuts import render
from .models import Category, Product
from django.http import Http404

# Create your views here.
def category_view(request, cat_id):
    # 1. Получение информации из базы по запросу
    try:
        category = Category.objects.get(id=cat_id)
    except Category.DoesNotExist:
        raise Http404
    products = Product.objects.filter(category=category).exclude(is_enabled=False).order_by("name")
    categories = Category.objects.order_by("name")
    # 2. Подготовка контекста
    context = {
        "category": category,
        "categories": categories,
        "products": products,
    }
    # 3. Вывод результат
    return render(request, "category.html", context=context)


def product_view(request, prod_id):
    pass
