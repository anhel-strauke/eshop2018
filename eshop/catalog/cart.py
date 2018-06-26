from .models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session

    def add_product(self, product):
        cart_data = self.session.get("cart", {})
        prod_id = str(product.id)
        if prod_id in cart_data:
            q = cart_data[prod_id]
        else:
            q = 0
        self.update_product(product, q + 1)

    def update_product(self, product, quantity):
        cart_data = self.session.get("cart", {})
        prod_id = str(product.id)
        if quantity <= 0:
            if prod_id in cart_data:
                del cart_data[prod_id]
        else:
            cart_data[prod_id] = quantity

        cart_sum = 0
        for product_id, quant in cart_data.items():
            try:
                prod = Product.objects.get(id=int(product_id))
            except Product.DoesNotExist:
                continue
            cart_sum += prod.price * quant

        self.session["cart"] = cart_data
        self.session["cartsum"] = cart_sum / 100

    def products(self):
        result = []
        cart_data = self.session.get("cart", {})
        for product_id, quantity in cart_data.items():
            try:
                prod = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                continue
            result.append({"product": prod, "quantity": quantity, "subtotal": prod.price * quantity})
        return result

    def quantity_by_id(self, product_id):
        cart_data = self.session.get("cart", {})
        return cart_data.get(str(product_id), 0)

    def clear(self):
        self.session["cart"] = {}
        self.session["cartsum"] = 0