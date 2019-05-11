from django.shortcuts import render
from meiduo_mall.utils.views import LoginRequiredView



class OrderSettlementView(LoginRequiredView):
    """结算订单"""
    def get(self,request):
        return render(request,'place_order.html')

