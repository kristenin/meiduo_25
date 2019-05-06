from django.shortcuts import render
from django.views import View
from goods.models import GoodsChannel, GoodsCategory
from .utils import get_categories

# Create your views here.

class IndexView(View):
    """首页"""
    def get(self, request):
        """
        商品分类及广告数据展示
        """

        context = {
            'categories':get_categories()
        }
        return render(request, 'index.html',context)