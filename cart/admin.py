from django.contrib import admin
from .models import Cart,Wishlist
# Register your models here.
# @admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    pass

# @admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    pass

from unfold.admin import ModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm
class ExampleAdmin(ModelAdmin, CartAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm

class ExampleWishlistAdmin(ModelAdmin, WishlistAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm

admin.site.register(Cart, ExampleAdmin)
admin.site.register(Wishlist, ExampleWishlistAdmin)