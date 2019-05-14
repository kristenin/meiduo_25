from django.conf.urls import url
from . import views

urlpatterns = [
    # 购物车增删改查
    url(r'^carts/$', views.CartsView.as_view()),

    # 全选购物车
    url(r'^carts/selection/$', views.CartsSelectAllView.as_view()),

    # 简单购物车
    url(r'^carts/simple/$', views.CartsSimpleView.as_view()),

    # url(r'^time/$', views.GetCartsTime.as_view()),
]