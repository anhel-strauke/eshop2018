from django.shortcuts import render
from .models import Category, Product
from django.http import Http404, HttpResponseRedirect

from .cart import Cart

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
    # 1. Получение информации из базы по запросу
    try:
        product = Product.objects.get(id=prod_id)
    except Product.DoesNotExist:
        raise Http404

    categories = Category.objects.order_by("name")
    # 2. Подготовка контекста
    context = {
        "categories": categories,
        "product": product,
    }
    # 3. Вывод результат
    return render(request, "product.html", context=context)


def main_view(request):
    # 1. Получение информации из базы по запросу
    products = Product.objects.filter(is_featured=True).exclude(is_enabled=False).order_by("name")
    hot_products = Product.objects.filter(is_really_hot=True).exclude(is_enabled=False).order_by("name")
    categories = Category.objects.order_by("name")
    # 2. Подготовка контекста
    context = {
        "categories": categories,
        "products": products,
        "hot_products": hot_products,
    }
    # 3. Вывод результат
    return render(request, "main.html", context=context)

def buy_view(request, prod_id):
    cart = Cart(request)
    try:
        product = Product.objects.get(id=prod_id)
    except Product.DoesNotExist:
        raise Http404
    cart.add_product(product)
    return HttpResponseRedirect("/")


def cart_view(request):
    CART_FIELD_PREFIX = "item_"
    cart = Cart(request)
    display_products = []
    total = 0
    if request.method == "POST":
        for field_name, field_value in request.POST.items():
            if field_name.startswith(CART_FIELD_PREFIX):
                try:
                    prod_id = int(field_name[len(CART_FIELD_PREFIX):])
                    product = Product.objects.get(id=prod_id)
                except ValueError:
                    continue
                except Product.DoesNotExist:
                    continue
                try:
                    qty = int(field_value)
                except ValueError:
                    qty = cart.quantity_by_id(prod_id)
                cart.update_product(product, qty)
                if qty > 0:
                    display_products.append({
                        "name": product.name,
                        "id": product.id,
                        "short_description": product.short_description,
                        "quantity": qty,
                        "subtotal": qty * product.price / 100,
                        })
                    total += qty * product.price

        if "go_back" in request.POST:
            return HttpResponseRedirect("/")
        elif "do_order" in request.POST:
            return HttpResponseRedirect("/cart/checkout/")

    else:
        products = cart.products()
        for p in products:
            display_products.append({
                "name": p["product"].name,
                "id": p["product"].id,
                "short_description": p["product"].short_description,
                "quantity": p["quantity"],
                "subtotal": p["subtotal"] / 100,
                })
            total += p["subtotal"]

    display_products.sort(key=lambda p: p["name"])

    return render(request, "cart.html", context={"products": display_products, "total": total / 100})
