from django.shortcuts import redirect

from django.views.generic import TemplateView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from workday.models import Calculator
from rank.models import RankingChart

from collections import Counter

from workday.library import calculator_lib

# Ranking Lib
import ranking

# Chart bar colors
GREEN = 'rgb(7,123,6)'
BLUE = 'rgb(6,44,187)'
RED = 'rgb(174,9,9)'


class RankingView(LoginRequiredMixin, TemplateView):
    template_name = "rank/ranking_index.html"

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            calculator = Calculator.objects.filter(author=request.user).first()
            if not calculator:
                return redirect(reverse_lazy('workday:create'))

        return super(RankingView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RankingView, self).get_context_data()

        current_calculator = Calculator.objects.get(author=self.request.user)
        current_chart_item = RankingChart.objects.get(calculator=current_calculator)
        context["current_chart_item"] = current_chart_item

        num_remain_days = [chart_itme.num_remaindays
                           for chart_itme in RankingChart.objects.exclude(num_remaindays=0).order_by('num_remaindays')]

        num_workdays = [chart_itme.num_workdays
                        for chart_itme in RankingChart.objects.exclude(num_workdays=0).order_by('num_workdays')]

        remaindays_ranking = ranking.Ranking(num_remain_days, start=1, reverse=True)
        workdays_ranking = ranking.Ranking(num_workdays, start=1, reverse=True)

        try:
            current_remaindays_ranking = remaindays_ranking.rank(current_chart_item.num_remaindays)
        except ValueError:
            current_remaindays_ranking = 0
        context["current_remaindays_ranking"] = current_remaindays_ranking

        try:
            current_workdays_ranking = workdays_ranking.rank(current_chart_item.num_workdays)
        except ValueError:
            current_workdays_ranking = 0
        context["current_workdays_ranking"] = current_workdays_ranking

        remaindays_ranking_length = len(num_remain_days)
        context["remaindays_ranking_length"] = remaindays_ranking_length
        workdays_ranking_length = len(num_workdays)
        context["workdays_ranking_length"] = workdays_ranking_length

        current_remaindays_ranking_percentage = round(current_remaindays_ranking / remaindays_ranking_length * 100, 1)
        context["current_remaindays_ranking_percentage"] = current_remaindays_ranking_percentage

        current_workdays_ranking_percentage = round(current_workdays_ranking / workdays_ranking_length * 100, 1)
        context["current_workdays_ranking_percentage"] = current_workdays_ranking_percentage

        context["remaindays_ranking"] = {value: rank for rank, value in remaindays_ranking}
        context["workdays_ranking"] = {value: rank for rank, value in workdays_ranking}

        remaindays_days_counter = Counter(num_remain_days)
        context["remaindays_days"] = [day for day in remaindays_days_counter.keys()]
        context["remaindays_counter"] = [round(counter / remaindays_ranking_length * 100, 1)
                                         for counter in remaindays_days_counter.values()]

        workdays_days_counter = Counter(num_workdays)
        context["workdays_days"] = [day for day in workdays_days_counter.keys()]
        context["workdays_counter"] = [round(counter / workdays_ranking_length * 100, 1)
                                       for counter in workdays_days_counter.values()]

        context["remaindays_colors"] = [RED if day == current_chart_item.num_remaindays
                                        else BLUE for day in remaindays_days_counter.keys()]

        context["workdays_colors"] = [RED if day == current_chart_item.num_workdays
                                      else GREEN for day in workdays_days_counter.keys()]

        return context


class RankingLineView(LoginRequiredMixin, TemplateView):
    template_name = "rank/ranking_test.html"

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            calculator = Calculator.objects.filter(author=request.user).first()
            if not calculator:
                return redirect(reverse_lazy('workday:create'))

        return super(RankingLineView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RankingLineView, self).get_context_data()

        current_calculator = Calculator.objects.get(author=self.request.user)
        info = calculator_lib.get_workday_from_calculator_ranking(current_calculator)
        obj, is_created = RankingChart.objects.update_or_create(
            calculator=current_calculator,
            defaults={
                'start_date': current_calculator.start_date,
                'end_date': current_calculator.end_date,
                'end_workday': info['end_workday'],

                'num_remaindays': info['num_remain_days'],
                'num_workdays': info['num_workdays'],

                'percent': info['percent'],
                'workday_percent': info['workday_percent']
            }

        )

        current_chart_item = obj
        context["current_chart_item"] = current_chart_item

        num_remain_days = [chart_itme.num_remaindays
                           for chart_itme in RankingChart.objects.exclude(num_remaindays=0).order_by('num_remaindays')]

        num_workdays = [chart_itme.num_workdays
                        for chart_itme in RankingChart.objects.exclude(num_workdays=0).order_by('num_workdays')]

        remaindays_ranking = ranking.Ranking(num_remain_days, start=1, reverse=True)
        workdays_ranking = ranking.Ranking(num_workdays, start=1, reverse=True)

        try:
            current_remaindays_ranking = remaindays_ranking.rank(current_chart_item.num_remaindays)
        except ValueError:
            current_remaindays_ranking = 0
        context["current_remaindays_ranking"] = current_remaindays_ranking

        try:
            current_workdays_ranking = workdays_ranking.rank(current_chart_item.num_workdays)
        except ValueError:
            current_workdays_ranking = 0
        context["current_workdays_ranking"] = current_workdays_ranking

        remaindays_ranking_length = len(num_remain_days)
        context["remaindays_ranking_length"] = remaindays_ranking_length
        workdays_ranking_length = len(num_workdays)
        context["workdays_ranking_length"] = workdays_ranking_length

        current_remaindays_ranking_percentage = round(current_remaindays_ranking / remaindays_ranking_length * 100, 1)
        context["current_remaindays_ranking_percentage"] = current_remaindays_ranking_percentage

        current_workdays_ranking_percentage = round(current_workdays_ranking / workdays_ranking_length * 100, 1)
        context["current_workdays_ranking_percentage"] = current_workdays_ranking_percentage

        context["remaindays_ranking"] = {value: rank for rank, value in remaindays_ranking}
        context["workdays_ranking"] = {value: rank for rank, value in workdays_ranking}

        remaindays_days_counter = Counter(num_remain_days)
        context["remaindays_days"] = [day for day in remaindays_days_counter.keys()]
        context["remaindays_counter"] = [round(counter / remaindays_ranking_length * 100, 1)
                                         for counter in remaindays_days_counter.values()]

        workdays_days_counter = Counter(num_workdays)
        context["workdays_days"] = [day for day in workdays_days_counter.keys()]
        context["workdays_counter"] = [round(counter / workdays_ranking_length * 100, 1)
                                       for counter in workdays_days_counter.values()]

        context["remaindays_colors"] = [RED if day == current_chart_item.num_remaindays
                                        else BLUE for day in remaindays_days_counter.keys()]

        context["workdays_colors"] = [RED if day == current_chart_item.num_workdays
                                      else GREEN for day in workdays_days_counter.keys()]

        return context
