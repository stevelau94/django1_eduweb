# -*-coding:utf-8-*-
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name=u'昵称', default='')
    birday = models.DateField(verbose_name=u'生日', null=True, blank=True)
    gender = models.CharField(max_length=8, choices=(('male', u'男'), ('female', '女')), default='female')
    address = models.CharField(max_length=100, default='')
    mobile = models.CharField(max_length=11, null=True, blank=True)
    # 头像 定义好上传路径
    image = models.ImageField(upload_to='image/%Y/%m', default=u'image/default.png', max_length=100)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name=u'验证码')
    email = models.EmailField(max_length=50, verbose_name=u'邮箱')
    send_type = models.CharField(verbose_name='验证码类型', choices=(('register', u'注册'), ('forget', u'找回密码')),
                                 max_length=10)
    send_time = models.DateTimeField(verbose_name='发送时间', default=datetime.now)

    class Meta:
        verbose_name = u'邮箱验证码'
        verbose_name_plural = verbose_name

    # 重载unicode，更在其在页面的显示方法
    def __unicode__(self):
        return '{0}({1})'.format(self.code, self.email)


class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name=u'标题')
    image = models.ImageField(upload_to='banner/%Y/%m', verbose_name=u'轮播图')
    url = models.URLField(max_length=200, verbose_name=u'访问地址')
    index = models.IntegerField(default=100, verbose_name=u'顺序')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'轮播图'
        verbose_name_plural = verbose_name
