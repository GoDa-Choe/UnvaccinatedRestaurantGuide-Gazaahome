from django.shortcuts import render, redirect, get_object_or_404
from forum.forms import CommentForm, PostForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from hitcount.views import HitCountDetailView

# forms
from troop_review.forms import TroopForm, ReviewForm

# models
from forum.models import Post, Category, Tag
from troop_review.models import Troop, Review
from django.contrib.auth.models import User


@require_POST
@login_required
def like(request, troop_pk, pk):
    review = get_object_or_404(Review, pk=request.POST.get('review_pk'))
    if review.likes.filter(pk=request.user.pk).exists():
        review.likes.remove(request.user)
    else:
        review.likes.add(request.user)

    return HttpResponseRedirect(reverse('troop_review:detail', args=(troop_pk,)))


# class PostDelete(LoginRequiredMixin, DeleteView):
#     model = Post
#     template_name = 'forum/post_delete_form.html'
#
#     def dispatch(self, request, *args, **kwargs):
#         post = Post.objects.get(pk=self.kwargs['pk'])
#         if post.author == self.request.user:
#             return super(PostDelete, self).dispatch(request, *args, **kwargs)
#         else:
#             raise PermissionDenied
#
#     def get_context_data(self, **kwargs):
#         context = super(PostDelete, self).get_context_data(**kwargs)
#         post = Post.objects.get(pk=self.kwargs['pk'])
#         context['post'] = post
#         return context
#
#     def get_success_url(self):
#         return reverse_lazy('index')
#
#
# class PostUpdate(LoginRequiredMixin, UpdateView):
#     model = Post
#     form_class = PostForm
#     template_name = 'forum/post_update_form.html'
#
#     def dispatch(self, request, *args, **kwargs):
#         if request.user.is_authenticated and request.user == self.get_object().author:
#             return super(PostUpdate, self).dispatch(request, *args, **kwargs)
#         else:
#             raise PermissionDenied
#
#     def get_context_data(self, **kwargs):
#         context = super(PostUpdate, self).get_context_data()
#         if self.object.tags.exists():
#             tags_str_list = []
#             for tag in self.object.tags.all():
#                 tags_str_list.append(tag.name)
#             context['tags_str_default'] = '#' + '#'.join(tags_str_list)
#
#         return context
#
#     def form_valid(self, form):
#         response = super(PostUpdate, self).form_valid(form)
#         self.object.tags.clear()
#
#         tags_str = self.request.POST.get('tags_str')
#
#         if tags_str:
#             tags_str = tags_str.strip(' #')
#             tags_str = tags_str.replace(',', '#')
#             tags_list = tags_str.split('#')
#
#             for tag in tags_list:
#                 tag = tag.strip(' #')
#                 tag, is_tag_created = Tag.objects.get_or_create(name=tag)
#                 if is_tag_created:
#                     tag.slug = slugify(tag, allow_unicode=True)
#                     tag.save()
#                 self.object.tags.add(tag)
#
#         return response
#
#
# class PostCreate(LoginRequiredMixin, CreateView):
#     model = Post
#     form_class = PostForm
#
#     def form_valid(self, form):
#         current_user = self.request.user
#         if current_user.is_authenticated:
#             form.instance.author = current_user
#             response = super(PostCreate, self).form_valid(form)
#
#             tags_str = self.request.POST.get('tags_str')
#
#             if tags_str:
#                 tags_str = tags_str.strip(' #')
#                 tags_str = tags_str.replace(',', '#')
#                 tags_list = tags_str.split('#')
#
#                 for tag in tags_list:
#                     tag = tag.strip()
#                     tag, is_tag_created = Tag.objects.get_or_create(name=tag)
#                     if is_tag_created:
#                         tag.slug = slugify(tag, allow_unicode=True)
#                         tag.save()
#                     self.object.tags.add(tag)
#
#             return response
#         else:
#             return redirect('/forum/')
#
#
# class LikesPostList(ListView):
#     model = Post
#     template_name = 'forum/post_list.html'
#     paginate_by = 10
#     queryset = sorted(Post.objects.all(), key=lambda post: (post.num_likes(), post.pk), reverse=True)[:20]
#
#     context_object_name = 'post_list'
#
#     def get_context_data(self, **kwargs):
#         context = super(LikesPostList, self).get_context_data()
#         context['categories'] = Category.objects.all().order_by("priority")
#         context['category'] = "특급"
#
#         return context
#
#
# class PopularPostList(ListView):
#     model = Post
#     template_name = 'forum/post_list.html'
#     paginate_by = 10
#     context_object_name = 'post_list'
#     queryset = Post.objects.order_by("-hit_count_generic__hits", '-pk')[:20]
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super(PopularPostList, self).get_context_data()
#         context['post_list'] = context['post_list'][:15]
#         context['categories'] = Category.objects.all().order_by("priority")
#         context['category'] = "인기"
#
#         return context
#
#
# class CategoryPostList(ListView):
#     model = Post
#     template_name = 'forum/post_list.html'
#     paginate_by = 10
#     context_object_name = 'post_list'
#
#     def get_queryset(self):
#         category = Category.objects.get(slug=self.kwargs['slug'])
#         notice_manager = User.objects.get(username="공지사항")
#         return category.post_set.exclude(author=notice_manager).order_by('-pk')
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super(CategoryPostList, self).get_context_data()
#         category = Category.objects.get(slug=self.kwargs['slug'])
#         notice_manager = User.objects.get(username="공지사항")
#         notice_list = category.post_set.filter(author=notice_manager)
#
#         context['category'] = category
#         context['categories'] = Category.objects.all().order_by("priority")
#         context['notice_list'] = notice_list
#         return context
#
#
# class PostList(ListView):
#     model = Post
#     template_name = 'forum/post_list.html'
#     context_object_name = 'post_list'
#     paginate_by = 10
#
#     def get_queryset(self):
#         notice_manager = User.objects.get(username="공지사항")
#         post_list = Post.objects.exclude(author=notice_manager).order_by('-pk')
#         return post_list
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super(PostList, self).get_context_data()
#         context['categories'] = Category.objects.all().order_by("priority")
#
#         return context
#
#
# class PostDetail(HitCountDetailView):
#     model = Post
#     template_name = 'forum/post_detail.html'
#     count_hit = True
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super(PostDetail, self).get_context_data()
#         context['categories'] = Category.objects.all().order_by("priority")
#         context['comment_form'] = CommentForm
#
#         likes_connected = get_object_or_404(Post, pk=self.kwargs['pk'])
#         liked = False
#         if likes_connected.likes.filter(pk=self.request.user.pk).exists():
#             liked = True
#         context['num_likes'] = likes_connected.num_likes()
#         context['is_liked'] = liked
#
#         return context


class TroopList(ListView):
    model = Troop
    template_name = 'troop_review/index.html'
    context_object_name = 'troop_reivew_list'
    paginate_by = 10


class TroopDetail(HitCountDetailView):
    model = Troop
    template_name = 'troop_review/detail.html'
    count_hit = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TroopDetail, self).get_context_data()

        # context['categories'] = Category.objects.all().order_by("priority")
        # context['comment_form'] = CommentForm
        #
        # likes_connected = get_object_or_404(Post, pk=self.kwargs['pk'])
        # liked = False
        # if likes_connected.likes.filter(pk=self.request.user.pk).exists():
        #     liked = True
        # context['num_likes'] = likes_connected.num_likes()
        # context['is_liked'] = liked

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
        context['current_troop'] = Troop.objects.get(pk=self.kwargs['pk'])

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
