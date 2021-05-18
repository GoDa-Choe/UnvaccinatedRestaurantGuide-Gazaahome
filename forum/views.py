from django.shortcuts import render, redirect, get_object_or_404
from forum.models import Post, Category, Tag, Comment
from forum.forms import CommentForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from hitcount.views import HitCountDetailView


@require_POST
@login_required
def like(request, pk):
    post = get_object_or_404(Post, pk=request.POST.get('post_id'))
    if post.likes.filter(pk=request.user.pk).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('detail', args=(pk,)))


class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post
    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied


def new_comment(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)

            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()

                return redirect(comment.get_absolute_url())
        else:
            return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'forum/post_delete_form.html'

    def dispatch(self, request, *args, **kwargs):
        post = Post.objects.get(pk=self.kwargs['pk'])
        if post.author == self.request.user:
            return super(PostDelete, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super(PostDelete, self).get_context_data(**kwargs)
        post = Post.objects.get(pk=self.kwargs['pk'])
        context['post'] = post
        return context

    def get_success_url(self):
        return reverse_lazy('index')


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'head_image', 'category']
    template_name = 'forum/post_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super(PostUpdate, self).get_context_data()
        if self.object.tags.exists():
            tags_str_list = []
            for tag in self.object.tags.all():
                tags_str_list.append(tag.name)
            context['tags_str_default'] = '#' + '#'.join(tags_str_list)

        return context

    def form_valid(self, form):
        response = super(PostUpdate, self).form_valid(form)
        self.object.tags.clear()

        tags_str = self.request.POST.get('tags_str')

        if tags_str:
            tags_str = tags_str.strip(' #')
            tags_str = tags_str.replace(',', '#')
            tags_list = tags_str.split('#')

            for tag in tags_list:
                tag = tag.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name=tag)
                if is_tag_created:
                    tag.slug = slugify(tag, allow_unicode=True)
                    tag.save()
                self.object.tags.add(tag)

        return response


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'head_image', 'category']

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
            response = super(PostCreate, self).form_valid(form)

            tags_str = self.request.POST.get('tags_str')

            if tags_str:
                tags_str = tags_str.strip(' #')
                tags_str = tags_str.replace(',', '#')
                tags_list = tags_str.split('#')

                for tag in tags_list:
                    tag = tag.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=tag)
                    if is_tag_created:
                        tag.slug = slugify(tag, allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)

            return response
        else:
            return redirect('/forum/')


def tag_post(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()

    context = {
        'post_list': post_list.order_by('-pk'),
        'tag': tag,
        'categories': Category.objects.all(),
        'num_noncategory_posts': Post.objects.filter(category=None).count(),
    }

    return render(
        request,
        'forum/post_list.html',
        context,
    )


def category_post(request, slug):
    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    context = {
        'post_list': post_list.order_by('-pk'),
        'categories': Category.objects.all(),
        'num_noncategory_posts': Post.objects.filter(category=None).count(),
        'category': category
    }

    return render(
        request,
        'forum/post_list.html',
        context,
    )


class PostList(ListView):
    model = Post
    template_name = 'forum/post_list.html'
    ordering = '-pk'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['num_noncategory_posts'] = Post.objects.filter(category=None).count()

        return context


class PostDetail(HitCountDetailView):
    model = Post
    template_name = 'forum/post_detail.html'
    count_hit = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['num_noncategory_posts'] = Post.objects.filter(category=None).count()
        context['comment_form'] = CommentForm

        likes_connected = get_object_or_404(Post, pk=self.kwargs['pk'])
        liked = False
        if likes_connected.likes.filter(pk=self.request.user.pk).exists():
            liked = True
        context['num_likes'] = likes_connected.num_likes()
        context['is_liked'] = liked

        return context
