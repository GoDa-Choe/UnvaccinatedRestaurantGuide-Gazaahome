from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic import CreateView, DeleteView
from django.views.generic import View
from workday.models import Calculator, Leave, Dayoff
import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from workday.forms import CalculatorForm, LeaveForm, DayoffForm

from workday.library import calculator_lib


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
            weekends = calculator_lib.make_days.get_weekends()
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


class CalculatorDetail(LoginRequiredMixin, DetailView):
    model = Calculator
    template_name = 'workday/calculator_detail.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super(CalculatorDetail, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super(CalculatorDetail, self).get_context_data(**kwargs)
        calculator = self.get_object()
        new = calculator_lib.get_workday_from_calculator(calculator)
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

    def get_success_url(self):
        return reverse_lazy('workday:index')


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
