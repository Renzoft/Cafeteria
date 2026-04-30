from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='nombre')
    slug = models.SlugField(max_length=200, verbose_name='slug')

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
        ]

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('tienda:product_list_category',
                       args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE,
                                 verbose_name='categoría')
    name = models.CharField(max_length=200, verbose_name='nombre')
    slug = models.SlugField(max_length=200, verbose_name='slug')
    image = models.ImageField(upload_to='',
                              blank=True, verbose_name='imagen')
    description = models.TextField(blank=True, verbose_name='descripción')
    price = models.DecimalField(max_digits=5,
                                decimal_places=2, verbose_name='precio')
    stock = models.PositiveIntegerField(default=0, verbose_name='stock')
    available = models.BooleanField(default=True, verbose_name='disponible')
    created = models.DateTimeField(auto_now=True, verbose_name='creado')
    updated = models.DateTimeField(auto_now_add=True, verbose_name='actualizado')

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('tienda:product_detail',
                       args=[self.id,self.slug])