from django.shortcuts import render
from forum.models import Post


def index(request):
    posts = Post.objects.all().order_by('-pk')
    context_data = {'posts': posts}

    return render(
        request,
        'forum/index.html',
        context_data
    )


def detail(request, pk):
    post = Post.objects.get(pk=pk)
    context_data = {'post': post}

    return render(
        request,
        'forum/detail.html',
        context_data
    )
