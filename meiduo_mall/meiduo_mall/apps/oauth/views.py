from django.shortcuts import render
from django.views import View
from django import http
from QQLoginTool.QQtool import OAuthQQ
from django.conf import settings
from meiduo_mall.utils.response_code import RETCODE
import logging
# Create your views here.

class QQAuthURLView(View):
    """提供QQ登录页面网址
    https://graph.qq.com/oauth2.0/authorize?response_type=code&client_id=xxx&redirect_uri=xxx&state=xxx
    """
    def get(self, request):
        # next表示从哪个页面进入到的登录页面，将来登录成功后，就自动回到那个页面
        next = request.GET.get('next', '/')

        # 获取QQ登录页面网址
        # oauth = OAuthQQ(client_id='appid', client_secret='appkey', redirect_url='授权成功回调url', state='记录来源')
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                        client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI,
                        state=next)
        # 拼接QQ登录链接
        login_url = oauth.get_qq_url()

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'login_url':login_url})

class QQAuthUserView(View):
    """用户扫玛登录的回调处理"""

    def get(self, request):
        """Oauth2.0认证"""
        # 接收Authorization Code
        code = request.GET.get('code')
        if not code:
            return http.HttpResponseForbidden('缺少code')

        # 创建工具对象
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                        client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI)

        try:
            # 使用code向QQ服务器请求access_token
            access_token = oauth.get_access_token(code)

            # 使用access_token向QQ服务器请求openid
            openid = oauth.get_open_id(access_token)
        except Exception as e:
            logger = logging.getLogger('django')
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.SERVERERR, 'errmsg':'QQ服务器不可用'})


        return http.HttpResponseServerError({'openid':openid})
