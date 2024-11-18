from cart.models import Cart
from django import template


register = template.Library()

@register.filter
def in_cart(product,user):
    return user.cart_set.filter(products=product).exists()

@register.filter
def in_wishlist(product,user):
    return user.wishlist_set.filter(products=product).exists()

