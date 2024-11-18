from django.urls import path
from . import views

urlpatterns = [
    path('cart/<int:product_id>/',views.cart,name='cart'),
    path('my-cart/',views.my_cart,name='my_cart'),
    path('cart/remove/<int:cart_id>/',views.cart_delete,name='cart_delete'),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('add-wishlist/<int:product_id>/', views.create_wishlist),

    path('my-ajax-view/', views.my_ajax_view, name='my_ajax_view'),

]