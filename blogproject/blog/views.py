# -*- coding: utf-8 -*-
import markdown

from comments.forms import CommentForm

from django.shortcuts import render,get_object_or_404

from django.http import HttpResponse

from .models import Post,Category

# Create your views here.

def index(request):
    post_list=Post.objects.all()
    return render(request,'blog/index.html',context={'post_list':post_list

    })


def detail(request,pk):
    post=get_object_or_404(Post,pk=pk)

    post.increase_views()
    post.text=markdown.markdown(post.text,extensions=['markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.toc'])

    form=CommentForm()
    comment_list=post.comment_set.all()

    context={'post': post,
               'form': form,
               'comment_list': comment_list
               }
    return render(request,'blog/detail.html',context=context)


#首先接受了一个名为 request 的参数，
# 这个 request 就是 Django 为我们封装好的 HTTP 请求，它是类 HttpRequest 的一个实例。然后我们便直接返回了一个 HTTP 响应给用户，这个 HTTP 响应也是 Django 帮我们封装好的，它是类 HttpResponse 的一个实例，
# 只是我们给它传了一个自定义的字符串参数。



def archives(request,year,month,day):
    post_list=Post.objects.filter(created_time__year=year,created_time__month=month,created_time__day=day).order_by('-created_time')
    return render(request,'blog/index.html',context={'post_list':post_list})


def category(request,pk):
    cate=get_object_or_404(Category,pk=pk)
    post_list=Post.objects.filter(category=cate).order_by('-created_time')
    return render(request,'blog/index.html',context={'post_list':post_list})