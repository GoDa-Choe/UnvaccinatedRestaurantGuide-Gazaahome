from django.db.models import Count

from django.conf import settings

from corona.models import Restaurant, Post

from django.views.generic import TemplateView, FormView

from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied

from video_forum.models import Video

from home.forms import CheckPasswordForm

from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


def get_service(api_name, api_version, scopes, key_file_location):
    """Get a service that communicates to a Google API.

    Args:
        api_name: The name of the api to connect to.
        api_version: The api version to connect to.
        scopes: A list auth scopes to authorize for the application.
        key_file_location: The path to a valid service account JSON key file.

    Returns:
        A service that is connected to the specified API.
    """

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        key_file_location, scopes=scopes)

    # Build the service object.
    service = build(api_name, api_version, credentials=credentials)

    return service


# Define the auth scopes to request.
scope = 'https://www.googleapis.com/auth/analytics.readonly'
key_file_location = settings.BASE_DIR / 'corona_home/guide-336820-3c09a7278a31.json'


# Create your views here.
class ContributorView(TemplateView):
    template_name = 'corona_home/contributors.html'

    start_date = '2021-12-26'
    ids = 'ids=ga%3A247902589'
    metrics = 'metrics=ga%3Ausers%2Cga%3Apageviews'
    access_token = "access_token=ya29.a0ARrdaM9unYhPBVuTHbO_SD--qG00IqaKmf4wc4gdIYgAJmONUsCFVWZU9PtP77V8ngo15nMT8ue1VaM4JmTBds-b01n-jz356Kw4uniZQsrYjKGmN-5S7Rsso7qtoJ40paPhg6NWc1MlXv5UEsRm7w1S9gGa"

    def get_context_data(self, **kwargs):
        context = super(ContributorView, self).get_context_data()

        # Authenticate and construct service.
        service = get_service(
            api_name='analytics',
            api_version='v3',
            scopes=[scope],
            key_file_location=key_file_location)

        accounts = service.management().accounts().list().execute()
        if accounts.get('items'):
            # Get the first Google Analytics account.
            account = accounts.get('items')[0].get('id')

            # Get a list of all the properties for the first account.
            properties = service.management().webproperties().list(accountId=account).execute()

        # 일주일간 세션수와, 페이지뷰수 받아오기
        total = service.data().ga().get(
            ids='ga:247902589',
            start_date='2021-12-26',
            end_date='today',
            metrics='ga:users,ga:pageviews').execute()
        today = service.data().ga().get(
            ids='ga:247902589',
            start_date='today',
            end_date='today',
            metrics='ga:users,ga:pageviews').execute()

        context['total'] = self.parsing(total)
        context['today'] = self.parsing(today)

        num_restaurants = Restaurant.objects.count()
        context["num_restaurants"] = num_restaurants

        return context

    def parsing(self, response):
        num_users = response['totalsForAllResults']['ga:users']
        num_pageviews = response['totalsForAllResults']['ga:pageviews']
        result = {
            "num_users": num_users,
            "num_pageviews": num_pageviews
        }
        return result


class HomeView(TemplateView):
    template_name = 'corona_home/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        restaurant_list = Restaurant.objects.annotate(
            num_likes=Count('likes', distinct=True)).annotate(
            num_comments=Count('restaurantcomment', distinct=True)
        )

        num_restaurants = 4

        mostrecent_restuarant_list = restaurant_list.order_by('-pk')[:num_restaurants]
        mostpopular_restuarant_list = restaurant_list.order_by('-hit_count_generic__hits', '-pk')[:num_restaurants]
        mostlikes_restuarant_list = restaurant_list.order_by('-num_likes', '-pk')[:num_restaurants]
        mostcomments_restuarant_list = restaurant_list.order_by('-num_comments', '-pk')[:num_restaurants]

        mostrecent_post_list = Post.objects.order_by('-pk')[:4]
        mostrecent_video_list = Video.objects.order_by('-pk')[:2]

        extension = {
            "mostrecent_restuarant_list": mostrecent_restuarant_list,
            "mostpopular_restuarant_list": mostpopular_restuarant_list,
            "mostlikes_restuarant_list": mostlikes_restuarant_list,
            "mostcomments_restuarant_list": mostcomments_restuarant_list,

            "mostrecent_post_list": mostrecent_post_list,
            "mostrecent_video_list": mostrecent_video_list
        }

        context.update(extension)

        return context


class GodaSoftStudioView(TemplateView):
    template_name = 'corona_home/goda_soft_studio.html'


class RobotView(TemplateView):
    template_name = 'corona_home/robots.txt'
    content_type = 'text/plain'


class PrivacyView(TemplateView):
    template_name = 'corona_home/policy/privacy.html'


class PolicyView(TemplateView):
    template_name = 'corona_home/policy/policy.html'


class LicenseView(TemplateView):
    template_name = 'corona_home/policy/license.html'


class PofileView(LoginRequiredMixin, TemplateView):
    template_name = 'account/corona_profile.html'

    def get_context_data(self, **kwargs):
        context = super(PofileView, self).get_context_data(**kwargs)
        password_form = CheckPasswordForm(self.request.user)
        context['password_form'] = password_form
        return context
