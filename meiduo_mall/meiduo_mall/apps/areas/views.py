from django.shortcuts import render
from django.views import  View
from django import http
from django.core.cache import cache
from .models import Area
from meiduo_mall.utils.response_code import RETCODE
# Create your views here.

class AreasView(View):
    """省市区数据查询"""
    def get(self, request):
        """实现省市区查询逻辑"""
        area_id = request.GET.get('area_id')

        # 如果area_id没有值,代表要查询所有省数据
        if area_id is None:

            # 先尝试性的去redis获取所有省的数据
            provinces_list = cache.get('provinces_list')
            if provinces_list is None:
                # 获取所有省的数据
                provinces_model_qs = Area.objects.filter(parent=None)
                provinces_list = [] # 把一个一个省的字典添加到此列表
                # 遍历所有省的查询集
                for province in provinces_model_qs:
                    province_dict = {
                        'id': province.id,
                        'name': province.name
                    }
                    provinces_list.append(province_dict)

                # 如果没有缓存，此时应该把所有省数据缓存起来
                cache.set('province_list', provinces_list, 3600)

            return http.JsonResponse({'code':RETCODE.OK, 'errmsg':'OK', 'province_list':provinces_list})
        else:
            # 如果area_id 有值代表要查询指定省及下级行政区，查询指定市及下级行政区
            area_datas = cache.get('area_data_%s' % area_id)
            if area_datas is None:
                try:
                    area_model = Area.objects.get(id=area_id)
                    # 此模型有可能是某个省，也有可能是某个市
                except Area.DoesNotExist:
                    return http.HttpResponseForbidden('area_id不存在')

                subs_model_qs = area_model.subs.all()   # 获取下级所有行政区

                sub_list = []   # 用来装下级行政区的字典
                for sub in subs_model_qs:
                    sub_dict = {
                        'id':sub.id,
                        'name':sub.name
                    }
                    sub_list.append(sub_dict)

                area_datas = {
                    'id': area_model.id,
                    'name':area_model.name,
                    'subs':sub_list
                }
                cache.set('area_datas_%s' % area_id, area_datas,3600)
            return http.JsonResponse({'code':RETCODE.OK, 'errmsg':'OK', 'sub_data':area_datas})