from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe
from .models import Category, Product

# Eliminar el apartado de Grupos
admin.site.unregister(Group)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    list_filter = ['name']
    readonly_fields = []

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        # Ocultar botones innecesarios
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        return super().changeform_view(request, object_id, form_url, extra_context)

    class Media:
        js = ('admin/js/slug_sync.js',)

@admin.register(Product)
# Custom Product Admin
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ['image_preview']

    fieldsets = (
        ('Información General', {
            'fields': ('category', 'name', 'slug', 'description')
        }),
        ('Imagen del Producto', {
            'fields': ('image_preview', 'image')
        }),
        ('Precios y Stock', {
            'fields': ('price', 'stock', 'available')
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" class="admin-image-preview"/>')
        return "No hay imagen cargada"

    image_preview.short_description = 'Vista previa actual'

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        # Ocultar botones innecesarios
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        return super().changeform_view(request, object_id, form_url, extra_context)

    class Media:
        js = ('admin/js/slug_sync.js',)
        css = {
            'all': ('admin/css/admin_styles.css',)
        }
    list_display = ['name', 'slug', 'price', 'stock', 'available', 'created', 'updated']
    list_filter = ['category', 'available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available']