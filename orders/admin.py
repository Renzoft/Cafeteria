from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from django.template.response import TemplateResponse
from .models import Order, OrderItem


class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'phone', 'status', 'created', 'delete_button']
    list_filter = ['status', 'created']
    list_editable = ['status']
    inlines = [OrderItemInLine]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'monitor/',
                self.admin_site.admin_view(self.monitor_view),
                name='orders_order_monitor',
            ),
            path(
                'api/pending-count/',
                self.admin_site.admin_view(self.pending_count_api),
                name='orders_order_pending_count',
            ),
        ]
        return custom_urls + urls

    def monitor_view(self, request):
        """Vista del Monitor de Pedidos en tiempo real."""
        context = {
            **self.admin_site.each_context(request),
            'title': 'Monitor de Pedidos',
            'opts': self.model._meta,
        }
        return TemplateResponse(
            request,
            'admin/orders/notifications.html',
            context,
        )

    def pending_count_api(self, request):
        """
        Endpoint JSON para el polling de notificaciones.
        Ahora vive bajo /admin/ para que el middleware de sesión lo procese correctamente.
        """
        pending_orders = Order.objects.filter(status='Pendiente')
        count = pending_orders.count()
        last_order = pending_orders.order_by('-created').first()

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

    def delete_button(self, obj):
        from django.urls import reverse
        from django.utils.html import format_html
        url = reverse('admin:orders_order_delete', args=[obj.id])
        return format_html(
            '<a class="btn btn-sm btn-danger" href="{}" style="padding: 2px 10px; font-weight: 600;">'
            '<i class="fas fa-trash"></i> Eliminar</a>',
            url
        )
    delete_button.short_description = 'Acciones'

    def delete_model(self, request, obj):
        for item in obj.items.all():
            product = item.product
            product.stock += item.quantity
            if product.stock > 0:
                product.available = True
            product.save()
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            for item in obj.items.all():
                product = item.product
                product.stock += item.quantity
                if product.stock > 0:
                    product.available = True
                product.save()
        super().delete_queryset(request, queryset)

    class Media:
        js = ('admin/js/slug_sync.js',)
        css = {
            'all': ('admin/css/admin_styles.css',)
        }