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
