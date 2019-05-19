from django.conf.urls import url
from . import views

urlpatterns = [
    # 获取QQ登录界面url
    url(r'^qq/authorization/$', views.OAuthURLView.as_view()),
    # QQ登录成功后的回调处理
    url(r'^oauth_callback/$', views.OAuthUserView.as_view()),
    # 获取weibo登录界面url
    url(r'^weibo/authorization/$', views.OAuthWeiboURLView.as_view()),

    url(r'^sina_callback/$', views.OAuthWeiboUserView.as_view()),

]