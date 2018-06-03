# -*- coding: utf-8 -*-
import markdown

from comments.forms import CommentForm

from django.shortcuts import render,get_object_or_404

from django.http import HttpResponse

from .models import Post,Category,Tag

from django.views.generic import ListView

from django.views.generic import DetailView

from django.utils.text import slugify

from markdown.extensions.toc import TocExtension

from django.db.models import Q

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

def search(request):
    q=request.GET.get('q')
    error_msg=''

    if not q:
        error_msg="请输入关键词"
        return render(request,'blog/index.html',{'error_msg': error_msg})

    post_list=Post.objects.filter(Q(title__icontains=q) | Q(text__icontains=q))
    return render(request,'blog/index.html',{'error_msg': error_msg,'post_list': post_list})


class IndexView(ListView):
    model=Post
    template_name = 'blog/index.html'
    paginate_by = 2
    context_object_name = 'post_list'   #model。将 model 指定为 Post，告诉 Django 我要获取的模型是 Post。template_name。指定这个视图渲染的模板。context_object_name。指定获取的模型列表数据保存的变量名。这个变量会被传递给模板。


    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data(**kwargs)
        paginator=context.get('paginator')
        page=context.get('page_obj')
        is_pageinated=context.get('is_paginated')

        pagination_data=self.pagination_data(paginator,page,is_pageinated)
        context.update(pagination_data)
        return context


    def pagination_data(self,paginator,page,is_paginated):
        if not is_paginated:
            return {}

        left=[]
        right=[]
        left_has_more=False
        right_has_more=False

        first=False
        last=False
        page_number=page.number
        total_pages=paginator.num_pages
        page_range=paginator.page_range

        if page_number==1:
            right=page_range[page_number:page_number+2]
            if right[-1]<total_pages-1:
                right_has_more=True

            if right[-1]<total_pages:
                last=True

        elif page_number==total_pages:
            left=page_range[(page_number-3) if (page_number-3>0) else 0:page_number-1]

            if left[0]>2:
                left_has_more=True

            if left[0]>1:
                first=True

        else:
            left=page_range[(page_number-3) if (page_number-3)>0 else 0:page_number-1]
            right=page_range[page_number:page_number+2]

            if right[-1]<total_pages-1:
                right_has_more=True

            if right[-1]<total_pages:
                last=True

            if left[0]>2:
                left_has_more=True
            if left[0]>1:
                first=True


        data={
            'left':left,
            'right':right,
            'left_has_more':left_has_more,
            'right_has_more':right_has_more,
            'first':first,
            'last':last
        }

        return data









class CategoryView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = "post_list"

    def get_queryset(self):
        cate=get_object_or_404(Category,pk=self.kwargs.get("pk"))
        return super(CategoryView, self).get_queryset().filter(category=cate)

class TagView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = "post_list"

    def get_queryset(self):
        tag=get_object_or_404(Tag,pk=self.kwargs.get("pk"))
        return super(TagView, self).get_queryset().filter(tag=tag)


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
        # post.text=markdown.markdown(post.text,extensions=['markdown.extensions.extra',
        #                                   'markdown.extensions.codehilite',
        #                                   'markdown.extensions.toc'])
        md=markdown.Markdown(extensions=['markdown.extensions.extra',
                                         'markdown.extensions.codehilite',
                                         TocExtension(slugify=slugify)])
        post.text=md.convert(post.text)
        post.toc=md.toc


        return post

    def get_context_data(self, **kwargs):
        context=super(PostDetailView,self).get_context_data(**kwargs)
        form=CommentForm()
        comment_list=self.object.comment_set.all()
        context.update({'form':form,'comment_list':comment_list})
        return context
