from django.core.files.storage import Storage

class FastDFSStorage(Storage):
    """自定义文件存储类"""

    def _open(self,name,mode='rb'):
        """
        用于打开文件
        :param name: 要打开的文件名
        :param mode: 打开文件模式
        """
        pass

    def _save(self,name,content):
        """
        文件上传时会调用此方法
        :param name: 要上传的文件名
        :param content: 要上传的文件对象
        :return: file_id
        """
        pass

    def url(self, name):
        """
        当使用image字段,url属性就会来调用此方法获取到要访问的图片绝对路径
        :param name: file_id
        :return: http://192.168.190.150:8888/ + file_id
        """
        return 'http://192.168.190.150:8888/' + name