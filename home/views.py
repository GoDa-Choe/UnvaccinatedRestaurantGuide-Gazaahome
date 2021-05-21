from django.shortcuts import render
from forum.models import Post, Category
from workday.models import Calculator
from workday.library import calculator_lib
from django.views.generic import TemplateView


def home(request):
    popular_posts = Post.objects.order_by("-hit_count_generic__hits", '-pk')[:3]

    most_likes_posts = sorted(Post.objects.all(), key=lambda post: (post.num_likes(), post.pk), reverse=True)
    most_likes_posts = most_likes_posts[:3]
    context = {
        'popular_posts': popular_posts,
        'most_likes_posts': most_likes_posts,
        'categories': Category.objects.all()
    }

    if request.user.is_authenticated:
        calculator = Calculator.objects.filter(author=request.user).first()
        if calculator:
            context['calculator'] = calculator
            new = calculator_lib.get_workday_from_calculator_light(calculator)
            context.update(new)
            return render(request, 'home/home.html', context)

    return render(
        request,
        'home/home.html',
        context
    )


class RobotView(TemplateView):
    template_name = 'home/robots.txt'
    content_type = 'text/plain'
