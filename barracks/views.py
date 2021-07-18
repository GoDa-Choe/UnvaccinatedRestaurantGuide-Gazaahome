from django.shortcuts import redirect, get_object_or_404

from hitcount.views import HitCountDetailView
from django.views.generic import ListView
from django.views.generic import CreateView, DeleteView, UpdateView
from django.views.generic import View, FormView
from django.views.generic.edit import FormMixin

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from django.core.exceptions import PermissionDenied

from barracks.models import Barracks, Invitation, GuestBook
from workday.models import Calculator

from barracks.forms import BarracksForm, CalculatorSearchForm, GuestBookForm

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

    def get_context_data(self, **kwargs):
        context = super(BarracksList, self).get_context_data(**kwargs)

        current_calculator = None
        if self.request.user.is_authenticated:
            current_calculator = Calculator.objects.filter(author=self.request.user).first()
            context['current_calculator'] = current_calculator

        if current_calculator:
            context['my_barracks_list'] = current_calculator.barracks_set.order_by('-created_at')

        return context


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


class BarracksDetail(HitCountDetailView):
    model = Barracks
    template_name = "barracks/barracks_detail.html"
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super(BarracksDetail, self).get_context_data(**kwargs)

        calculator_color_list = list(zip(self.object.members.all(), COLORS))

        unsorted_calculator_list = {(calculator, color): calculator_lib.get_workday_from_calculator_barracks(calculator)
                                    for calculator, color in calculator_color_list}

        sorted_calculator_info_percent_order = {
            calculator_color: info for calculator_color, info
            in sorted(unsorted_calculator_list.items(), key=lambda x: x[-1]['percent'], reverse=True)}

        sorted_calculator_info_workday_order = {
            calculator_color: info for calculator_color, info
            in sorted(unsorted_calculator_list.items(), key=lambda x: x[-1]['workday_percent'], reverse=True)}

        unsorted_calculator_leave_list = {(calculator, color): calculator_lib.get_leave_from_calculator(calculator)
                                          for calculator, color in calculator_color_list}

        sorted_calculator_leave_list = {
            calculator_color: leaves for calculator_color, leaves
            in sorted(unsorted_calculator_leave_list.items(), key=lambda x: x[-1]['total'], reverse=True)}

        first_key = next(iter(sorted_calculator_leave_list))
        max_leaves = sorted_calculator_leave_list[first_key]["total"]

        calculator_lib.get_leave_for_progress(sorted_calculator_leave_list, max_leaves)

        context['calculator_list_percent_order'] = sorted_calculator_info_percent_order
        context['calculator_list_workday_order'] = sorted_calculator_info_workday_order

        context['guest_book_form'] = GuestBookForm

        context['current_calculator'] = None
        if self.request.user.is_authenticated:
            context['current_calculator'] = Calculator.objects.filter(author=self.request.user).first()

        context['calculator_leave_list'] = sorted_calculator_leave_list

        return context


class DeleteInvitation(View):
    def get(self, request, *args, **kwargs):
        invitation = Invitation.objects.get(pk=self.kwargs['invitation_pk'])
        invitation.delete()

        return redirect(reverse_lazy('barracks:search_calculator', args=(self.kwargs['pk'],)))


class SendInvitation(View):
    def get(self, request, *args, **kwargs):
        inviter = request.user
        inviter_calculator = Calculator.objects.filter(author=inviter).first()
        barracks = Barracks.objects.get(pk=self.kwargs['pk'])
        invitee_calculator = Calculator.objects.filter(name=self.kwargs['calculator_name']).first()

        if barracks.members.count() >= 5:
            raise PermissionDenied

        barracks.invitation_set.create(inviter=inviter,
                                       inviter_calculator=inviter_calculator,
                                       invitee=invitee_calculator)
        return redirect(reverse_lazy('barracks:search_calculator', args=(self.kwargs['pk'],)))


class CalculatorSearch(LoginRequiredMixin, FormView):
    form_class = CalculatorSearchForm
    template_name = 'barracks/calculator_search.html'

    def form_valid(self, form):
        calculator_name = form.cleaned_data['calculator_name']
        return redirect(reverse_lazy('barracks:searched_calculator_list', args=(self.kwargs['pk'], calculator_name)))

    def get_context_data(self, **kwargs):
        context = super(CalculatorSearch, self).get_context_data()
        barracks = Barracks.objects.get(pk=self.kwargs['pk'])

        context["barracks"] = barracks
        context["invitation_list"] = barracks.invitation_set.all()
        return context


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

    def get_context_data(self, **kwargs):
        context = super(SearchedCalculatorList, self).get_context_data()
        context["barracks"] = Barracks.objects.get(pk=self.kwargs['pk'])
        return context


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

        if repulicate := barracks.invitation_set.filter(invitee=calculator):
            repulicate.delete()

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


class GuestBookUpdate(LoginRequiredMixin, UpdateView):
    model = GuestBook
    form_class = GuestBookForm
    template_name = 'barracks/guest_book_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(GuestBookUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


def delete_guest_book(request, pk):
    guest_book = get_object_or_404(GuestBook, pk=pk)
    barracks = guest_book.barracks
    if request.user.is_authenticated and request.user == guest_book.author:
        guest_book.delete()
        return redirect(barracks.get_absolute_url())
    else:
        raise PermissionDenied


def new_guest_book(request, pk):
    if request.user.is_authenticated:
        barracks = get_object_or_404(Barracks, pk=pk)
        calculator = Calculator.objects.filter(author=request.user).first()

        if request.method == 'POST':
            guest_book_form = GuestBookForm(request.POST)

            if guest_book_form.is_valid():
                guest_book = guest_book_form.save(commit=False)
                guest_book.author = request.user
                guest_book.calculator = calculator
                guest_book.barracks = barracks
                guest_book.save()

                return redirect(guest_book.get_absolute_url())
        else:
            return redirect(barracks.get_absolute_url())
    else:
        raise PermissionDenied


class InvitationList(LoginRequiredMixin, ListView):
    model = Invitation
    template_name = 'barracks/invitation_list.html'

    def get(self, request, *args, **kwargs):
        response = super(InvitationList, self).get(request, *args, **kwargs)
        calculator = Calculator.objects.filter(author=request.user).first()
        if not calculator:
            return redirect(reverse_lazy('workday:create'))

        return response

    def get_queryset(self):
        user = self.request.user
        calculator = Calculator.objects.filter(author=user).first()

        invitation_list = None
        if calculator:
            invitation_list = calculator.invitation_set.all()

        return invitation_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(InvitationList, self).get_context_data()

        return context


class AcceptInvitation(View):
    def get(self, request, *args, **kwargs):
        calculator = Calculator.objects.filter(author=request.user).first()
        if not calculator:
            return redirect(reverse_lazy('workday:create'))

        barracks_pk = self.kwargs['pk']

        barracks = Barracks.objects.get(pk=barracks_pk)

        if barracks.members.count() >= 5:
            raise PermissionDenied
        barracks.members.add(calculator)

        invitation = Invitation.objects.get(pk=self.kwargs['invitation_pk'])
        invitation.delete()

        return redirect(reverse_lazy('barracks:barracks_detail', args=(barracks_pk,)))
