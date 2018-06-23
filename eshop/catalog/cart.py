from .models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session

    def update_product(self, product, quantity):
        cart_data = request.session.get("cart", {})
        #cart_sum = request.session.get("cartsum", 0)
        if quantity <= 0:
            if product.id in cart_data:
                del cart_data[product.id]
        elif product.id in cart_data:
            cart_data[product.id] += quantity
        else:
            cart_data[product.id] = quantity

        cart_sum = 0
        for product_id, quant in cart_data.items():
            try:
                prod = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                continue
            cart_sum += prod.price * quant

        self.session["cart"] = cart_data
        self.session["cartsum"] = cart_sum

    def products(self):
        result = []
        cart_data = request.session.get("cart", {})
        for product_id, quantity in cart_data:
            try:
                prod = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                continue
            result.append({"product": product, "quantity": quantity})
        return result

    def clear(self):
        self.session["cart"] = {}
        self.session["cartsum"] = 0