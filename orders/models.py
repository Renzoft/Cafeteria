from django.db import models
from mitienda.models import Product
from django.conf import settings


class Order(models.Model):
    STATUS_CHOICES = (
        ('Pendiente', 'Pendiente'),
        ('Listo', 'Listo para recoger'),
        ('Entregado', 'Entregado'),
        ('Cancelado', 'Cancelado'),
    )
    first_name = models.CharField(max_length=100, verbose_name='nombre')
    last_name = models.CharField(max_length=100, verbose_name='apellidos')
    email = models.EmailField(verbose_name='correo electrónico')
    phone = models.CharField(max_length=20, blank=True, verbose_name='teléfono')
    reference_address = models.CharField(max_length=250, blank=True, verbose_name='dirección de referencia')
    created = models.DateTimeField(auto_now_add=True, verbose_name='creado')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pendiente', verbose_name='estado')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='usuario')

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

    def __str__(self):
        return f'Order {self.id}'
        
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name='pedido')
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE, verbose_name='producto')
    price = models.DecimalField(max_digits=5,
                                decimal_places=2, verbose_name='precio')
    quantity = models.PositiveIntegerField(default=1, verbose_name='cantidad')

    class Meta:
        verbose_name = 'Artículo de pedido'
        verbose_name_plural = 'Artículos de pedido'

    def __str__(self):
        return str(self.id)
        
    def get_cost(self):
        return self.price * self.quantity