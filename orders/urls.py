from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('api/pending-count/', views.pending_orders_count, name='pending_orders_count'),
    path('admin/monitor/', views.admin_notifications_dashboard, name='admin_notifications'),
]