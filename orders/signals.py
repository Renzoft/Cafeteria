from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.contenttypes.models import ContentType
from .models import Order

@receiver(post_save, sender=Order)
def log_order_creation(sender, instance, created, **kwargs):
    if created:
        # Intentar obtener el tipo de contenido para el modelo Order
        content_type = ContentType.objects.get_for_model(instance)
        
        # Loguear la creación del pedido en el historial de administración
        # Usamos el usuario asociado al pedido si existe, de lo contrario nada
        # Nota: LogEntry requiere un user_id, así que si no hay usuario, 
        # podríamos usar un usuario de sistema o simplemente no loguear.
        # Pero el usuario suele estar (el cliente).
        
        # Para que aparezca en el dashboard del administrador, el LogEntry debe estar 
        # asociado a un usuario con permisos de staff/admin. 
        # Si el pedido es de un cliente (no staff), lo logueamos a nombre del primer superusuario
        # para que sea visible en el feed de actividad global del admin.
        
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # Prioridad: Si el usuario que hizo el pedido es staff, usarlo. 
        # Si no, buscar el primer superusuario disponible.
        log_user = None
        if instance.user and instance.user.is_staff:
            log_user = instance.user
        else:
            log_user = User.objects.filter(is_superuser=True).first()
        
        if log_user:
            from django.utils import timezone
            LogEntry.objects.create(
                user_id=log_user.id,
                content_type_id=content_type.pk,
                object_id=str(instance.pk),
                object_repr=str(instance),
                action_flag=ADDITION,
                change_message=f"Pedido #{instance.id} realizado por {instance.first_name} {instance.last_name}",
                action_time=timezone.now()
            )
