from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    #path('login/', views.user_login, name='login')
    path('login/',auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/',auth_views.LogoutView.as_view(), name='logout'),
    path('password-change/',auth_views.PasswordChangeView.as_view(template_name='account/password_change.html'), name='password_change'),
    path('password-change/done/',auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password-reset/', views.direct_password_reset, name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/',auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('check-email/', views.check_email_exists, name='check_email_exists'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('profile/', views.profile_view, name='profile'),
    path('history/', views.order_history, name='history'),
]

