from django.shortcuts import render
from forum.models import Post, Category
from workday.models import Calculator
from workday.library import calculator_lib


def temp(request):
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


def home(request):
    recent_posts = Post.objects.order_by('-pk')[:5]
    popular_posts = Post.objects.order_by("-hit_count_generic__hits", '-pk')[:3]

    most_likes_posts = sorted(Post.objects.all(), key=lambda post: post.num_likes(), reverse=True)
    most_likes_posts = most_likes_posts[:3]
    context = {
        'recent_posts': recent_posts,
        'popular_posts': popular_posts,
        'most_likes_posts': most_likes_posts,
        'categories': Category.objects.all()
    }

    if request.user.is_authenticated:
        calculator = Calculator.objects.filter(author=request.user).first()
        if calculator:
            context['calculator'] = calculator
            new = calculator_lib.get_workday_from_calculator(calculator)
            context.update(new)
            return render(request, 'home/home.html', context)

    return render(
        request,
        'home/home.html',
        context
    )
