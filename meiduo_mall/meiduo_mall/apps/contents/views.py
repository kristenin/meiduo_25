from django.shortcuts import render
from django.views import View
from goods.models import GoodsChannel, GoodsCategory
from .utils import get_categories
from .models import ContentCategory,Content

# Create your views here.

class IndexView(View):
    """首页"""
    def get(self, request):
        """
        商品分类及广告数据展示
        """
        contents = {}   # 用来装所有广告数据的字典
        """
        {
            'index_lbt':lbt_qs,
            'index_kx':kx_qs
        }
        """
        contentCategory_qs = ContentCategory.objects.all()  # 获取所有广告类别数据
        for category in contentCategory_qs:
            contents[category.key] = category.content_set.filter(status=True).order_by('sequence')

        context = {
            'categories':get_categories(),
            'contents':contents
        }
        return render(request, 'index.html',context)