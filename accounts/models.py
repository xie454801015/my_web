from django.db import models

# Create your models here.


class User(models.Model):
    """user list
    表名:user_data
    user_name 用户名 唯一 主键
    password 密码
    email 电子邮箱
    sex 性别
    creation_time 创建时间
    """
    gender = (
        ('male', '男'),
        ('female', '女')
    )
    user_name = models.CharField(max_length=128, unique=True, primary_key=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default='男')
    creation_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_name
    # 返回实例的用户名

    class Meta:
        db_table = 'user_data'
        ordering = ['creation_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'
