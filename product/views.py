from django.shortcuts import render
from .models import Product,Images
from cart.models import Cart
# Create your views here.
def product_list(request):
    product_list = Product.objects.filter(is_available=True)
    if request.user.is_authenticated:
        my_cart = Cart.objects.filter(user=request.user)
        all_total_sub_price = sum(cart.total() for cart in my_cart)
        return render(request, 'product/product_list.html',
                      {'product_list': product_list, 'my_cart': my_cart, 'all_total_sub_price': all_total_sub_price})
    return render(request,'product/product_list.html',{'product_list':product_list})