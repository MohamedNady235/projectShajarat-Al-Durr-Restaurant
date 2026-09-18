from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('gallery/', views.gallery, name='gallery'),
    path('reserve/', views.reserve_table, name='reserve-table'),
    path('contact/', views.contact, name='contact'),
    path('menu/', views.menu_list, name='menu-list'),
    path('menu/<int:menu_item_id>/', views.menu_detail, name='menu-detail'),
    path('orders/place/', views.place_order, name='place-order'),
    path('orders/<int:order_id>/confirmation/', views.order_confirmation, name='order_confirmation'),
]
