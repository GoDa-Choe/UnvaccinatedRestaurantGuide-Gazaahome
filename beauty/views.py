from django.shortcuts import render, redirect

from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic import CreateView, FormView

from beauty.models import Recode
from beauty.forms import RecordForm, TestForm


class TestView(TemplateView):
    template_name = 'beauty/index.html'


class Test(FormView):
    form_class = TestForm
    template_name = 'beauty/create_record.html'

    def form_valid(self, form):
        current_user = self.request.user
        response = super(Test, self).form_valid(form)

        return redirect(reverse_lazy('beauty:result'))


class CreateRecord(CreateView):
    model = Recode
    form_class = RecordForm
    template_name = 'beauty/create_record.html'
    success_url = '/thanks/'

    def form_valid(self, form):
        current_user = self.request.user
        form.instance.score = 0.0
        obj = form.save()

        return render(self.request, template_name="beauty/index.html", context={"obj": obj})
