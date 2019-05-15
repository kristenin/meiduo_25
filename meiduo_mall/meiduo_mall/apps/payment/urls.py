from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^payment/(?P<order_id>\d+)/$', views.PaymentView.as_view()),

    url(r'^payment/status/$', views.PaymentStatusView.as_view()),
]

