from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    reference_address = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return f'Perfil de {self.user.username}'
