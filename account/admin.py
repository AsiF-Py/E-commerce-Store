from django.contrib import admin
from .models import Account,Address
# Register your models here.

# @admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['email']

# @admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass


from unfold.admin import ModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm
class ExampleAdmin(ModelAdmin, AccountAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm

class ExampleAddressAdmin(ModelAdmin, AddressAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm

admin.site.register(Account, ExampleAdmin)
admin.site.register(Address, ExampleAddressAdmin)

from django.contrib.auth.models import Group

admin.site.unregister(Group)