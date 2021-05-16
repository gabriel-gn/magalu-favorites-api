from django.contrib import admin

from .models import *


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'price', 'brand', 'reviews', 'created', 'modified')
    # list_filter = ()
    # search_fields = ()
    ordering = ('-modified', '-created')

    def reviews(self, obj):
        """
        Retorna a quantidade de reviews para este produto
        """
        return len(ProductReview.objects.filter(product=obj))


@admin.register(ProductBrand)
class ProductBrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'created', 'modified')
    # list_filter = ()
    # search_fields = ()
    ordering = ('-modified', '-created')


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'product', 'created', 'modified')
    # list_filter = ()
    # search_fields = ()
    ordering = ('-modified', '-created')


@admin.register(UserFavorites)
class UserFavoritesAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_favorites', 'created', 'modified')
    # list_filter = ()
    # search_fields = ()
    ordering = ('-modified', '-created')

    def get_favorites(self, obj):
        """
        Retorna a quantidade de favoritos para este user
        """
        return len(obj.products.all())