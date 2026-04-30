from django.shortcuts import render, redirect
from django.contrib.auth  import authenticate, login
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from .forms import UserRegistrationForm, UserEditForm, LoginForm, ProfileEditForm, DirectPasswordResetForm
from .models import Profile

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, 
                                username=cd['username'], 
                                password = cd['password']) 
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Usuario autenticado')
                else:
                    return HttpResponse('Usuario inactivo')
            else:
                return HttpResponse('Usuario no encontrado')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form':form})

@login_required
def profile_view(request):
    Profile.objects.get_or_create(user=request.user)
    return render(request, 'account/profile.html', {'section':'profile'})

@login_required
def order_history(request):
    orders = request.user.order_set.all().order_by('-created')
    return render(request, 'account/history.html', {'section':'history', 'orders': orders})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(
                user=new_user,
                date_of_birth=user_form.cleaned_data.get('date_of_birth'),
                phone=user_form.cleaned_data.get('phone'),
                reference_address=user_form.cleaned_data.get('reference_address')
            )
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form':user_form})

@login_required
def edit(request):
    Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Perfil actualizado', 'succesful')
        else:
            messages.error(request, 'Error al actualizar el perfil')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html',{
        'user_form':user_form,
        'profile_form':profile_form
    })

def direct_password_reset(request):
    if request.method == 'POST':
        form = DirectPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            new_password = form.cleaned_data['password']
            try:
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Tu contraseña ha sido restablecida con éxito. Ahora puedes iniciar sesión.')
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'No existe ningún usuario con este correo electrónico.')
    else:
        form = DirectPasswordResetForm()
    return render(request, 'account/password_reset_direct.html', {'form': form})

def check_email_exists(request):
    email = request.GET.get('email', '')
    exists = User.objects.filter(email=email).exists() if email else False
    return JsonResponse({'exists': exists})

def check_username_exists(request):
    username = request.GET.get('username', '')
    exists = User.objects.filter(username=username).exists() if username else False
    return JsonResponse({'exists': exists})