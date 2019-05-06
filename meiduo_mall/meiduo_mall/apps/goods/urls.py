from django.conf.urls import url

from . import views

urlpatterns = [
    # 商品列表界面
    url(r'^list/(?P<category_id>\d+)/(?P<page_num>\d+)/$', views.ListView.as_view()),

    # 热销排行
    url(r'^hot/(?P<category_id>\d+)/', views.HotGoodsView.as_view()),
]