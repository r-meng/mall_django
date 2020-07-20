from django.urls import path, re_path

from accounts import views

urlpatterns = [
    path('user/login/', views.user_login, name='user_login'),
    path('user/logout/', views.user_logout, name='user_logout'),
    path('user/register/', views.user_register, name='user_register'),
    path('user/address/list/', views.address_list, name='address_list'),
    # 新增和修改
    # user/address/edit/add      user/address/edit/12
    re_path(r'^user/address/edit/(?P<pk>\S+)/$', views.address_edit, name='address_edit'),
    path(r'^user/address/delete/<int:pk>/', views.address_delete, name='address_delete'),


]