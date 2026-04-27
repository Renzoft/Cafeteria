from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from cart.cart import Cart
from .models import Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import OrderCreateForm

@login_required
def order_create(request):
    cart = Cart(request)
    if not cart:
        return redirect('cart:cart_detail')
        
    profile = getattr(request.user, 'profile', None)
    initial_data = {
        'first_name': request.user.first_name or request.user.username,
        'last_name': request.user.last_name,
        'email': request.user.email,
        'phone': profile.phone if profile else '',
        'reference_address': profile.reference_address if profile else '',
    }
        
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                for item in cart:
                    if item['quantity'] > item['product'].stock:
                        messages.error(request, f"No hay suficiente stock para '{item['product'].name}'.")
                        return redirect('cart:cart_detail')
                
                order = form.save(commit=False)
                order.user = request.user
                order.save()
                
                for item in cart:
                    product = item['product']
                    OrderItem.objects.create(order=order,
                                             product=product,
                                             price=item['price'],
                                             quantity=item['quantity'])
                    product.stock -= item['quantity']
                    if product.stock <= 0:
                        product.stock = 0
                        product.available = False
                    product.save()
                    
                cart.clear()
                return render(request, 'orders/created.html', {'order': order})
    else:
        form = OrderCreateForm(initial=initial_data)
            
    return render(request, 'orders/create.html', {'cart': cart, 'form': form})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/detail.html', {'order': order})