from django.shortcuts import redirect, get_object_or_404

from hitcount.views import HitCountDetailView
from django.views.generic import ListView
from django.views.generic import CreateView, DeleteView, UpdateView
from django.views.generic import View, TemplateView, FormView
from django.views.generic.edit import FormMixin

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from django.core.exceptions import PermissionDenied

from barracks.models import Barracks, Invitation, GuestBook
from workday.models import Calculator

from barracks.forms import BarracksForm, CalculatorSearchForm, GuestBookForm

from collections import Counter

# Core Lib
from workday.library import calculator_lib

# Ranking Lib
import ranking


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
        current_info = calculator_lib.get_workday_from_calculator_ranking(current_calculator)
        context["current_calculator"] = current_calculator
        context["current_info"] = current_info

        calculator_info = {calculator: calculator_lib.get_workday_from_calculator_ranking(calculator)
                           for calculator in Calculator.objects.all()}

        num_remain_days = [info["num_remain_days"] for info in calculator_info.values() if info["num_remain_days"] != 0]
        num_remain_days.sort()
        num_workdays = [info["num_workdays"] for info in calculator_info.values() if info["num_workdays"] != 0]
        num_workdays.sort()

        context["num_remain_days"] = num_remain_days
        context["num_workdays"] = num_workdays

        remaindays_ranking = ranking.Ranking(num_remain_days, start=1, reverse=True)
        workdays_ranking = ranking.Ranking(num_workdays, start=1, reverse=True)

        try:
            current_remaindays_ranking = remaindays_ranking.rank(current_info["num_remain_days"])
        except ValueError:
            current_remaindays_ranking = 0
        context["current_remaindays_ranking"] = current_remaindays_ranking

        try:
            current_workdays_ranking = workdays_ranking.rank(current_info["num_workdays"])
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

        context["remaindays_colors"] = ['rgb(240, 9, 9, 1)' if day == current_info["num_remain_days"]
                                        else 'rgb(21, 67, 235, 1)' for day in remaindays_days_counter.keys()]

        context["workdays_colors"] = ['rgb(240, 9, 9, 1)' if day == current_info["num_workdays"]
                                      else 'rgba(11, 152, 10, 1)' for day in workdays_days_counter.keys()]

        return context
