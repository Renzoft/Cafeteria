from decimal import Decimal
from django.conf import settings
from mitienda.models import Product
from .models import Cart as DBCart, CartItem

class Cart:
    def __init__(self, request):
        self.session = request.session
        self.request = request
        self.user = request.user
        
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.session_cart = cart

        if self.user.is_authenticated:
            self.db_cart, _ = DBCart.objects.get_or_create(user=self.user)

    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        
        if self.user.is_authenticated:
            item, created = CartItem.objects.get_or_create(cart=self.db_cart, product=product)
            if override_quantity:
                item.quantity = quantity
            else:
                if not created:
                    item.quantity += quantity
                else:
                    item.quantity = quantity
            item.save()
        else:
            if product_id not in self.session_cart:
                self.session_cart[product_id] = {'quantity': 0, 'price': str(product.price)}
            if override_quantity:
                self.session_cart[product_id]['quantity'] = quantity
            else:
                self.session_cart[product_id]['quantity'] += quantity
            self.save_session()

    def save_session(self):
        self.session.modified = True

    def remove(self, product):
        if self.user.is_authenticated:
            CartItem.objects.filter(cart=self.db_cart, product=product).delete()
        else:
            product_id = str(product.id)
            if product_id in self.session_cart:
                del self.session_cart[product_id]
                self.save_session()

    def __iter__(self):
        if self.user.is_authenticated:
            items = self.db_cart.items.select_related('product').all()
            for item in items:
                yield {
                    'product': item.product,
                    'quantity': item.quantity,
                    'price': Decimal(item.product.price),
                    'total_price': Decimal(item.product.price) * item.quantity
                }
        else:
            product_ids = self.session_cart.keys()
            products = Product.objects.filter(id__in=product_ids)
            cart = self.session_cart.copy()
            for product in products:
                cart[str(product.id)]['product'] = product
            for item in cart.values():
                item['price'] = Decimal(item['price'])
                item['total_price'] = item['price'] * item['quantity']
                yield item

    def __len__(self):
        if self.user.is_authenticated:
            return sum(item.quantity for item in self.db_cart.items.all())
        else:
            return sum(item['quantity'] for item in self.session_cart.values())
    
    def get_total_price(self):
        if self.user.is_authenticated:
            return sum(Decimal(item.product.price) * item.quantity for item in self.db_cart.items.select_related('product').all())
        else:
            return sum(Decimal(item['price']) * item['quantity'] for item in self.session_cart.values())
    
    def clear(self):
        if self.user.is_authenticated:
            self.db_cart.items.all().delete()
        else:
            if settings.CART_SESSION_ID in self.session:
                del self.session[settings.CART_SESSION_ID]
                self.save_session()