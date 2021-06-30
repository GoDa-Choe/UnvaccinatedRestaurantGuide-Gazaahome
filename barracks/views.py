from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic import CreateView, DeleteView

from barracks.models import Barracks, Invitation
from workday.models import Calculator


# Create your views here.
class BarracksList(ListView):
    model = Barracks
    template_name = 'barracks/barracks_list.html'
    context_object_name = 'barracks_list'
    ordering = '-created_at'
    paginate_by = 10


class DeleteBarracks:
    pass


class CreateBarracks:
    pass


class BarracksDetail:
    pass


class InviteToBarracks:
    pass


class TransferToBarracks:
    pass


class QuitBarracks:
    pass
