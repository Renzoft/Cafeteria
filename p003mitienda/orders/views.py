from django.shortcuts import render

from cart.cart import Cart
from .forms import OrderCreateForm
from .models import OrderItem

from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            for item in cart:
                if item['quantity'] > item['product'].stock:
                    messages.error(request, f"No hay suficiente stock para '{item['product'].name}'.")
                    return redirect('cart:cart_detail')
                
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for item in cart:
                product = item['product']
                OrderItem.objects.create(order = order,
                                         product = product,
                                         price = item['price'],
                                         quantity = item['quantity'])
                product.stock -= item['quantity']
                if product.stock <= 0:
                    product.stock = 0
                    product.available = False
                product.save()
            cart.clear()
            return render(request,
                          'orders/created.html',
                          {'order':order})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/create.html', {'form':form, 'cart':cart})