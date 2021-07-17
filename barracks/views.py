from django.shortcuts import render, redirect, reverse

from django.views.generic import ListView, DetailView
from django.views.generic import CreateView, DeleteView
from django.views.generic import View, FormView
from django.views.generic.edit import FormMixin

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy

from django.core.exceptions import PermissionDenied

from barracks.models import Barracks, Invitation
from workday.models import Calculator

from barracks.forms import BarracksForm, CalculatorSearchForm

# Core Lib
from workday.library import calculator_lib

COLORS = [
    "primary",
    "warning",
    "danger",
    "success",
    "info",
]

MAXIMUM = 5  # the number of maximum members of a barracks


# Create your views here.
class BarracksList(ListView):
    model = Barracks
    template_name = 'barracks/barracks_list.html'
    context_object_name = 'barracks_list'
    ordering = '-created_at'
    paginate_by = 10


class DeleteBarracks(DeleteView):
    model = Barracks
    template_name = "barracks/barracks_delete.html"
    success_url = reverse_lazy('barracks:barracks_list')


class CreateBarracks(LoginRequiredMixin, CreateView):
    model = Barracks
    form_class = BarracksForm

    def dispatch(self, request, *args, **kwargs):
        calculator = Calculator.objects.filter(author=self.request.user).first()
        if calculator:
            return super(CreateBarracks, self).dispatch(request, *args, **kwargs)

        return redirect(reverse_lazy('workday:create'))

    def form_valid(self, form):
        current_user = self.request.user
        form.instance.host = current_user
        response = super(CreateBarracks, self).form_valid(form)

        current_calculator = Calculator.objects.filter(author=self.request.user).first()
        self.object.members.add(current_calculator)

        return response


class BarracksDetail(DetailView):
    model = Barracks
    template_name = "barracks/barracks_detail.html"

    def get_context_data(self, **kwargs):
        context = super(BarracksDetail, self).get_context_data(**kwargs)

        calculator_color_list = zip(self.object.members.all(), COLORS)

        unsorted_calculator_list = {(calculator, color): calculator_lib.get_workday_from_calculator_barracks(calculator)
                                    for calculator, color in calculator_color_list}

        sorted_calculator_info_percent_order = {
            calculator_color: info for calculator_color, info
            in sorted(unsorted_calculator_list.items(), key=lambda x: x[-1]['percent'], reverse=True)}

        sorted_calculator_info_workday_order = {
            calculator_color: info for calculator_color, info
            in sorted(unsorted_calculator_list.items(), key=lambda x: x[-1]['workday_percent'], reverse=True)}

        context['calculator_list_percent_order'] = sorted_calculator_info_percent_order
        context['calculator_list_workday_order'] = sorted_calculator_info_workday_order

        temp = [[1, 2], [3, 4]]
        context["temp"] = temp

        return context


class InviteToBarracks(CreateBarracks):
    pass


class CalculatorSearch(LoginRequiredMixin, FormView):
    form_class = CalculatorSearchForm
    template_name = 'barracks/calculator_search.html'

    def form_valid(self, form):
        calculator_name = form.cleaned_data['calculator_name']
        return redirect(reverse_lazy('barracks:searched_calculator_list', args=(self.kwargs['pk'], calculator_name)))


class SearchedCalculatorList(LoginRequiredMixin, FormMixin, ListView):
    model = Calculator
    form_class = CalculatorSearchForm
    template_name = 'barracks/searched_calculator_list.html'
    context_object_name = 'searched_calculator_list'
    ordering = '-created_at'
    paginate_by = 10

    def get_queryset(self):
        searched_calculator_list = Calculator.objects.filter(name__icontains=self.kwargs['calculator_name'])
        return searched_calculator_list

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        calculator_name = form.cleaned_data['calculator_name']
        return redirect(reverse_lazy('barracks:searched_calculator_list', args=(self.kwargs['pk'], calculator_name)))


class TransferToBarracks(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        calculator = Calculator.objects.filter(author=request.user).first()
        if not calculator:
            return redirect(reverse_lazy('workday:create'))

        barracks_pk = self.kwargs['pk']

        barracks = Barracks.objects.get(pk=barracks_pk)

        if barracks.members.count() >= 5:
            raise PermissionDenied

        barracks.members.add(calculator)
        return redirect(reverse_lazy('barracks:barracks_detail', args=(barracks_pk,)))


class QuitBarracks(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):

        barracks_pk = self.kwargs['pk']
        barracks = Barracks.objects.get(pk=barracks_pk)

        member_calculator = barracks.members.filter(author=request.user)
        if not member_calculator.exists():
            raise PermissionDenied

        member_calculator = member_calculator.first()

        if barracks.members.count() == 1:
            barracks.delete()
            return redirect(reverse_lazy('barracks:barracks_list'))

        barracks.members.remove(member_calculator)
        return redirect(reverse_lazy('barracks:barracks_detail', args=(barracks_pk,)))
