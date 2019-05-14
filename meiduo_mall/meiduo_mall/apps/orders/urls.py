from django.conf.urls import url
from . import views

urlpatterns = [
    # 结算订单
    url(r'^orders/settlement/$', views.OrderSettlementView.as_view()),

    # 订单提交
    url(r'^orders/commit/$', views.OrderCommitView.as_view()),

    # 订单提交成功页面
    url(r'^orders/success/$', views.OrderSuccessView.as_view()),

    url(r'^orders/comment/$', views.OrderCommentView.as_view()),

    url(r'^comments/(?P<sku_id>\d+)/$', views.GoodsCommentView.as_view()),
]
