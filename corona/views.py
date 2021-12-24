from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from hitcount.views import HitCountDetailView

from corona.models import Restaurant
from corona.forms import RestaurantCommentForm


class MapView(TemplateView):
    template_name = 'corona/map.html'

    def get_context_data(self, **kwargs):
        context = super(MapView, self).get_context_data(**kwargs)

        restaurant_list = Restaurant.objects.all()

        context = {
            'restaurant_list': restaurant_list,
        }

        return context


class RestaurantList(ListView):
    model = Restaurant
    template_name = 'corona/index.html'
    context_object_name = 'restaurant_list'
    paginate_by = 8
    ordering = '-pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RestaurantList, self).get_context_data()

        context['num_restaurants'] = Restaurant.objects.count()

        return context


class RestaurantDetail(HitCountDetailView):
    model = Restaurant
    template_name = 'corona/detail.html'
    count_hit = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RestaurantDetail, self).get_context_data()
        context['restaurant_comment_form'] = RestaurantCommentForm
        context['num_video'] = Restaurant.objects.count()

        return context
