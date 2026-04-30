from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE, verbose_name='usuario')
    date_of_birth = models.DateField(blank=True, null=True, verbose_name='fecha de nacimiento')
    photo = models.ImageField(upload_to='', blank=True, null=True, verbose_name='foto')
    phone = models.CharField(max_length=20, blank=True, verbose_name='teléfono')
    reference_address = models.CharField(max_length=250, blank=True, verbose_name='dirección de referencia')

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'

    def __str__(self):
        return f'Perfil de {self.user.username}'
