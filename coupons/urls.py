from django.urls import path
from . import views


urlpatterns = [
    path('apply-coupons/',views.coupon_apply,name='apply_coupons'),
    ]