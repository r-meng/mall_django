from django.contrib import admin

# Register your models here.
from mall.forms import ProductAdminForm
from mall.models import Product, Classify, Tag
from utils.admin_actions import set_invalid, set_valid


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'types', 'price', 'status', 'is_valid')
    list_per_page = 5
    list_filter = ('status',)
    # 排除掉某些字段，使之不能编辑，在编辑界面不可见
    # exclude = ['remain_count']
    # 不可编辑，但是在界面可见
    readonly_fields = ['remain_count']
    actions = [set_invalid, set_valid]
    form = ProductAdminForm

# 方式二： 注册到后台管理
# admin.site.register(Product, ProductAdmin)


@admin.register(Classify)
class ClassifyAdmin(admin.ModelAdmin):
    list_display = ('parent', 'name', 'code', 'is_valid')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_valid')

