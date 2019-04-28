from itsdangerous import TimedJSONWebSignatureSerializer as Serializer,BadData
from django.conf import settings

def generate_eccess_token(openid):
    """
    对openid进行签名
    :param openid: 用户的openid
    :return: access_token
    """
    # SECRET_KEY  是系统配置文件下随机生成的密钥
    # expires_in 是过期时间
    serializer = Serializer(settings.SECRET_KEY, expires_in=600)
    data = {'openid':openid} # 把数据包装成字典
    token = serializer.dump(data) # 加密后返回的数据是bytes类型
    return token.decode()


def check_openid_sign(openid_sign):
    """
    对加密后的openid进行解密，回到原本样子
    :param openid_sign: 要解密的openid
    :return: 原本的openid
    """
    # serializer = Serializer(密钥， 有效期秒)
    serializer = Serializer(settings.SECRET_KEY, expires_in=600)

    # 检验token
    # 验证失败，会抛出itsdangerous.BadData异常
    try:
        data = serializer.loads(openid_sign)
    except BadData:
        return None
    else:
        return data.get('openid')