from celery import Celery
import os

# 告诉celery它里面用的Django配置文件在哪里
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meiduo_mall.settings.dev")

# 1. 创建celery实力对象（生产者）
celery_app = Celery('meiduo')

# 2.加载配置，指定谁来作为经纪人（任务存在哪里）
celery_app.config_from_object('celery_tasks.config')

# 3.自动注册执行
celery_app.autodiscover_tasks(['celery_tasks.sms','celery_tasks.email'])