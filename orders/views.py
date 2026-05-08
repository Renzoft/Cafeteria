from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from cart.cart import Cart
from .models import Order, OrderItem
from .forms import OrderCreateForm


def generate_qr_base64(url):
    """Genera un código QR como imagen Base64 a partir de una URL."""
    import qrcode
    import io
    import base64

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=8,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="#4a3324", back_color="#ffffff")

    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return base64.b64encode(buffer.getvalue()).decode('utf-8')


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

                # Generar QR para la página de confirmación
                from django.urls import reverse
                validate_path = reverse('orders:order_receipt', args=[order.validation_token])
                validate_url = request.build_absolute_uri(validate_path)
                qr_base64 = generate_qr_base64(validate_url)

                return render(request, 'orders/created.html', {
                    'order': order,
                    'qr_base64': qr_base64,
                })
    else:
        form = OrderCreateForm(initial=initial_data)
            
    return render(request, 'orders/create.html', {'cart': cart, 'form': form})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Generar QR solo si el pedido no ha sido entregado ni cancelado
    qr_base64 = None
    if order.status not in ('Entregado', 'Cancelado'):
        from django.urls import reverse
        validate_path = reverse('orders:order_receipt', args=[order.validation_token])
        validate_url = request.build_absolute_uri(validate_path)
        qr_base64 = generate_qr_base64(validate_url)

    return render(request, 'orders/detail.html', {
        'order': order,
        'qr_base64': qr_base64,
    })


def order_receipt(request, token):
    """
    Vista pública de solo lectura que funciona como comprobante digital.
    No requiere inicio de sesión, usa el token UUID como seguridad.
    """
    order = get_object_or_404(Order, validation_token=token)
    return render(request, 'orders/receipt.html', {'order': order})



