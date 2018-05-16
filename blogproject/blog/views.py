# -*- coding: utf-8 -*-
import markdown

from comments.forms import CommentForm

from django.shortcuts import render,get_object_or_404

from django.http import HttpResponse

from .models import Post,Category

from django.views.generic import ListView

from django.views.generic import DetailView

# Create your views here.

# def index(request):
#     post_list=Post.objects.all()
#     return render(request,'blog/index.html',context={'post_list':post_list
#
#     })


# def detail(request,pk):
#     post=get_object_or_404(Post,pk=pk)
#
#     post.increase_views()
#     post.text=markdown.markdown(post.text,extensions=['markdown.extensions.extra',
#                                      'markdown.extensions.codehilite',
#                                      'markdown.extensions.toc'])
#
#     form=CommentForm()
#     comment_list=post.comment_set.all()
#
#     context={'post': post,
#                'form': form,
#                'comment_list': comment_list
#                }
#     return render(request,'blog/detail.html',context=context)


#首先接受了一个名为 request 的参数，
# 这个 request 就是 Django 为我们封装好的 HTTP 请求，它是类 HttpRequest 的一个实例。然后我们便直接返回了一个 HTTP 响应给用户，这个 HTTP 响应也是 Django 帮我们封装好的，它是类 HttpResponse 的一个实例，
# 只是我们给它传了一个自定义的字符串参数。



# def archives(request,year,month,day):
#     post_list=Post.objects.filter(created_time__year=year,created_time__month=month,created_time__day=day).order_by('-created_time')
#     return render(request,'blog/index.html',context={'post_list':post_list})


# def category(request,pk):
#     cate=get_object_or_404(Category,pk=pk)
#     post_list=Post.objects.filter(category=cate).order_by('-created_time')
#     return render(request,'blog/index.html',context={'post_list':post_list})

class IndexView(ListView):
    model=Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'   #model。将 model 指定为 Post，告诉 Django 我要获取的模型是 Post。template_name。指定这个视图渲染的模板。context_object_name。指定获取的模型列表数据保存的变量名。这个变量会被传递给模板。


class CategoryView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = "post_list"

    def get_queryset(self):
        cate=get_object_or_404(Category,pk=self.kwargs.get("pk"))
        return super(CategoryView, self).get_queryset().filter(category=cate)

class ArchivesView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = "post_list"

    def get_queryset(self):
        year=self.kwargs.get("year")
        month=self.kwargs.get("month")
        day=self.kwargs.get("day")
        return super(ArchivesView, self).get_queryset().filter(created_time__year=year,
                                                                created_time__month=month,
                                                                created_time__day=day)

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        response=super(PostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response
    #可以简单地把 get 方法看成是 detail 视图函数，至于其它的像 get_object、get_context_data 都是辅助方法，这些方法最终在 get 方法中被调用，这里你没有看到被调用的原因是它们隐含在了 super(PostDetailView, self).get(request, *args, **kwargs) 即父类 get 方法的调用中。最终传递给浏览器的 HTTP 响应就是 get 方法返回的 HttpResponse 对象。

    def get_object(self, queryset=None):
        post=super(PostDetailView, self).get_object(queryset=None)
        post.text=markdown.markdown(post.text,extensions=['markdown.extensions.extra',
                                          'markdown.extensions.codehilite',
                                          'markdown.extensions.toc'])
        return post

    def get_context_data(self, **kwargs):
        context=super(PostDetailView,self).get_context_data(**kwargs)
        form=CommentForm()
        comment_list=self.object.comment_set.all()
        context.update({'form':form,'comment_list':comment_list})
        return context
