from django.shortcuts import render,get_object_or_404,redirect


from blog.models import Post

from .models import Comment
from .forms import CommentForm


def post_comment(request,post_pk):
    post=get_object_or_404(Post, pk=post_pk)
    if request.method=='POST':
        form=CommentForm(request.POST) #利用表单数据构造了 CommentForm 的实例，这样 Django 的表单就生成了。

        if form.is_valid():
            comment=form.save(commit=False)   #利用表单生成了模型 类 的实例
            comment.post=post
            comment.save()

            return redirect(post)  #当 redirect 函数接收一个模型的实例时，它会调用这个模型实例的 get_absolute_url 方法，
            # 然后重定向到 get_absolute_url 方法返回的 URL。

        else:
            comment_list=post.comment_set.all()
            context={'post': post,
                       'form': form,
                       'comment_list': comment_list}
            return render(request,'blog/detail.html',context=context)

    return redirect(post)

#post.comment_set.all() 来获取 post 对应的全部评论。
# Comment 和Post 是通过 ForeignKey 关联的，
# 回顾一下我们当初获取某个分类 cate 下的全部文章时的代码：Post.objects.filter(category=cate)。
# 这里 post.comment_set.all() 也等价于 Comment.objects.filter(post=post)，
# 即根据 post 来过滤该 post 下的全部评论。
# 但既然我们已经有了一个 Post 模型的实例 post（它对应的是 Post 在数据库中的一条记录），
# 那么获取和 post 关联的评论列表有一个简单方法，
# 即调用它的 xxx_set 属性来获取一个类似于 objects 的模型管理器，
# 然后调用其 all 方法来返回这个 post 关联的全部评论。
# 其中 xxx_set 中的 xxx 为关联模型的类名（小写）。
# 例如 Post.objects.filter(category=cate) 也可以等价写为 cate.post_set.all()。
# Create your views here.
