from django.urls import path, re_path, include
from . import views


app_name = 'forums'

urlpatterns = [
    # 查阅论坛
    path('consult/', views.ConsultView.as_view(), name='consult')
    # re_path(r'consult/(?P<block_name>\d+)/(?P<article_id>\d+)/(?P<page_no>\d+)/', views.consult, name='consult'),
    # 发布文章
    # path('publish/')
]
