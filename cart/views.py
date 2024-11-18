from django.shortcuts import render,redirect
from product.models import Product
from .models import Cart,Wishlist
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.conf import settings
from coupons.forms import CouponApplyForm
from coupons.models import Coupon
from decimal import Decimal
# Create your views here.
@login_required
def cart(request,product_id):
    product = Product.objects.get(id=product_id)
    quantity = request.GET.get('quantity', 1)
    cart = Cart.objects.create(products=product,user=request.user,quantity=quantity)
    return redirect('product_list')
@login_required
def my_cart(request):
    cart_list = Cart.objects.filter(user=request.user)
    all_total_sub_price = sum(cart.total() for cart in cart_list)

    shipping_fe = settings.DELIVERY_FEES
    all_total_price = shipping_fe + all_total_sub_price
    coupon_apply_form = CouponApplyForm()
    if request.session.get('coupon_id'):
        coupon_id = request.session.get('coupon_id')
        coupon = Coupon.objects.get(id=coupon_id)
        apply_coupon = coupon.discount / Decimal(100) * all_total_price

    return render(request,'cart/my_cart.html',{'cart_list':cart_list,
                                               'all_total_sub_price':all_total_sub_price,
                                               'all_total_price':all_total_price,
                                               'coupon_apply_form' : coupon_apply_form,
                                               'apply_coupon':apply_coupon
                                               })
@login_required
def cart_delete(request,cart_id):
    cart = Cart.objects.get(id=cart_id)
    cart.delete()
    return redirect('product_list')
@login_required
def wishlist(request):
    wishlist = Wishlist.objects.filter(user=request.user)

    return render(request,'cart/wishlist.html',{'wishlist':wishlist})
@login_required
def create_wishlist(request,product_id):
    product = Product.objects.get(id=product_id)
    Wishlist.objects.create(products=product,user=request.user)
    return redirect('wishlist')


# myapp/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # Use this decorator if you want to disable CSRF protection for this view during development. In production, handle CSRF properly.
def my_ajax_view(request):


    if request.method == 'POST':
        cart_id = request.POST.get('cart_id')
        quantity = request.POST.get('quantity')
        cart = Cart.objects.get(id=cart_id)
        cart.quantity = quantity
        cart.save()
        total_value = cart.total()


        sub_total = Cart.objects.filter(user=request.user)
        all_total_sub_price = sum(cart.total() for cart in sub_total)

        shipping_fe = settings.DELIVERY_FEES
        all_total_price = shipping_fe + all_total_sub_price


        response_data = {
            'message': f'Updated value received successfully for cart {cart_id} {total_value}',
            'total': total_value,
            'all_total_sub_price':all_total_sub_price,
            'all_total_price' : all_total_price,

        }
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Invalid request method'})





