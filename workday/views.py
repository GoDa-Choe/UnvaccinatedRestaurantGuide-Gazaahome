from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from workday.models import Calculator
import locale, datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from workday.forms import CalculatorForm
from workday.implement import create_block, make_days

locale.setlocale(locale.LC_ALL, 'ko_KR.UTF-8')


class CalculatorCreate(LoginRequiredMixin, CreateView):
    model = Calculator
    form_class = CalculatorForm
    success_url = reverse_lazy('workday:index')

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
            response = super(CalculatorCreate, self).form_valid(form)

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

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['object'] = get_object_or_404(Board, pk=self.kwargs['pk'])
    #     return context

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

        workdays = make_days.make_work_days(service_days)

        temp = []
        for month in blocked_service_days:
            temp1 = []
            for day in month:
                if day in serviced_days:
                    temp1.append((day, False))
                else:
                    if day in workdays:
                        temp1.append((day, True))
                    else:
                        temp1.append((day, False))
            temp.append(temp1)

        temp[0].pop(0)
        temp[-1].pop()

        # context['blocked_service_days'] = blocked_service_days
        context['blocked_service_days'] = temp
        context['service_days'] = len(service_days)
        context['serviced_days'] = len(serviced_days)
        context['workdays'] = len(workdays)
        context['percent'] = f'{len(serviced_days) / len(service_days) * 100 :.2f}'
        context['today'] = datetime.date.today()
        context['remaining_days'] = remaining_days
        return context
