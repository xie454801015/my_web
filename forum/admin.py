from django.contrib import admin
from .models import *
# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('article_title', 'creation_time', 'block_id')


admin.site.register(ForumBlock)
admin.site.register(Articles, ArticleAdmin)
