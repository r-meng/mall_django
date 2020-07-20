from django.urls import path, re_path

from mall import views

urlpatterns = [
    # 商品列表 def function实现
    # path('prod/list/', views.product_list, name='product_list'),
    # 使用class来实现
    path('prod/list/', views.ProductList.as_view(), name='product_list'),
    re_path(r'^prod/detail/(?P<pk>\S+)/$', views.product_detail, name='product_detail'),
]
