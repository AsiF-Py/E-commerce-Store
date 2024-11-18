from .models import Cart,Wishlist
from django.conf import settings
def cart_count(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        wistlist = Wishlist.objects.filter(user=request.user)
        return {'cart_count':cart.count,'wistlist':wistlist.count,'DELIVERY_FEES':settings.DELIVERY_FEES}
    return {'cart_count':0,'wistlist':0,'DELIVERY_FEES':settings.DELIVERY_FEES}