from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from hitcount.views import HitCountDetailView

# forms
from troop_review.forms import TroopForm, ReviewForm

# models
from troop_review.models import Troop, Review

# python lib
from collections import Counter


@require_POST
@login_required
def like(request, troop_pk, pk):
    review = get_object_or_404(Review, pk=request.POST.get('review_pk'))
    if review.likes.filter(pk=request.user.pk).exists():
        review.likes.remove(request.user)
    else:
        review.likes.add(request.user)

    return HttpResponseRedirect(reverse('troop_review:detail', args=(troop_pk,)))


class TroopList(ListView):
    model = Troop
    template_name = 'troop_review/index.html'
    context_object_name = 'troop_reivew_list'
    paginate_by = 10


class TroopDetail(LoginRequiredMixin, HitCountDetailView):
    model = Troop
    template_name = 'troop_review/detail.html'
    count_hit = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TroopDetail, self).get_context_data()

        current_troop = context['troop']

        review_list = current_troop.review_set

        training_list = [review.get_training_display() for review in review_list.iterator()]
        training_counter = Counter(training_list)
        context["training_size"] = len(training_list)
        context["training_keys"] = list(training_counter.keys())
        context["training_values"] = list(training_counter.values())

        discipline_list = [review.get_discipline_display() for review in review_list.iterator()]
        discipline_counter = Counter(discipline_list)
        context["discipline_size"] = len(discipline_list)
        context["discipline_keys"] = list(discipline_counter.keys())
        context["discipline_values"] = list(discipline_counter.values())

        leave_list = [review.get_leave_display() for review in review_list.iterator()]
        leave_counter = Counter(leave_list)
        context["leave_size"] = len(leave_list)
        context["leave_keys"] = list(leave_counter.keys())
        context["leave_values"] = list(leave_counter.values())

        return context


class CreateTroop(LoginRequiredMixin, CreateView):
    model = Troop
    form_class = TroopForm
    template_name = 'troop_review/create_troop.html'

    def form_valid(self, form):
        current_user = self.request.user
        form.instance.author = current_user
        return super(CreateTroop, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('troop_review:create_review', args=(self.object.id,))


class CreateReview(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'troop_review/create_review.html'

    def form_valid(self, form):
        current_user = self.request.user
        form.instance.reviewer = current_user

        current_troop = Troop.objects.get(pk=self.kwargs['pk'])
        form.instance.troop = current_troop

        return super(CreateReview, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateReview, self).get_context_data(**kwargs)
        context['current_troop'] = Troop.objects.get(pk=self.kwargs['pk'])

        return context

    def get_success_url(self):
        return reverse_lazy('troop_review:detail', args=(self.kwargs['pk'],))


class UpdateReview(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'troop_review/update_review.html'

    def dispatch(self, request, *args, **kwargs):
        current_review = Review.objects.get(pk=self.kwargs['pk'])

        if current_review.reviewer == self.request.user:
            return super(UpdateReview, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super(UpdateReview, self).get_context_data(**kwargs)
        context['current_troop'] = Troop.objects.get(pk=self.kwargs['troop_pk'])

        return context

    def get_success_url(self):
        return reverse_lazy('troop_review:detail', args=(self.kwargs['troop_pk'],))


class DeleteReview(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = 'troop_review/delete_review.html'

    def dispatch(self, request, *args, **kwargs):
        current_review = Review.objects.get(pk=self.kwargs['pk'])

        if current_review.reviewer == self.request.user:
            return super(DeleteReview, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super(DeleteReview, self).get_context_data(**kwargs)
        current_review = Review.objects.get(pk=self.kwargs['pk'])
        context['review'] = current_review
        return context

    def get_success_url(self):
        return reverse_lazy('troop_review:detail', args=(self.kwargs['troop_pk'],))
