from fdfs_client.client import Fdfs_client

# 创建fast客户，加载客户端配置文件
client = Fdfs_client('./client.conf')

# 上传
ret = client.upload_by_filename('/home/python/Desktop/01.jpeg')
print(ret)
