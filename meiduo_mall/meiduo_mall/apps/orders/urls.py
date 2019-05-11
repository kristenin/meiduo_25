from django.conf.urls import url
from . import views

urlpatterns = [
    # 结算订单
    url(r'^orders/settlement/$', views.OrderSettlementView.as_view()),

    # 订单提交
    url(r'^orders/commit/$', views.OrderCommitView.as_view()),
]
