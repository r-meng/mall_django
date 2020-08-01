from django.contrib import admin

# Register your models here.
from mine.models import Order, Cart, Comments


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """订单后台管理"""
    list_display = ('sn', 'user', 'to_user', 'to_area', 'to_phone')
    search_fields = ('user__username', 'user__nickname', 'to_user')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'price', 'img')


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'score', 'desc')
