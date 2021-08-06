from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy

from hitcount.views import HitCountDetailView
from django.views.generic import ListView
from django.views.generic import CreateView, DeleteView
from django.views.generic import View, FormView
from django.views.generic.edit import FormMixin

from workday.models import Calculator, Leave, Dayoff
from rank.models import RankingChart
import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from workday.forms import CalculatorForm, LeaveForm, DayoffForm, CalculatorSearchForm

from workday.library import calculator_lib


class CalculatorSearch(LoginRequiredMixin, FormView):
    form_class = CalculatorSearchForm
    template_name = 'workday/calculator_search.html'

    def form_valid(self, form):
        calculator_name = form.cleaned_data['calculator_name']
        calculator = Calculator.objects.get(name=calculator_name)

        return redirect(reverse_lazy('workday:detail', args=(calculator.pk,)))


class SearchedCalculatorList(LoginRequiredMixin, FormMixin, ListView):
    model = Calculator
    form_class = CalculatorSearchForm
    template_name = 'workday/searched_calculator_list.html'
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
        return redirect(reverse_lazy('workday:searched_list', args=(calculator_name,)))


class CalculatorCreate(LoginRequiredMixin, CreateView):
    model = Calculator
    form_class = CalculatorForm
    success_url = reverse_lazy('workday:index')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            calculator = Calculator.objects.filter(author=self.request.user).first()
            if not calculator:
                return super(CalculatorCreate, self).dispatch(request, *args, **kwargs)

        raise PermissionDenied

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user

            holidays = calculator_lib.make_days.get_holidays()
            weekends = calculator_lib.make_days.get_weekends(form.cleaned_data['start_date'],
                                                             form.cleaned_data['end_date'])
            response = super(CalculatorCreate, self).form_valid(form)

            for holiday in holidays:
                record = Dayoff(date=holiday, calculator=form.instance)
                record.save()

            for weekend in weekends:
                record = Dayoff(date=weekend, calculator=form.instance)
                record.save()

            return response
        else:
            return redirect('/workday/')


class CalculatorList(LoginRequiredMixin, ListView):
    model = Calculator
    template_name = 'workday/calculator_list.html'
    paginate_by = 20
    ordering = '-pk'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super(CalculatorList, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CalculatorList, self).get_context_data()
        calculator_list = Calculator.objects.filter(author=self.request.user)
        context['calculator_list'] = calculator_list
        return context


class CalculatorDetail(LoginRequiredMixin, FormMixin, HitCountDetailView):
    model = Calculator
    form_class = CalculatorSearchForm
    template_name = 'workday/calculator_detail.html'
    count_hit = True

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super(CalculatorDetail, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        calculator_name = form.cleaned_data['calculator_name']

        return redirect(reverse_lazy('workday:searched_list', args=(calculator_name,)))

    def get_context_data(self, **kwargs):
        context = super(CalculatorDetail, self).get_context_data(**kwargs)
        calculator = self.get_object()

        new = calculator_lib.get_workday_from_calculator(calculator)

        obj, is_created = RankingChart.objects.update_or_create(
            calculator=calculator,
            defaults={
                "start_date": calculator.start_date,
                "end_date": calculator.end_date,
                "end_workday": new['end_workday'],
                "num_remaindays": new['num_remain_days'],
                "num_workdays": new['num_workdays'],
                "percent": float(new['percent']),
                "workday_percent": float(new['workday_percent'])
            }
        )

        context.update(new)
        return context


class LeaveCreate(LoginRequiredMixin, CreateView):
    model = Leave
    form_class = LeaveForm

    def dispatch(self, request, *args, **kwargs):
        current_calculator = Calculator.objects.get(pk=self.kwargs['pk'])
        if current_calculator.author == self.request.user:
            return super(LeaveCreate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_form_kwargs(self):
        kwargs = super(LeaveCreate, self).get_form_kwargs()
        kwargs['calculator'] = Calculator.objects.get(pk=self.kwargs['pk'])
        return kwargs

    def form_valid(self, form):
        current_calculator = Calculator.objects.get(pk=self.kwargs['pk'])
        form.instance.calculator = current_calculator
        response = super(LeaveCreate, self).form_valid(form)
        return response

    def get_success_url(self):
        return reverse_lazy('workday:detail', args=(self.kwargs['pk'],))


class LeaveDelete(LoginRequiredMixin, DeleteView):
    model = Leave
    form_class = LeaveForm
    template_name = 'workday/leave_delete.html'

    def dispatch(self, request, *args, **kwargs):
        current_calculator = Calculator.objects.get(pk=self.kwargs['cal'])
        if current_calculator.author == self.request.user:
            return super(LeaveDelete, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_success_url(self):
        return reverse_lazy('workday:detail', args=(self.kwargs['cal'],))


class CalculatorDelete(LoginRequiredMixin, DeleteView):
    model = Calculator
    form_class = CalculatorForm
    template_name = 'workday/calculator_delete.html'

    def dispatch(self, request, *args, **kwargs):
        current_calculator = Calculator.objects.get(pk=self.kwargs['pk'])
        if current_calculator.author == self.request.user:
            return super(CalculatorDelete, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def delete(self, request, *args, **kwargs):
        current_calculator = Calculator.objects.get(pk=self.kwargs['pk'])
        barracks_list = current_calculator.barracks_set.all()
        for barracks in barracks_list:
            if barracks.members.count() == 1:
                barracks.delete()

        return super(CalculatorDelete, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('workday:create')


class CalculatorUpdate(LoginRequiredMixin, View):
    template_name = 'workday/calculator_update.html'

    def dispatch(self, request, *args, **kwargs):
        current_calculator = Calculator.objects.get(pk=self.kwargs['pk'])
        if current_calculator.author == self.request.user:
            return super(CalculatorUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_success_url(self):
        return reverse_lazy('workday:detail', args=(self.kwargs['pk'],))

    def get(self, request, *args, **kwargs):
        calculator = Calculator.objects.get(pk=self.kwargs['pk'])
        context = calculator_lib.get_workday_from_calculator(calculator)
        context['calculator'] = calculator
        return render(request, 'workday/calculator_update.html', context)

    def post(self, request, *args, **kwargs):
        calculator = Calculator.objects.get(pk=self.kwargs['pk'])
        calculator.dayoff_set.all().delete()
        dayoffs = request.POST.getlist('dayoffs')

        if dayoffs:
            for dayoff in dayoffs:
                dayoff_date = datetime.datetime.fromisoformat(dayoff)
                form = DayoffForm({'date': dayoff_date, 'calculator': calculator})
                if form.is_valid():
                    date = form.cleaned_data['date']
                    record = Dayoff(date=date, calculator=calculator)
                    record.save()
                else:
                    return redirect(reverse_lazy('workday:detail', args=(self.kwargs['pk'],)))
        return redirect(reverse_lazy('workday:detail', args=(self.kwargs['pk'],)))


def redirect_calculator(request):
    if request.user.is_authenticated:
        calculator = Calculator.objects.filter(author=request.user).first()
        if calculator:
            return redirect(reverse('workday:detail', args=(calculator.pk,)))
        else:
            return redirect('workday:create')
    else:
        raise PermissionDenied
