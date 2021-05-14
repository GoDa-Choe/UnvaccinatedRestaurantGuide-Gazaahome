from django.shortcuts import render
from forum.models import Post


def home(request):
    recent_posts = Post.objects.order_by('-pk')[:5]
    popular_posts = Post.objects.order_by("-hit_count_generic__hits", '-pk')[:5]

    most_likes_posts = sorted(Post.objects.all(), key=lambda post: post.num_likes(), reverse=True)
    most_likes_posts = most_likes_posts[:5]

    context = {
        'recent_posts': recent_posts,
        'popular_posts': popular_posts,
        'most_likes_posts': most_likes_posts,
    }

    return render(
        request,
        'home/index.html',
        context
    )
