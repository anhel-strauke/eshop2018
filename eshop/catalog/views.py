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
    products = Product.objects.filter(category=category).order_by("name")
    # 2. Подготовка контекста
    context = {
        "category": category,
        "products": products,
    }
    # 3. Вывод результат
    return render(request, "category.html", context=context)