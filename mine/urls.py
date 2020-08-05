from django.contrib.auth.decorators import login_required
from django.urls import path, re_path

from mine import views

urlpatterns = [
    path('', views.index, name='index'),
    # 订单详情
    re_path(r'^order/detail/(?P<sn>\S+)/$', login_required(views.OrderDetailView.as_view()), name='order_detail'),
    # 添加到购物车
    re_path(r'^cart/add/(?P<prod_uid>\S+)/$', views.cart_add, name='cart_add'),
    # 我的购物车
    path('cart/', views.cart, name='cart'),
    # 提交订单
    path('order/pay/', views.order_pay, name='order_pay'),
    # 我的订单列表
    # path('order/list/', views.order_list, name='order_list'),
    path('order/list/', login_required(views.OrderListView.as_view()), name='order_list'),
    # 我的收藏
    path('prod/collect/', views.prod_collect, name='prod_collect')
]
