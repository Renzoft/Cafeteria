from django import forms
from django.contrib.auth.models import User
from .models import Profile

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class UserRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(label='Nombres', required=True)
    last_name = forms.CharField(label='Apellidos', required=True)
    email = forms.EmailField(label='Correo electrónico', required=True, validators=[validate_email])
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Repite la contraseña', widget=forms.PasswordInput, required=True)
    
    # Campos adicionales para el Profile
    date_of_birth = forms.DateField(label='Fecha de nacimiento', widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}), required=True)
    phone = forms.CharField(label='Teléfono', max_length=20, required=True)
    reference_address = forms.CharField(label='Dirección de referencia', max_length=250, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'Nombre de usuario',
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return cd['password2']
    
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'email': 'Correo electrónico'
        }

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo', 'phone', 'reference_address']
        labels = {
            'date_of_birth': 'Fecha de nacimiento',
            'photo': 'Foto de perfil',
            'phone': 'Teléfono',
            'reference_address': 'Dirección de referencia'
        }
        widgets = {
            'date_of_birth': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }

class DirectPasswordResetForm(forms.Form):
    email = forms.EmailField(label='Correo electrónico')
    password = forms.CharField(label='Nueva contraseña', widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Repite la nueva contraseña', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data