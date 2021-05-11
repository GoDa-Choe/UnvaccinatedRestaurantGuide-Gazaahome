from django.shortcuts import render
from forum.models import Post


def home(request):
    recent_posts = Post.objects.order_by('-pk')[:5]
    context = {
        'recent_posts': recent_posts,
    }

    return render(
        request,
        'home/index.html',
        context
    )
