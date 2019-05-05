from django.db import models

# Create your models here.


class ForumBlock(models.Model):
    """block
    表名: forum_block
    """
    block_ID = models.AutoField(primary_key=True)
    block_name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.block_name

    class Meta:
        db_table = 'forum_block'
        verbose_name = '论坛版块'
        verbose_name_plural = '论坛板块'


class Articles(models.Model):
    articles_id = models.AutoField(primary_key=True)
    article_title = models.CharField(max_length=100, null=True)
    content = models.TextField(null=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    block_id = models.ForeignKey(ForumBlock, on_delete=models.CASCADE, related_name='forum_article')
    author = models.CharField(max_length=128, null=True, default='匿名用户')
    praise_points = models.PositiveIntegerField(default='0')

    class Meta:
        db_table = 'articles'
        ordering = ['creation_time']
        verbose_name = '文章汇总'
        verbose_name_plural = '文章汇总'


# class Replies