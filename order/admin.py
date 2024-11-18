from django.contrib import admin
from .models import Order, OrderItem
from django.shortcuts import reverse
from django.utils.html import mark_safe


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    readonly_fields = ['product', 'price', 'quantity',]
    extra = 0
    template = 'admin/edit_inline/tabular.html'




# @admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'paid', 'total_amount' ,'created_at', 'updated_at']
    list_filter = ['paid', 'created_at', 'updated_at']
    search_fields = ['user']
    ordering = ['-created_at']
    inlines = [OrderItemInline]
    readonly_fields = ['total_amount',]


    def total_amount(self, obj):
        return sum(item.total() for item in obj.items.all())

    # def order_pdf(obj):
    #     url = reverse('orders:admin_order_pdf', args=[obj.id])
    #     return mark_safe(f'<a href="{url}">PDF</a>')
    # order_pdf.short_description = 'Invoice'



    total_amount.short_description = 'Total Amount'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        obj = Order.objects.get(id=object_id)
        extra_context['custom_data'] = sum(item.total() for item in obj.items.all())
        extra_context['quantity'] = sum(item.quantity for item in obj.items.all())
        extra_context['obj'] = obj
        return super().change_view(request, object_id, form_url, extra_context=extra_context)


from unfold.admin import ModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm
class ExampleAdmin(ModelAdmin, OrderAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm

admin.site.register(Order, ExampleAdmin)