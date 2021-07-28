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

    def get_context_data(self, **kwargs):
        context = super(RankingView, self).get_context_data()

        calculator_info = {calculator: calculator_lib.get_workday_from_calculator_ranking(calculator)
                           for calculator in Calculator.objects.all()}

        context["calculator_info"] = calculator_info

        num_remain_days = [info["num_remain_days"] for info in calculator_info.values() if info["num_remain_days"] != 0]
        num_remain_days.sort()
        num_workdays = [info["num_workdays"] for info in calculator_info.values() if info["num_workdays"] != 0]
        num_workdays.sort()

        context["num_remain_days"] = num_remain_days
        context["num_workdays"] = num_workdays

        remaindays_ranking = list(ranking.Ranking(num_remain_days, start=1, reverse=True))
        workdays_ranking = list(ranking.Ranking(num_workdays, start=1, reverse=True))

        context["remaindays_ranking"] = remaindays_ranking
        context["workdays_ranking"] = workdays_ranking

        remaindays_ranks = [item[0] for item in remaindays_ranking]
        remaindays_days = [item[1] for item in remaindays_ranking]

        remaindays_ranks = [item[0] for item in remaindays_ranking]
        workdays_days = [item[1] for item in workdays_ranking]

        remaindays_days_counter = Counter(remaindays_days)
        context["remaindays_days"] = [f"D-{day}" for day in remaindays_days_counter.keys()]
        context["remaindays_days_length"] = len(list(remaindays_days_counter))
        context["remaindays_days_counter"] = [round(counter / len(list(remaindays_days_counter)) * 100, 2)
                                              for counter in remaindays_days_counter.values()]

        workdays_days_counter = Counter(workdays_days)
        context["workdays_days"] = list(workdays_days_counter.keys())
        context["workdays_days_counter"] = list(workdays_days_counter.values())

        return context
