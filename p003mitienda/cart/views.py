from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages

from mitienda.models import Product
from .forms import CartAddProductForm
from .cart import Cart

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    if product.stock <= 0:
        messages.error(request, f"Lo sentimos, el producto '{product.name}' está agotado.")
        return redirect('cart:cart_detail')
    
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cantidad_solicitada = cd['cantidad']
        if cantidad_solicitada > product.stock:
            messages.error(request, f"Solo hay {product.stock} unidades disponibles de '{product.name}'.")
            return redirect('cart:cart_detail')
        
        cart.add(product=product,
                 quantity=cd['cantidad'],
                 override_quantity=cd['override'])
    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_details(request):
    cart = Cart(request)
    return render(request, 'cart/details.html', {'cart':cart})