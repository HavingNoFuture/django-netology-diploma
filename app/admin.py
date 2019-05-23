from django.contrib import admin

from .models import Product, Review, Article, Order, Category, CartItem, Cart

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    pass


def make_order_payed(modelAdmin, request, queryset):
    queryset.update(status='Оплачен')
make_order_payed.short_description = 'Пометить как оплаченные'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'status')
    list_filter = ['create_date']
    actions = [make_order_payed]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    pass

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    pass