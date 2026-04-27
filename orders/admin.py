from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'phone', 'reference_address', 'status',
                    'created']
    list_filter = ['status', 'created']
    list_editable = ['status']
    inlines = [OrderItemInLine]
    