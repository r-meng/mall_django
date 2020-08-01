from django.contrib.auth.decorators import login_required
from django.urls import path, re_path

from mine import views

urlpatterns = [
    # 订单详情
    re_path(r'^order/detail/(?P<sn>\S+)/$', login_required(views.OrderDetailView.as_view()), name='order_detail'),
    re_path(r'^cart/add/(?P<prod_uid>\S+)/$', views.cart_add, name='cart_add'),
    path('cart/', views.cart, name='cart')
]
