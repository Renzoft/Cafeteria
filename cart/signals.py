from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.conf import settings
from .models import Cart, CartItem
from mitienda.models import Product

@receiver(user_logged_in)
def merge_session_cart_to_db(sender, user, request, **kwargs):
    session_cart = request.session.get(settings.CART_SESSION_ID)
    if not session_cart:
        return

    db_cart, _ = Cart.objects.get_or_create(user=user)

    for product_id, item_data in session_cart.items():
        try:
            product = Product.objects.get(id=int(product_id))
            quantity = item_data.get('quantity', 0)
            
            db_item, created = CartItem.objects.get_or_create(cart=db_cart, product=product)
            if not created:
                db_item.quantity += quantity
            else:
                db_item.quantity = quantity
            db_item.save()
        except Product.DoesNotExist:
            continue

    del request.session[settings.CART_SESSION_ID]
    request.session.modified = True
