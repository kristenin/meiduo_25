from django.contrib.auth.backends import ModelBackend
import re
from .models import User
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.conf import settings

def get_user_by_account(account):
    """
    根据account查询用户
    :param account: 用户名或者手机号
    :return: user,None
    """
    try:
        if re.match('^1[3-9]\d{9}$', account):
            # 手机号登陆
            user = User.objects.get(mobile=account)
        else:
            # 用户名登陆
            user = User.objects.get(username=account)
    except User.DoesNotExist:
        return None
    else:
        return user # 要返回的是查询出来的user对象，不要写成类了


class UsernameMobileAuthBackend(ModelBackend):
    """自定义用户认证后端"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        重写认证方法，实现多账号登陆
        :param request: 请求对象
        :param username: 用户名
        :param password: 密码
        :param kwargs: 其他参数
        :return: user
        """
        # 根据传入的username获取user对象，username可以是手机号也可以是账号
        user = get_user_by_account(username)
        # 校验user是否存在并校验密码是否正确
        if user and user.check_password(password):
            return user


def generate_verify_email_url(user):
    """对当前传入的user生成激活邮箱url"""
    serializer = Serializer(secret_key=settings.SECRET_KEY, expires_in=3600*24)
    data = {'user_id':user.id, 'email':user.email}
    data_sign = serializer.dumps(data).decode()

    # verify_url = 'http://www.meiduo.site:8000/emails/verification/?token=2'
    verify_url = settings.EMAIL_VERIFY_URL + '?token' + data_sign
    return verify_url