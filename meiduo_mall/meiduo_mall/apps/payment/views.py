from django.shortcuts import render
from django import http
from django.conf import settings
from django.views import View

import os
from alipay import AliPay
from orders.models import OrderInfo
from meiduo_mall.utils.views import LoginRequiredView
from meiduo_mall.utils.response_code import RETCODE
from .models import Payment

class PaymentView(LoginRequiredView):
    def get(self,request, order_id):
        try:
            order = OrderInfo.objects.get(order_id = order_id, user = request.user, status=OrderInfo.ORDER_STATUS_ENUM['UNPAID'])
        except OrderInfo.DoesNotExist:
            return http.HttpResponseForbidden('订单有误')

        alipay = AliPay(
            appid = settings.ALIPAY_APPID,
            app_notify_url = None,
            app_private_key_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'keys/app_private_key.pem'),
            alipay_public_key_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'keys/alipay_public_key.pem'),
            sign_type = "RSA2",
            debug = settings.ALIPAY_DEBUG
        )

        order_string = alipay.api_alipay_trade_page_pay(
            subject='美多商城%s' % order_id,
            out_trade_no=order_id,
            total_amount=str(order.total_amount),
            return_url=settings.ALIPAY_RETURN_URL
        )

        alipay_url = settings.ALIPAY_RETURN_URL + "?" + order_string

        return http.JsonResponse({'code':RETCODE.OK, 'errmsg':'OK', 'alipay_url':alipay_url})

class PaymentStatusView(View):
    def get(self, request):
        query_dict = request.GET
        data = query_dict.dict()
        sign = data.pop('sign')

        alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,
            app_private_key_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'keys/app_private_key.pem'),
            alipay_public_key_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),'keys/alipay_public_key.pem'),
            sign_type="RSA2",
            debug=settings.ALIPAY_DEBUG
        )

        success = alipay.verify(data, sign)
        if success:
            order_id = data.get('out_trade_no')
            trade_id = data.get('trade_no')
            try:
                Payment.objects.get(order_id=order_id, trade_id=trade_id)
            except Payment.DoesNotExist:
                Payment.objects.create(
                    order_id = order_id,
                    trade_id = trade_id
                )

                OrderInfo.objects.filter(user=request.user, order_id = order_id, status=OrderInfo.ORDER_STATUS_ENUM['UNPAID']).update(
                    status = OrderInfo.ORDER_STATUS_ENUM['UNCOMMENT']
                )
            return render(request, 'pay_success.html', {'trade_id':trade_id})
        else:
            return http.HttpResponseForbidden('非法请求')
