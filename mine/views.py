from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db import transaction
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView

from mall.models import Product
from mine.models import Order, Cart
from utils import constants


class OrderDetailView(DetailView):
    model = Order
    slug_field = 'sn'
    slug_url_kwarg = 'sn'
    template_name = 'order_info.html'


@login_required
@transaction.atomic()
def cart_add(request, prod_uid):
    user = request.user
    product = get_object_or_404(Product,
                                uid=prod_uid,
                                is_valid=True,
                                status=constants.PRODUCT_STATUS_SELL)
    # 购买数量
    count = int(request.POST.get('count', 1))
    # 检查库存
    if product.remain_count < count:
        return HttpResponse('no')
    # 减库存
    product.update_store_count(count)
    # 生成购物查记录， 如果已经添加到购物车了，就把购买数量和价格更新一下
    try:
        cart = Cart.objects.get(product=product, user=user, status=constants.ORDER_STATUS_INIT)
        # 更新价格和数量
        count = cart.count + count
        cart.count = count
        cart.amount = count * cart.price
        cart.save()
    except Cart.DoesNotExist:
        Cart.objects.create(
            product=product,
            user=user,
            name=product.name,
            img=product.img,
            price=product.price,
            origin_price=product.origin_price,
            count=count,
            amount=count * product.price
        )
    return HttpResponse('ok')


@login_required
def cart(request):
    """我的购物车"""
    prod_list = request.user.carts.filter(status=constants.ORDER_STATUS_INIT)
    return render(request, 'cart.html', {
        'prod_list': prod_list
    })


