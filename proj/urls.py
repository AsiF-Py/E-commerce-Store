from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('account.urls')),
    path("", include("allauth.urls")),
    path('', include('product.urls')),
    path('', include('cart.urls')),
    path('', include('order.urls')),
    path('', include('coupons.urls')),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)