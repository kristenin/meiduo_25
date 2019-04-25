from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection
from meiduo_mall.libs.captcha.captcha import captcha
from django import http
from random import randint


from meiduo_mall.libs.captcha.captcha import captcha
from meiduo_mall.utils.response_code import RETCODE
import logging
from meiduo_mall.libs.yuntongxun.sms import CCP
logger = logging.getLogger('django')
# Create your views here.

class ImageCodeView(View):
    """生成图形验证码"""
    print("456")
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

        :param request: 请求对象
        :param mobile: 手机号
        :return: JSON
        """
        # 接收参数,接收到前端传入的mobile,image_code,uuid
        image_code_client = request.GET.get("image_code")
        uuid = request.GET.get("uuid")

        # 校验参数,判断参数是否齐全
        if not all([image_code_client, uuid]):
            return http.JsonResponse({"code":RETCODE.NECESSARYPARAMERR, "errmasg":"缺少必要参数"})

        # 创建连接到redis的对象
        redis_conn = get_redis_connection("verify_code")
        # 提取图形验证码,根据uuid作为key 获取到redis中当前用户的图形验证值
        image_code_server = redis_conn.get('img_%s' % uuid)
        # 从redis中取出来的数据都是bytes类型

        # 判断用户写的图形验证码和我们redis存的是否一致
        if image_code_server is None or image_code_client.lower() != image_code_server.decode().lower():
            return http.JsonResponse({'code':RETCODE.NECESSARYPARAMERR,'errmsg':'图形验证码错误'})

        # 发送短信
        # 利用随机模块生成一个6位数字
        sms_code = "%06d" % randint(0, 999999)
        logger.info(sms_code)

        # 将生成好的短信验证码也存储到redis，以备后期校验
        redis_conn.setex('sms_%s' % mobile, 300, sms_code)
        # 利用容联云SDK发短信
        # CCP().send_template_sms(手机号,[验证码, 提示用户验证码有效期多少分钟],短信模板)
        CCP().send_template_sms(mobile,[sms_code, 5],1)

        # 响应
        return http.JsonResponse({"code":RETCODE.OK, 'errmsg':'发送短信验证'})