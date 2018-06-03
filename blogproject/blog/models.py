# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import markdown
from django.utils.html import strip_tags
from django.views.generic import ListView
from django.utils.six import python_2_unicode_compatible

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    title=models.CharField(max_length=100)
    text=models.TextField()
    created_time=models.DateTimeField()
    modified_time=models.DateTimeField()
    exerpt=models.CharField(max_length=200,blank=True)
   # name=models.CharField(max_length=100)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,)
    tag=models.ManyToManyField(Tag,blank=True)
    author=models.ForeignKey(User,on_delete=models.CASCADE,)

    views=models.PositiveIntegerField(default=0)

    class Meta:
        ordering=['-created_time','title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail',kwargs={'pk':self.pk})
#第一个参数的值是 'blog:detail'，意思是 blog 应用下的 name=detail 的函数，
# 由于我们在上面通过 app_name = 'blog' 告诉了 Django 这个 URL 模块是属于 blog 应用的，
# 因此 Django 能够顺利地找到 blog 应用下 name 为 detail 的视图函数，
# 于是 reverse 函数会去解析这个视图函数对应的 URL，我们这里 detail 对应的规则就是 post/(?P<pk>[0-9]+)/ 这个正则表达式，
# 而正则表达式部分会被后面传入的参数 pk 替换，所以，如果 Post 的 id（或者 pk，这里 pk 和 id 是等价的） 是 255 的话，
# 那么 get_absolute_url 函数返回的就是 /post/255/ ，这样 Post 自己就生成了自己的 URL。

    def increase_views(self):
        self.views=self.views+1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        if (not self.exerpt) or (self.text):
            md=markdown.Markdown(extensions=['markdown.extensions.extra',
                'markdown.extensions.codehilite'])

            self.exerpt=strip_tags(md.convert(self.text))[:54]
        super(Post,self).save(*args, **kwargs)


