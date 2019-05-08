from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    # 注册
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    # 判断用户名是否已注册
    url(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/', views.UsernameCountView.as_view(), name='usernames'),
    # 判断手机号是否已注册
    url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/', views.MobileCountView.as_view(), name='mobiles'),

    # 用户登陆
    url(r'^login/',views.LoginView.as_view(), name='login'),
    # 退出登陆
    url(r'^logout/',views.LogoutView.as_view(), name='logout'),

    # 用户中心
    url(r'^info/$', login_required(views.UserInfoView.as_view()), name='info'),

    # 设置用户邮箱
    url(r'^emails/$', views.EmailView.as_view()),

    # 激活邮箱
    url(r'^emails/verification/$', views.VerifyEmailView.as_view()),

    # 用户收获地址
    url(r'^addresses/$', views.AddressView.as_view()),
    # 用户新增收获地址
    url(r'^addresses/create/$', views.CreateAddressView.as_view()),

    # 用户收货地址修改和删除
    url(r'^addresses/(?P<address_id>\d+)/$', views.UpdateDestroyAddressView.as_view()),
    # 用户设置默认地址
    url(r'^addresses/(?P<address_id>\d+)/default/$', views.DefaultAddressView.as_view()),
    # 修改用户地址标题
    url(r'^addresses/(?P<address_id>\d+)/title/$', views.UpdateTitleAddressView.as_view()),
    # 修改用户密码
    url(r'^password/$', views.ChangePasswordView.as_view()),

    # 保存用户浏览记录
    url(r'^browse_histories/', views.UserBrowseHistory.as_view()),
]
