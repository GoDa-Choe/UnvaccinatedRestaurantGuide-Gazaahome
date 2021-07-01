from django.shortcuts import render, redirect, reverse

from django.views.generic import ListView, DetailView
from django.views.generic import CreateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy

from django.core.exceptions import PermissionDenied

from barracks.models import Barracks, Invitation
from workday.models import Calculator

from barracks.forms import BarracksForm


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

    # success_url = reverse_lazy('barracks:barracks_list')

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


class InviteToBarracks:
    pass


class TransferToBarracks:
    pass


class QuitBarracks:
    pass
