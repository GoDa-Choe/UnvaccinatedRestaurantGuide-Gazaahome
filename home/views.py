import datetime
from django.utils import timezone

from django.shortcuts import render
from forum.models import Post, Category
from workday.models import Calculator
from workday.library import calculator_lib
from django.views.generic import TemplateView
from gazahome.settings import GOOGLE_SITE_REGISTER_CODE, NAVER_SITE_REGISTER_CODE
from django.contrib.auth.models import User


def home(request):
    popular_posts = Post.objects.order_by("-hit_count_generic__hits", '-pk')[:3]

    most_likes_posts = sorted(Post.objects.all(), key=lambda post: (post.num_likes(), post.pk), reverse=True)
    most_likes_posts = most_likes_posts[:3]
    context = {
        'popular_posts': popular_posts,
        'most_likes_posts': most_likes_posts,
        'categories': Category.objects.order_by('priority'),
        'google_site_register_code': GOOGLE_SITE_REGISTER_CODE,
        'naver_site_register_code': NAVER_SITE_REGISTER_CODE,
        'now': str(timezone.now())
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


class ContributorView(TemplateView):
    template_name = 'home/contributor.html'

    def get_context_data(self, **kwargs):
        context = super(ContributorView, self).get_context_data()

        num_user = User.objects.count()
        num_calculator = Calculator.objects.count()

        context["num_user"] = num_user
        context["num_calculator"] = num_calculator

        return context
