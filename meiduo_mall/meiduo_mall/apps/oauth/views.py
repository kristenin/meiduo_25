from django.shortcuts import render, redirect
from django.views import View
from django import http
from QQLoginTool.QQtool import OAuthQQ
from django.conf import settings
from django.contrib.auth import login

from meiduo_mall.utils.response_code import RETCODE
import logging
from .models import OAuthQQUser
import re

from django_redis import get_redis_connection
from .utils import generate_openid_signature,check_openid_sign
from users.models import User
from carts.utils import merge_cart_cookie_to_redis


logger = logging.getLogger('django')


# Create your views here.
class OAuthURLView(View):
    """提供QQ登录界面链接"""

    def get(self, request):
        # 提取前端用查询参数传入的next参数:记录用户从哪里去到login界面
        next = request.GET.get('next', '/')
        # QQ_CLIENT_ID = '101518219'
        # QQ_CLIENT_SECRET = '418d84ebdc7241efb79536886ae95224'
        # QQ_REDIRECT_URI = 'http://www.meiduo.site:8000/oauth_callback'
        # oauth = OAuthQQ(client_id='appid', client_secret='appkey', redirect_uri='授权成功回调url', state='记录来源')
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                        client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI,
                        state=next)
        # 拼接QQ登录连接
        # https://graph.qq.com/oauth2.0/authorize?response_type=code&client_id=123&redirect_uri=xxx&state=next
        login_url = oauth.get_qq_url()

        return http.JsonResponse({'login_url': login_url, 'code': RETCODE.OK, 'errmsg': 'OK'})


class OAuthUserView(View):
    """QQ登录后回调处理"""

    def get(self, request):

        # 获取查询字符串中的code
        code = request.GET.get('code')
        state = request.GET.get('state', '/')


        # 创建QQ登录SDK对象
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                        client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI,
                        )

        try:
            # 调用SDK中的get_access_token(code) 得到access_token
            access_token = oauth.get_access_token(code)
            # 调用SDK中的get_openid(access_token) 得到openid
            openid = oauth.get_open_id(access_token)
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.SERVERERR, 'errmsg': 'QQ服务器不可用'})

        # 在OAuthQQUser表中查询openid
        try:
            oauth_model = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist:
            # 如果在OAuthQQUser表中没有查询到openid, 没绑定说明第一个QQ登录

            # 先对openid进行加密
            openid = generate_openid_signature(openid)
            # 创建一个新的美多用户和QQ的openid绑定
            return render(request, 'oauth_callback.html', {'openid':openid})
        else:
            # 如果在OAuthQQUser表中查询到openid,说明是已绑定过美多用户的QQ号
            user = oauth_model.user
            login(request, user)
            # 直接登录成功:  状态操持,
            response = redirect(state)
            response.set_cookie('username', user.username, max_age=settings.SESSSION_COOKIE_AGE)

            # 登录成功那一刻合并购物车
            merge_cart_cookie_to_redis(request, user, response)

            return response
        # return http.JsonResponse({'openid': openid})

    def post(self, request):
        """美多商城用户绑定到openid"""
        # 接收参数
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        sms_code = request.POST.get('sms_code')
        openid = request.POST.get('openid')

        # 校验参数
        # 判断参数是否齐全
        if all([mobile, password,sms_code,openid]) is False:
            return http.HttpResponseForbidden('缺少必传参数')
        # 判断手机号是否合法
        if  not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('请输入正确的手机号码')
        # 判断密码是否合适
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return http.HttpResponseForbidden('请输入8-20位的密码')

        # 判断短信验证码是否一致
        redis_conn = get_redis_connection('verify_code')
        sms_code_server = redis_conn.get('sms_%s' % mobile)
        if sms_code_server is None:
            return render(request, 'oauth_callback.html', {'sms_code_errmsg':'无效的短信验证码'})
        if sms_code != sms_code_server.decode():
            return render(request,'oauth_callback.html',{'sms_code_errmsg':'输入短信验证码有误'})
        # 判断openid是否有效：错误提示放在sms_code_errmsg位置
        openid = check_openid_sign(openid)
        if not openid:
            return render(request,'oauth_callback.html',{'openid_errmsg':'无效的openid'})

        # 保存注册数据
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            # 用户不存在，新建用户
            user = User.objects.create_user(
                username=mobile,
                password=password,
                mobile=mobile,
            )
        else:
            # 如果用户存在，检查用户密码
            if  user.check_password(password) is False:
                return render(request,'oauth_callback.html',{'account_errmsg':'用户名或密码错误'})

        # 将用户绑定openid
        OAuthQQUser.objects.create(
            openid=openid,
            user=user
        )

        # 实现状态保持
        login(request, user)

        # 响应绑定结果
        next = request.GET.get('state')
        response = redirect(next)

        # 登录时用户名写入到cookie，有效期15天
        response.set_cookie('username', user.username, max_age=3600*24*15)

        return response