from django.contrib import admin
from product.models import *
from mptt.admin import DraggableMPTTAdmin
# Register your models here.

class ProductImagesInline(admin.TabularInline):
    model = Images
    extra = 5

class CategoryAdmin2(admin.ModelAdmin):
    list_display = [
        'title',
        'status',
    ]



class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "productTitle"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Product,
                'productCategorie',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Product,
                 'productCategorie',
                 'products_count',
                 cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'

admin.site.register(Campaigns)
admin.site.register(Tag)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'productTitle',
        'productPrice',
        'productShipping',
    ]

    search_fields = (
        'productTitle',
        'productPrice',
    )
    inlines = [ProductImagesInline]

@admin.register(ProductVariationModel)
class ProductVariationAdmin(admin.ModelAdmin):
    list_display        = ["product","variation_category","variation_value"]
    list_display_links  = ["product",]

    class Meta:
        model = ProductVariationModel

@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    list_display = (
        'title', 
        'product',
        'image',
    )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'subject',
        'comment',
        'status'
    )
    list_filter = (
        'status',
    )

admin.site.register(Category, CategoryAdmin2)