from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django import forms
from .models import Profile
from .forms import UserRegistrationForm

class AdminUserCreationForm(UserRegistrationForm):
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            if hasattr(self, 'save_m2m'):
                self.save_m2m()
        return user

from django.core.validators import validate_email

class UserProfileForm(forms.ModelForm):
    email = forms.EmailField(label='Correo electrónico', required=True, validators=[validate_email])
    date_of_birth = forms.DateField(required=True, label='Fecha de nacimiento', widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))
    photo = forms.ImageField(required=False, label='Foto') # Photo is usually optional but we can leave it False
    phone = forms.CharField(max_length=20, required=True, label='Teléfono')
    reference_address = forms.CharField(max_length=250, required=True, label='Dirección de referencia')

    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'is_active' in self.fields:
            self.fields['is_active'].label = "Cuenta Activa"
            self.fields['is_active'].help_text = "Desmarque esto para bloquear el acceso al usuario sin eliminar su cuenta."
        if 'is_staff' in self.fields:
            self.fields['is_staff'].label = "Acceso al Panel (Staff)"
            self.fields['is_staff'].help_text = "Permite al usuario entrar a este panel de administración."
        if 'is_superuser' in self.fields:
            self.fields['is_superuser'].label = "Super Administrador"
            self.fields['is_superuser'].help_text = "Otorga todos los permisos del sistema sin restricciones."

        if self.instance and self.instance.pk:
            try:
                profile = self.instance.profile
                self.fields['date_of_birth'].initial = profile.date_of_birth
                self.fields['photo'].initial = profile.photo
                self.fields['phone'].initial = profile.phone
                self.fields['reference_address'].initial = profile.reference_address
            except Profile.DoesNotExist:
                pass

class CustomUserAdmin(BaseUserAdmin):
    form = UserProfileForm
    add_form = AdminUserCreationForm
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = []
    ordering = ('username',)

    readonly_fields = ('last_login', 'date_joined')

    class Media:
        js = ('admin/js/slug_sync.js',)
        css = {
            'all': ('admin/css/admin_styles.css',)
        }
    
    fieldsets = (
        ('Credenciales de Acceso', {
            'fields': ('username', 'password'),
            'classes': ('wide',),
        }),
        ('Información Personal', {
            'fields': (
                ('first_name', 'last_name'),
                ('email', 'phone'),
                ('date_of_birth', 'reference_address'),
                'photo',
            ),
        }),
        ('Estado y Roles', {
            'fields': (
                'is_active', 
                'is_staff', 
                'is_superuser'
            ),
            'description': 'Configure si este usuario tendrá acceso administrativo al sistema o será un cliente regular.'
        }),
        ('Fechas de Registro', {
            'fields': (
                'last_login', 
                'date_joined'
            ),
            'description': 'Información sobre la actividad del usuario en el sistema.'
        }),
    )
    filter_horizontal = ('groups', 'user_permissions')

    add_fieldsets = (
        ('Crear nuevo usuario', {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'email', 'password', 'password2', 'date_of_birth', 'phone', 'reference_address'),
        }),
    )

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save_and_add_another': False,
            'show_save_and_continue': False,
        })
        return super().render_change_form(request, context, add, change, form_url, obj)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        
        profile, created = Profile.objects.get_or_create(user=obj)
        
        if 'date_of_birth' in form.cleaned_data:
            profile.date_of_birth = form.cleaned_data.get('date_of_birth')
        if 'photo' in form.cleaned_data and form.cleaned_data.get('photo'):
            profile.photo = form.cleaned_data.get('photo')
        if 'phone' in form.cleaned_data:
            profile.phone = form.cleaned_data.get('phone')
        if 'reference_address' in form.cleaned_data:
            profile.reference_address = form.cleaned_data.get('reference_address')
            
        profile.save()

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)