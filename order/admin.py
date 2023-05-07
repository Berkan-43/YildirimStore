from django.contrib import admin
from order.models import *
# Register your models here.


class OrderProductInline(admin.TabularInline):
    model = OrderItemModel
    extra = 0

@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    list_display        = ["order_number","order_total","status","is_ordered"]
    list_display_links  = ["order_number"]
    inlines             = [OrderProductInline]

    class Meta:
        model = OrderModel


@admin.register(OrderItemModel)
class OrderItemModelAdmin(admin.ModelAdmin):
    list_display       = ["user","order","product","amount","created_add"]
    list_display_links = ["user","order"]
    list_filter        = ["order","user"]
    class Meta:
        model = OrderItemModel