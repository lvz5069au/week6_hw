from django.conf.urls import url

from web.views import index

urlpatterns = [
    # 前台首页
    url(r'^$', index.index, name="index"),
]
