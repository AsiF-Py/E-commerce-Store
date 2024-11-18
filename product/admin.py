from django.contrib import admin
from .models import Category,Product,Images



class ImageInline(admin.TabularInline):  # or admin.StackedInline
    model = Images
    extra = 3
    template = 'admin/edit_inline/image_tabular.html'
# @admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
# @admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','category','price','is_available',]
    inlines = [ImageInline]
    list_editable = ['price']




from unfold.admin import ModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm
class ExampleAdmin(ModelAdmin, ProductAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm

admin.site.register(Product, ExampleAdmin)

class ExampleCategoryAdmin(ModelAdmin, CategoryAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm

admin.site.register(Category, ExampleCategoryAdmin)