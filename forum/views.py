from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
from . import models
from django.core import serializers
import json
import math
from datetime import datetime


class ConsultView(View):
    template_name = 'articles.html'
    form_class = [models.ForumBlock, models.Articles]
    articles = None
    sig_page_num = 10
    block_name = '所有文章'
    block_id = None
    article_id = None
    page_no = 1
    art_num = 0

    def get(self, request):
        # 可添加预先返回的数据，如图片地址等
        return render(request, self.template_name)

    def post(self, request):
        self.init_data_attributes(request)
        self.page_no = int(request.POST.get('page_no', self.page_no))
        # 检索数据库的条数
        pages_num = math.ceil(self.art_num/self.sig_page_num)
        if pages_num < self.page_no:
            self.page_no = 1
        # 计算所取区间
        start = (self.page_no-1) * self.sig_page_num
        end = self.page_no * self.sig_page_num
        # 根据分页，获取部分版块内文章
        articles = list(self.articles.values('articles_id', 'article_title', 'creation_time', 'author', 'praise_points')[start:end])
        # 组合传输的
        views_data = {'articles': json.dumps(articles,cls=DateEncoder),
                      'block_name': self.block_name,
                      'pages_num': pages_num,
                      'page_no': self.page_no,
                      }
        return JsonResponse(views_data)

    def init_data_attributes(self, request):
        # 初始化views数据方法，用于post获取
        # get获取对应url数据
        self.block_id = request.GET.get("block_id", None)
        self.article_id = request.GET.get("article_id", None)
        if self.block_id:
            block = self.form_class[0].objects.get(block_ID=self.block_id)
            self.block_name = block.block_name
            if self.article_id:
                # 介入文章内容以及评论self.
                pass
            else:
                self.articles = self.form_class[1].objects.filter(block_id=self.block_id)
                self.art_num = self.articles.count()
        else:
            # 未输入ID时 获取所有文章
            self.block_name = '所有文章'
            self.articles = self.form_class[1].objects.all()
            self.art_num = self.articles.count()


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)


