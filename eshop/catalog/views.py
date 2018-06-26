from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from hashlib import md5
from datetime import datetime
from random import randint
from .cart import Cart
from .forms import CheckoutForm
from .models import Category, Product, Order, OrderedProduct, OrderStatus


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
    return HttpResponseRedirect(reverse("cart_view"))


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
            return HttpResponseRedirect(reverse("main_view"))
        elif "do_order" in request.POST:
            return HttpResponseRedirect(reverse("checkout_view"))

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


def make_order_code(person_name):
    source_str = "{pn}{dt}{r}".format(pn=person_name, dt=datetime.now().isoformat(), r=randint(100000, 999999))
    hash_func = md5()
    hash_func.update(source_str.encode("utf-8"))
    return hash_func.hexdigest()

def checkout_view(request):
    cart = Cart(request)
    if cart.is_empty():
        return HttpResponseRedirect(reverse("cart_view"))
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order_code = make_order_code(form.cleaned_data["person_name"])
            try:
                order_status = OrderStatus(id=1)
            except:
                order_status = None
            order = Order(
                code=order_code, 
                person_name=form.cleaned_data["person_name"],
                person_email=form.cleaned_data["person_email"],
                person_phone=form.cleaned_data["person_phone"],
                person_address=form.cleaned_data["person_address"],
                notes=form.cleaned_data["notes"],
                status=order_status)
            order.save()
            for prod in cart.products():
                ordered_product = OrderedProduct(
                    order=order, 
                    product=prod["product"], 
                    quantity=prod["quantity"],
                    price=prod["product"].price)
                ordered_product.save()
            context = {
                "order_id": order.id,
                "person_email": form.cleaned_data["person_email"],
                "order_code": order_code,
            }
            cart.clear()

            # TODO: Отправка писем (покупателю и менеджеру)

            return render(request, "checkout_done.html", context=context)
    else:
        form = CheckoutForm()

    total = cart.total()
    return render(request, "checkout.html", context={"form": form, "total": total / 100})
