from django.urls import path
from . import views


urlpatterns = [
    path('', views.store, name='index'),
    path('home/', views.store, name='index'),
    path('shop/', views.shop, name='shop'),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('product/<int:pk>/', views.shop_single, name='shop-single'),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('contact/', views.contact, name="contact"),

    path('product/<int:pk>/review/', views.item_detail, name='item-detail'),
    path('product/<int:pk>/addreview/', views.add_review, name='add-review'),
]