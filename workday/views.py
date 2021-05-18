from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic import CreateView, DeleteView
from django.views.generic import View
from workday.models import Calculator, Leave, Dayoff
import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from workday.forms import CalculatorForm, LeaveForm, DayoffForm
from workday.implement import create_block, make_days


class CalculatorCreate(LoginRequiredMixin, CreateView):
    model = Calculator
    form_class = CalculatorForm
    success_url = reverse_lazy('workday:index')

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user

            holidays = make_days.get_holidays()
            weekends = make_days.get_weekends()
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
        context = super().get_context_data(**kwargs)

        ob = self.get_object()
        begin_service = ob.start_date
        end_service = ob.end_date

        service_days = make_days.make_service_days(begin_service, end_service)

        blocked_service_days = \
            create_block.make_blocked_service_days(service_days, begin_service, end_service)

        serviced_days = make_days.make_serviced_days(begin_service)
        remaining_days = service_days - serviced_days

        leaves = []
        leave_list = ob.leave_set.all()
        for leave in leave_list:
            leaves.extend(leave.get_leaves())

        dayoffs = []
        dayoff_list = ob.dayoff_set.all()
        for dayoff in dayoff_list:
            dayoffs.append(dayoff.date)

        holidays = make_days.get_holidays()
        weekends = make_days.get_weekends()

        workdays = remaining_days - set(dayoffs) - set(leaves)

        first_weekday = []
        last_weekday = []
        for month in blocked_service_days:
            first_weekday.append(month[0].weekday())
            last_weekday.append(month[-1].weekday())

        for i in range(len(blocked_service_days)):
            first_count = first_weekday[i]
            last_count = 6 - last_weekday[i]
            for j in range(first_count):
                blocked_service_days[i].insert(0, None)
            for j in range(last_count):
                blocked_service_days[i].append(None)

        weekdays = ['월', '화', '수', '목', '금', '토', '일']

        context['blocked_service_days'] = blocked_service_days
        context['service_days'] = service_days
        context['serviced_days'] = serviced_days
        context['workdays'] = workdays
        context['percent'] = f'{len(serviced_days) / len(service_days) * 100 :.2f}'
        context['today'] = datetime.date.today()
        context['remaining_days'] = remaining_days
        context['leaves'] = leaves
        context['weekdays'] = weekdays
        context['dayoffs'] = dayoffs
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
        ob = Calculator.objects.get(pk=self.kwargs['pk'])
        begin_service = ob.start_date
        end_service = ob.end_date

        service_days = make_days.make_service_days(begin_service, end_service)

        blocked_service_days = \
            create_block.make_blocked_service_days(service_days, begin_service, end_service)

        serviced_days = make_days.make_serviced_days(begin_service)
        remaining_days = service_days - serviced_days

        leaves = []
        leave_list = ob.leave_set.all()
        for leave in leave_list:
            leaves.extend(leave.get_leaves())

        dayoffs = []
        dayoff_list = ob.dayoff_set.all()
        for dayoff in dayoff_list:
            dayoffs.append(dayoff.date)

        holidays = make_days.get_holidays()
        weekends = make_days.get_weekends()

        workdays = remaining_days - set(dayoffs) - set(leaves)

        first_weekday = []
        last_weekday = []
        for month in blocked_service_days:
            first_weekday.append(month[0].weekday())
            last_weekday.append(month[-1].weekday())

        for i in range(len(blocked_service_days)):
            first_count = first_weekday[i]
            last_count = 6 - last_weekday[i]
            for j in range(first_count):
                blocked_service_days[i].insert(0, None)
            for j in range(last_count):
                blocked_service_days[i].append(None)

        weekdays = ['월', '활', '수', '목', '금', '토', '일']

        context = {}
        context['calculator'] = ob
        context['blocked_service_days'] = blocked_service_days
        context['service_days'] = service_days
        context['serviced_days'] = serviced_days
        context['workdays'] = workdays
        context['percent'] = f'{len(serviced_days) / len(service_days) * 100 :.2f}'
        context['today'] = datetime.date.today()
        context['remaining_days'] = remaining_days
        context['leaves'] = leaves
        context['weekdays'] = weekdays
        context['dayoffs'] = dayoffs

        return render(request, 'workday/calculator_update.html', context=context)

    def post(self, request, *args, **kwargs):
        calculator = Calculator.objects.get(pk=self.kwargs['pk'])
        past_dayoffs = calculator.dayoff_set.all().delete()

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
