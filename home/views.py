from django.utils import timezone

from django.shortcuts import render, redirect
from workday.library import calculator_lib
from django.views.generic import TemplateView, DeleteView, FormView
from gazahome.settings import GOOGLE_SITE_REGISTER_CODE, NAVER_SITE_REGISTER_CODE
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from forum.models import Post, Category
from workday.models import Calculator
from video_forum.models import Video
from troop_review.models import Troop
from barracks.models import Barracks

from home.forms import CheckPasswordForm


def home(request):
    popular_posts = Post.objects.order_by("-hit_count_generic__hits", '-pk')[:4]

    most_likes_posts = sorted(Post.objects.all(), key=lambda post: (post.num_likes(), post.pk), reverse=True)
    most_likes_posts = most_likes_posts[:4]
    most_recently_posts = Post.objects.order_by('-pk')[:4]

    most_recently_videos = Video.objects.order_by('-pk')[:3]

    popular_troops = Troop.objects.order_by("-hit_count_generic__hits", '-pk')[:2]

    popular_barracks = Barracks.objects.exclude(is_close=True).order_by("-hit_count_generic__hits", '-pk')[:2]

    context = {
        'popular_posts': popular_posts,
        'most_likes_posts': most_likes_posts,
        'most_recently_posts': most_recently_posts,

        'most_recently_videos': most_recently_videos,

        'popular_troops': popular_troops,

        'popular_barracks': popular_barracks,

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


class GodaSoftStudioView(TemplateView):
    template_name = 'home/goda_soft_studio.html'


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


class PrivacyView(TemplateView):
    template_name = 'home/policy/privacy.html'


class PolicyView(TemplateView):
    template_name = 'home/policy/policy.html'


class LicenseView(TemplateView):
    template_name = 'home/policy/license.html'


class PofileView(LoginRequiredMixin, TemplateView):
    template_name = 'account/profile.html'

    def get_context_data(self, **kwargs):
        context = super(PofileView, self).get_context_data(**kwargs)
        calculator = Calculator.objects.filter(author=self.request.user).first()
        context['calculator'] = calculator
        password_form = CheckPasswordForm(self.request.user)
        context['password_form'] = password_form
        return context


class AccountDeleteView(LoginRequiredMixin, FormView):
    form_class = CheckPasswordForm
    template_name = 'account/account_delete.html'

    def dispatch(self, request, *args, **kwargs):

        current_user = self.request.user

        if current_user.is_authenticated:
            current_user_id = current_user.id

            if current_user_id == self.kwargs['pk']:
                return super(AccountDeleteView, self).dispatch(request, *args, **kwargs)
            else:
                raise PermissionDenied

        else:
            raise PermissionDenied

    def get_form(self, form_class=None):
        return CheckPasswordForm(self.request.user, self.request.POST)

    def form_valid(self, form):
        self.request.user.delete()
        return super(AccountDeleteView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('home:home')
