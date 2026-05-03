from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
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

@staff_member_required
def pending_orders_count(request):
    """
    Endpoint mejorado que devuelve el conteo y una lista de los pedidos más recientes.
    """
    pending_orders = Order.objects.filter(status='Pendiente')
    count = pending_orders.count()
    last_order = pending_orders.order_by('-created').first()
    
    # Lista detallada para el monitor en vivo
    orders_list = []
    for o in pending_orders.order_by('-created')[:12]:
        orders_list.append({
            'id': o.id,
            'user_name': f"{o.first_name} {o.last_name}",
            'created': o.created.strftime('%H:%M:%S'),
        })
    
    data = {
        'count': count,
        'last_id': last_order.id if last_order else None,
        'last_user': f"{last_order.first_name} {last_order.last_name}" if last_order else "",
        'orders': orders_list,
    }
    return JsonResponse(data)
@staff_member_required
def admin_notifications_dashboard(request):
    return render(request, 'admin/orders/notifications.html')
