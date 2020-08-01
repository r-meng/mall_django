import xadmin

from mall.models import Product


class ProductAdmin(object):
    list_display = ('name', 'types', 'price')
    list_filter = ('types', 'status')
    search_fields = ('name',)

xadmin.site.register(Product, ProductAdmin)

