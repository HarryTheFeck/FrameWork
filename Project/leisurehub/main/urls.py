from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('', lambda request: redirect('login')),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('activities/', views.activity_list, name='activities'),
    path('items/', views.item_list, name='items'),
    path('book/<int:id>/', views.book_activity, name='book_activity'),
    path('order/<int:id>/', views.order_item, name='order_item'),
    path('coordinator/activities/', views.coordinator_activities, name='coordinator_activities'),
    path('coordinator/activities/create/', views.create_activity, name='create_activity'),
    path('manager/orders/', views.manage_orders, name='manage_orders'),
    path('manager/orders/update/<int:order_id>/', views.update_order_status, name='update_order_status'),
]
