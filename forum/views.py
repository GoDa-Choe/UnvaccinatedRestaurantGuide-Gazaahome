from django.shortcuts import render
from forum.models import Post
from django.views.generic import ListView


class PostList(ListView):
    model = Post
    template_name = 'forum/post_list.html'
    ordering = '-pk'


def detail(request, pk):
    post = Post.objects.get(pk=pk)
    context_data = {'post': post}

    return render(
        request,
        'forum/detail.html',
        context_data
    )
