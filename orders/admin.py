from django.contrib import admin
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
        # Restaurar stock antes de eliminar
        for item in obj.items.all():
            product = item.product
            product.stock += item.quantity
            if product.stock > 0:
                product.available = True
            product.save()
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        # Restaurar stock para todos los pedidos seleccionados
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
    