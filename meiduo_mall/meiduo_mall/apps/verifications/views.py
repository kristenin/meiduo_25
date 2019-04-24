from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection
from meiduo_mall.libs.captcha.captcha import captcha
from django import http
# Create your views here.

class ImageCodeView(View):
    """生成图形验证码"""
    def get(self, request, uuid):
        """
        :param uuid: 唯一标识,用来区分当前的图形验证码属于哪个用户
        :return:
        """
        # 利用SDK 生成图形验证码
        # name为唯一标识字符串, text为图形验证内容字符串, image为二进制图片数据
        name, text, image = captcha.generate_captcha()

        # 创建redis连接对象
        redis_conn = get_redis_connection('verify_code')

        # 将图形验证码字符串存入到redis
        redis_conn.setex('img_%s' % uuid, 300, text)

        # 把生成好的图片响应给前端
        return http.HttpResponse(image, content_type='image/png')


class SMSCodeView(View):
    """短信验证码"""

    def get(self, request, mobile):
        """

        :param mobile: 要接收短信验证码的手机号
        """
        pass