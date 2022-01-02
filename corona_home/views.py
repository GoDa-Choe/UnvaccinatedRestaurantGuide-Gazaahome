from django.shortcuts import render
from django.views.generic import TemplateView

from django.db.models import Count

from django.conf import settings

from corona.models import Restaurant, Post
from video_forum.models import Video

from gazahome.settings import GOOGLE_SITE_REGISTER_CODE, NAVER_SITE_REGISTER_CODE

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
            num_likes=Count('likes')).annotate(
            num_comments=Count('restaurantcomment')
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


def home(request):
    popular_posts = Post.objects.order_by("-pk")[:5]

    most_likes_posts = sorted(Post.objects.all(), key=lambda post: (post.num_likes(), post.pk), reverse=True)
    most_likes_posts = most_likes_posts[:4]
    most_recently_posts = Post.objects.order_by('-pk')[:4]

    most_recently_videos = Video.objects.order_by('-pk')[:3]

    # popular_troops = Troop.objects.order_by("-hit_count_generic__hits", '-pk')[:3]

    # popular_barracks = Barracks.objects.exclude(is_close=True).order_by("-hit_count_generic__hits", '-pk')[:2]

    context = {
        'popular_posts': popular_posts,
        'most_likes_posts': most_likes_posts,
        'most_recently_posts': most_recently_posts,

        'most_recently_videos': most_recently_videos,

        # 'popular_troops': popular_troops,

        # 'popular_barracks': popular_barracks,

        # 'categories': Category.objects.order_by('priority'),
        'google_site_register_code': GOOGLE_SITE_REGISTER_CODE,
        'naver_site_register_code': NAVER_SITE_REGISTER_CODE,
        # 'now': str(timezone.now())
    }

    # if request.user.is_authenticated:
    #     calculator = Calculator.objects.filter(author=request.user).first()
    #     if calculator:
    #         context['calculator'] = calculator
    #         new = calculator_lib.get_workday_from_calculator_light(calculator)
    #         context.update(new)
    #         return render(request, 'home/home.html', context)

    return render(
        request,
        'corona_home/home.html',
        context
    )
