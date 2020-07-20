from django.db.models import Q
from django.shortcuts import render


# Create your views here.
from django.views.generic import ListView

from mall.models import Product
from utils import constants


def product_list(request, template_name='product_list.html'):
    prod_list = Product.objects.filter(
        status=constants.PRODUCT_STATUS_SELL,
        is_valid=True
    )

    name = request.GET.get('name', '')
    if name:
        prod_list = prod_list.filter(name__icontains=name)

    return render(request, template_name, {
        'prod_list': prod_list
    })


def product_detail(request, pk, template_name='product_detail.html'):
    return render(request, template_name)

class ProductList(ListView):
    paginate_by = 5
    template_name = 'product_list.html'

    def get_queryset(self):
        query = Q(status=constants.PRODUCT_STATUS_SELL, is_valid=True)
        name = self.request.GET.get('name', '')
        if name:
            query = query & Q(name__icontains=name)
        return Product.objects.filter
