from django.shortcuts import render, redirect, reverse

from django.views.generic import ListView, DetailView
from django.views.generic import CreateView, DeleteView
from django.views.generic import FormView
from django.views.generic.edit import FormMixin

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy

from django.core.exceptions import PermissionDenied

from barracks.models import Barracks, Invitation
from workday.models import Calculator

from barracks.forms import BarracksForm, CalculatorSearchForm


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
        return super(CreateBarracks, self).form_valid(form)


class BarracksDetail(DetailView):
    model = Barracks
    template_name = "barracks/barracks_detail.html"


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


class TransferToBarracks:
    pass


class QuitBarracks:
    pass
